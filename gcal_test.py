import pprint

import gflags
import httplib2
import datetime
from rfc3339 import *
import dateutil.parser as parser

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Developers Console
FLOW = OAuth2WebServerFlow(
    client_id='1025989757471-qvk9ucnvbupq6ap31kplk7i74nva9a3d.apps.googleusercontent.com',
    client_secret='835igyR3nveJQota0gviI2SN',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='YOUR_APPLICATION_NAME/YOUR_APPLICATION_VERSION')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google Developers Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='YOUR_DEVELOPER_KEY')

def makeMenu(title, menuList):
    menuString = "%s\n======================\n\n" % title.upper()
    for i in xrange(len(menuList)):
        if len(menuList[i]) == 2:
            menuString += "%d: %s\n" % (i+1, menuList[i][1])
    menuString += "\nWhich option do you choose: "

    option = raw_input(menuString)
    print

    try:
        option = int(option) - 1
        if option < len(menuList) and option >= 0:
            print
            return menuList[option]
        else:
            print "Invalid option, try again."
    except:
        pass

    print
    return makeMenu(title, menuList)

def main():

    page_token = None

    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      calendar_shorter_list = map(lambda cal: (cal['id'], cal['summary']), calendar_list['items'])

      cal = makeMenu("Get the cal", calendar_shorter_list)
      print ("You have chosen: %s" % cal[1])
      print

      page_token = calendar_list.get('nextPageToken')

      if not page_token:
        break

    page_token = None

    while True:
        events = service.events().list(calendarId=cal[0], orderBy='startTime', singleEvents='True',
                                       timeMin=rfc3339(datetime.datetime(2010,11,10)),
                                       timeMax=rfc3339(datetime.datetime(2014,11,28)),
                                       pageToken=page_token).execute()

        #pprint.pprint(events)

        for event in events['items']:
            #pprint.pprint(event)
            if 'dateTime' in event['start']:
                print event['summary'], ": From %s to %s" % ((parser.parse(event['start']['dateTime'])).strftime("%A, %d. %B %Y %I:%M%p"), (parser.parse(event['end']['dateTime'])).strftime("%A, %d. %B %Y %I:%M%p"))
            elif 'date' in event['start']:
                print event['summary'], ": On %s" % parser.parse(event['start']['date']).strftime("%A, %d. %B %Y")
            else:
                print event['summary'], "is a weird event..."

        page_token = events.get('nextPageToken')

        if not page_token:
            break

if __name__ == "__main__":
    cont = True

    while cont:
        print
        main()
        print
        cont = True if raw_input("Another request? (Y/N): ") == "Y" else False

