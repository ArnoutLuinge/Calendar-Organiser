from ast import keyword
from distutils.command.config import config
from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC # timezone
import yaml
import requests
import create_cfg
import os.path
from os import path

#check wether the config file exists, if not make one
if not path.exists("config.yml"):
    print("No config file found, lets create one")
    create_cfg.make_cfg()

if not os.path.exists("new_calendars"):
    os.makedirs("new_calendars")

# Read YAML file
with open("config.yml", 'r') as stream:
    config_data = yaml.safe_load(stream)

#get the file using requests
def get_file(ical_link):
    ical_file = requests.get(ical_link)
    print("Source calendar downloaded")
    cal = open("temp_calendar.ics", 'wb').write(ical_file.content)
    cal = open("temp_calendar.ics", 'rb')
    return cal

def organise(ical_link, sorting_keywords):
    org_cal = get_file(ical_link)
    cal = Calendar.from_ical(org_cal.read())

    #create calendars for each keyword plus one for misc / remaining events
    Misc_cal = Calendar()
    Misc_cal.add('prodid', '-//Arnouts great calendar//EN')
    Misc_cal.add('version', '2.0')

    i = 0
    while i < len(sorting_keywords):
        Temp_cal = Calendar()
        Temp_cal.add('prodid', '-//Arnouts great calendar//EN')
        Temp_cal.add('version', '2.0')

        for component in cal.walk():
            if component.name == "VEVENT":
                if "Type: " + sorting_keywords[i] in component.get('description'):
                    event = Event()
                    event.add('summary', sorting_keywords[i] + " " + component.get('summary'))
                    event.add('dtstart', component.get('dtstart'))
                    event.add('dtend', component.get('dtend'))
                    event.add('dtstamp', component.get('dtstamp'))
                    event.add('location', component.get('location'))
                    event.add('description', isolate_staff(component.get('description')))
                    event.add('priority', i)
                    Temp_cal.add_component(event)
                # else:
                #     event = Event()
                #     event.add('summary', component.get('summary'))
                #     event.add('dtstart', component.get('dtstart'))
                #     event.add('dtend', component.get('dtend'))
                #     event.add('dtstamp', component.get('dtstamp'))
                #     event.add('location', component.get('location'))
                #     event.add('description', isolate_staff(component.get('description')))
                #     event.add('priority', 10)
                #     Misc_cal.add_component(event)

        f = open('new_calendars/' + sorting_keywords[i] + '_cal.ics', 'wb')
        f.write(Temp_cal.to_ical())
        f.close()
        print(sorting_keywords[i] + "_cal file created")
        i +=1


    f = open('new_calendars/Misc_cal.ics', 'wb')
    f.write(Misc_cal.to_ical())
    f.close()
    print("Misc_cal file created")

    org_cal.close()
    return 0

def isolate_staff(org_desc):
    if 'Staff member(s):' in org_desc:
        start = org_desc.find('Staff member(s):')
        end = len(org_desc) - start
        org_desc = org_desc[start:]
        end = org_desc.find('\n')
        return org_desc[:end]

organise(config_data['Calendar_URL'], config_data['keywords'])

os.remove("temp_calendar.ics")