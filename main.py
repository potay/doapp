# Write some headers here

import pprint

# G-Cal Connection Class

import gflags
import httplib2
import datetime
from rfc3339 import rfc3339
import dateutil.parser as parser

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

class GoogleConnection(object):
    CLIENT_ID = '1025989757471-qvk9ucnvbupq6ap31kplk7i74nva9a3d.apps.googleusercontent.com'
    CLIENT_SECRET = '835igyR3nveJQota0gviI2SN'
    SCOPE = 'https://www.googleapis.com/auth/calendar'
    USER_AGENT = 'YOUR_APPLICATION_NAME/YOUR_APPLICATION_VERSION'
    DEVELOPER_KEY = 'YOUR_DEVELOPER_KEY'

    DATA_FOLDER = 'data/calendars/'

    FLAGS = gflags.FLAGS
    FLOW = OAuth2WebServerFlow(client_id=CLIENT_ID,
                               client_secret=CLIENT_SECRET,
                               scope=SCOPE,
                               user_agent=USER_AGENT)

    def __init__(self, dataFile="default.dat"):
        storage = Storage(GoogleConnection.DATA_FOLDER+dataFile)
        credentials = storage.get()
        if (credentials is None or credentials.invalid == True):
            credentials = run(GoogleConnection.FLOW, storage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build(serviceName='calendar',
                             version='v3',
                             http=http,
                             developerKey=GoogleConnection.DEVELOPER_KEY)

    def makeMenu(self, title, menuList):
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
        return self.makeMenu(title, menuList)

    def getCalendar(self):
        page_token = None

        while True:
            calList = self.service.calendarList().list(
                        pageToken=page_token).execute()
            calListShort = map(lambda cal: (cal['id'], cal['summary']),
                           calList['items'])

            cal = self.makeMenu("Get the cal", calListShort)
            print ("You have chosen: %s" % cal[1])
            print

            page_token = calList.get('nextPageToken')

            if not page_token:
                break

        return cal

    def printEvents(self, calID='primary', orderBy='startTime',
                    singleEvents=True, timeMin=datetime.datetime(2010,11,10),
                    timeMax=datetime.datetime(2010,11,28)):
        page_token = None

        while True:
            events = self.service.events().list(
                        calendarId=calID,
                        orderBy=orderBy,
                        singleEvents=str(singleEvents),
                        timeMin=rfc3339(timeMin),
                        timeMax=rfc3339(timeMax),
                        pageToken=page_token).execute()

            for event in events['items']:
                if ('dateTime' in event['start']):
                    print event['summary'], ": From %s to %s" % ((parser.parse(event['start']['dateTime'])).strftime("%A, %d. %B %Y %I:%M%p"), (parser.parse(event['end']['dateTime'])).strftime("%A, %d. %B %Y %I:%M%p"))
                elif ('date' in event['start']):
                    print event['summary'], ": On %s" % parser.parse(event['start']['date']).strftime("%A, %d. %B %Y")
                else:
                    print event['summary'], "is a weird event..."

            page_token = events.get('nextPageToken')

            if not page_token:
                break

# Lets try some basic calendar classes

# Event class

# Main Function
def main():
    print "Main file"
    print "Making connection..."
    gConn = GoogleConnection()
    print "Connection successful."
    print "Choosing Calendar"
    cal = gConn.getCalendar()
    print "Printing events"
    gConn.printEvents(cal[0], timeMin=datetime.datetime(2014,10,1),
                              timeMax=datetime.datetime(2014,12,12))

if __name__ == "__main__":
    main()
