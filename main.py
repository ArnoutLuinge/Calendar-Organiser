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

# Read YAML file
with open("config.yml", 'r') as stream:
    config_data = yaml.safe_load(stream)


def get_file(ical_link):
    ical_file = requests.get(ical_link)
    print("Source calendar downloaded")
    cal = open("calendar.ics", 'wb').write(ical_file.content)
    cal = open("calendar.ics", 'rb')
    return cal

def organise(ical_link, sorting_keywords):
    org_cal = get_file(ical_link)
    cal = Calendar.from_ical(org_cal.read())
    
    #create calendars for each keyword plus one for misc / remaining events
    i = 4 #TODO not permanent!!!
    while i < len(sorting_keywords) + 1:
        Exam_cal = Calendar()
        Exam_cal.add('prodid', '-//Arnouts great calendar//EN')
        Exam_cal.add('version', '2.0')

        i +=1



    for component in cal.walk():
        if component.name == "VEVENT":
            if "Type: " + sorting_keywords[0] in component.get('description'):
                event = Event()
                event.add('summary', 'Exam ' + component.get('summary'))
                event.add('dtstart', component.get('dtstart'))
                event.add('dtend', component.get('dtend'))
                event.add('dtstamp', component.get('dtstamp'))
                event.add('location', component.get('location'))
                event.add('description', isolate_staff(component.get('description')))
                event.add('priority', 1)

                Exam_cal.add_component(event)


    f = open('Exam_cal.ics', 'wb')
    f.write(Exam_cal.to_ical())
    f.close()
    org_cal.close()

    print("Ical file created")

    return 0

def isolate_staff(org_desc):
    if 'Staff member(s):' in org_desc:
        start = org_desc.find('Staff member(s):')
        end = len(org_desc) - start
        org_desc = org_desc[start:]
        end = org_desc.find('\n')
        return org_desc[:end]

organise(config_data['Calendar_URL'], config_data['keywords'])