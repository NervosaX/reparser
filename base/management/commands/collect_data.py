import modules

from django.core.management.base import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyvirtualdisplay import Display

from base.models import Detail, RailwayPosition

import re
import datetime
from datetime import timedelta

import logging

logger = logging.getLogger("applog")

def tdelta(input):

    keys = ["weeks", "days", "hours", "minutes"]
    regex = "".join(["((?P<%s>\d+)%s ?)?" % (k, k[0]) for k in keys])
    kwargs = {}
    for k,v in re.match(regex, input).groupdict(default="0").items():
        kwargs[k] = int(v)
    return timedelta(**kwargs)

class Command(BaseCommand):
    args = ""
    help = ""

    def handle(self, *args, **options):
        print "--- RUNNING COLLECT DATA ---"
        logger.debug("Running on: " + str(datetime.datetime.now()))

        if settings.USE_HIDDEN_DISPLAY:
            display = Display(visible=0, size=(800, 600))
            display.start()

        browser = webdriver.Firefox()

        realestate = modules.realestate.CollectData(**{
            'browser': browser,
            'search_string': settings.REAL_ESTATE_SEARCH_STRING,
            #'max_pages': 1,    
        })

        details = realestate.get()

        
        for detail in details:
            address = detail['address']


            exists = Detail.objects.filter(address=address)
            if exists:
                continue

            address 

            suburb_excludes = [
                'Frankston', 'Cranbourne', 'Carrum Downs', 'Pakenham', 'North Clyde', 
                'Carrum', 'Patterson Lakes', 'Dandenong', 'Noble Park', 'Seaford',
                'Sandhurst', 'Narre Warren', 'Endeavour Hills', 'Boronia'
            ]

            excluded = False
            for s_exclude in suburb_excludes:
                if s_exclude in address > 0:
                    print "... ... Bad Suburb, ignoring."
                    excluded = True
                    break

            if excluded:
                continue


            print "Trying address", address, "... ..."
          
            # TODO: Insert regex to get prices!
            # (\d+,*\d*[Kk]?)*

            gmaps = modules.gmaps.GMaps()


            details = {
                'address': detail['address'],
                'title': detail['title'],
                'price': detail['price'],
                'url': detail['url'],
                'bedrooms': detail['bedrooms'],
                'bathrooms': detail['bathrooms'],
                'carspaces': detail['carspaces'],
            }

            detail = Detail.objects.create(**details)

            directions = gmaps.get_travel_time_between(detail['address'], "Melbourne, Oakleigh, Victoria, Australia")
            if directions:
                detail.oak_summary = directions

            if detail['bedrooms'] < 3:
                continue

            if detail['bathrooms'] < 2:
                continue

            # Get public travel time from address
            pt = modules.ptmelb.PublicTransport()
            pt_data = pt.get(address, browser)


            if pt_data:
                _td = tdelta(pt_data['duration'])
                if _td > tdelta("1h 15m"):
                    print "Skipping, too far away... ..."
                    continue

                try:
                    detail.pt_depart_time = pt_data['departTime']
                    detail.pt_arrive_time = pt_data['arriveTime']
                    detail.pt_duration = pt_data['duration']
                except KeyError:
                    continue


            # Get possible ADSL2+ speed
            adsl2 = modules.adsl2.ADSL2()
            adsl2_data = adsl2.get(address, browser)

            if adsl2_data:
                if adsl2_data['estimated_speed'] < 8000:
                    print "Internet is too slow... ..."
                    continue

                try:
                    detail.crow_fly_distance = adsl2_data['crow_fly_distance']
                    detail.cable_length = adsl2_data['cable_length']
                    detail.estimated_speed = adsl2_data['estimated_speed']
                    print "Adsl2 data found ..."
                except KeyError:
                    continue

            detail.save()

            # Get nearby railways
            distances = gmaps.get_distance_from_railways(address)

            if distances:
                print "Railway data found ..."
                for distance in distances:
                    try:
                        RailwayPosition.objects.create(**{
                            'detail': detail,
                            'line_name': distance['line_name'],
                            'distance': distance['distance']
                        })
                    except KeyError:
                        continue

            print "... House has been added."
            logger.debug("... ... added address: " + address)

        browser.close()

        if settings.USE_HIDDEN_DISPLAY:
            display.stop()
