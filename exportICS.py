from icalendar import Calendar, Event
from datetime import datetime
from datetime import timedelta
from pytz import UTC
import json
import os

BASE_PATH = 'docs/data/class/'
PROD = "2018_2019-2_2_4LCDI"
classCode = "21221"
def createICS():
    for filename in os.listdir(BASE_PATH):
        print('[PROCESSING] ' + filename)
        file = open(BASE_PATH + filename);
        data = json.loads(file.read())
        process_data(data, filename, classCode)
        # TODO put classes with same class code together

def process_data(data, name, classCode):
    cal = Calendar()
    cal.add('prodid', '-//MPIBsC//' + name + '//EN')
    cal.add('version', '1.0')
    cal.add('name', name)
    cal.add('X-WR-CALNAME', name)
    cal.add('X-WR-TIMEZONE', 'Asia/Macau')

    for item in data:
        if item['class_code'][-5: ] == classCode:
            event = Event()
            event.add('tzname', 'Asia/Macau')
            event.add('summary', item['subject'])
            event.add('description', item['class_code'])
            dp = item['period'][0]
            tp = item['time'][0]
            dtstart = dp[0: dp.find('-')] + tp[0:tp.find('-')]
            dtend = dp[0: dp.find('-')] + tp[tp.find('-') + 1: ]
            rend = dp[dp.find('-') + 1:] + tp[tp.find('-') + 1: ]
            byday = ''
            for key, value in item['day'].iteritems():
                if value == 'true':
                    byday = key

            if byday == 'mo':
                weekDay = 0
            if byday == 'tu':
                weekDay = 1
            if byday == 'we':
                weekDay = 2
            if byday == 'th':
                weekDay = 3
            if byday == 'fr':
                weekDay = 4
            if byday == 'sa':
                weekDay = 5
            if byday == 'su':
                weekDay = 6
            dtstart = datetime.strptime(dtstart, '%Y/%m/%d%H:%M')
            dtend = datetime.strptime(dtend, '%Y/%m/%d%H:%M')
            if weekDay >= dtstart.weekday():
                tld = timedelta(days = weekDay - dtstart.weekday())
                dtstart += tld
                dtend += tld

            print(item['class_code'] + ' ' + str(dtstart) + ' ' + byday)

            event.add('uid', item['class_code'] + byday + dp + tp + '@ipm.edu.mo')
            event.add('dtstamp', datetime.now())
            event.add('dtstart', dtstart)
            event.add('dtend', dtend)
            event.add('location', item['room'][0])
            event.add('rrule', {'FREQ': "WEEKLY", 'BYDAY': byday, 'UNTIL': datetime.strptime(rend, '%Y/%m/%d%H:%M')})
            cal.add_component(event)

    f = open('docs/calendar/' + PROD + classCode + '.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

createICS()
