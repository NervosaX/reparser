import modules

from django.core.management.base import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyvirtualdisplay import Display

from base.models import Detail, RailwayPosition

import re
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
        logger.debug("Initializing display ...")
        if settings.USE_HIDDEN_DISPLAY:
            display = Display(visible=0, size=(800, 600))
            display.start()

        browser = webdriver.Firefox()

        realestate = modules.realestate.CollectData(**{
            'browser': browser,
            'search_string': settings.REAL_ESTATE_SEARCH_STRING,
            #'max_pages': 1,    
        })

        logger.debug("Getting realestate data ...")
        details = realestate.get()
        
        for detail in details:
            address = detail['address']

            exists = Detail.objects.filter(address=address)
            if exists:
                continue

            logger.debug(address + " does not exist. Attempting data collection.")
         
            # TODO: Insert regex to get prices!
            # (\d+,*\d*[Kk]?)*

            details = {
                'address': detail['address'],
                'title': detail['title'],
                'price': detail['price'],
                'url': detail['url'],
                'bedrooms': detail['bedrooms'],
                'bathrooms': detail['bathrooms'],
                'carspaces': detail['carspaces'],
                'status': 'N', # A big fat NO unless it passes everything
            }

            new_detail = Detail.objects.create(**details)

            suburb_excludes = [
                'Frankston', 'Cranbourne', 'Carrum Downs', 'Pakenham', 'North Clyde', 
                'Carrum', 'Patterson Lakes', 'Dandenong', 'Noble Park', 'Seaford',
                'Sandhurst', 'Narre Warren', 'Endeavour Hills', 'Boronia'
            ]

            excluded = False
            for s_exclude in suburb_excludes:
                if s_exclude in address > 0:
                    logger.debug("... ... Bad Suburb, ignoring (" + s_exclude + ")")
                    excluded = True
                    break

            if excluded:
                continue

            if detail['bedrooms'] < 3:
                logger.debug("... ... ... Under three bedrooms. Skipping.")
                continue

            if detail['bathrooms'] < 2:
                logger.debug("... ... ... Under two bathrooms. Skipping.")
                continue

            # Get public travel time from address
            logger.debug("... ... PTMelb travel time from Collingwood to address.")
            pt = modules.ptmelb.PublicTransport()
            pt_data = pt.get(address, browser)

            if pt_data:
                _td = tdelta(pt_data['duration'])
                if _td > tdelta("1h 15m"):
                    logger.debug("... ... ... Skipping, too far away. (" + pt_data['duration'] + ")")
                    continue

                try:
                    new_detail.pt_depart_time = pt_data['departTime']
                    new_detail.pt_arrive_time = pt_data['arriveTime']
                    new_detail.pt_duration = pt_data['duration']
                except KeyError:
                    continue


            logger.debug("... ... Checking google maps car travel time.")
            gmaps = modules.gmaps.GMaps()
            directions = gmaps.get_travel_time_between(detail['address'], "Melbourne, Oakleigh, Victoria, Australia")
            if directions:
                detail.oak_summary = directions


            # Get possible ADSL2+ speed
            logger.debug("... ... Checking possible ADSL2+ speed.")
            adsl2 = modules.adsl2.ADSL2()
            adsl2_data = adsl2.get(address, browser)

            if adsl2_data:
                if adsl2_data['estimated_speed'] < 8000:
                    logger.debug("... ... ... Internet will be too slow. (" + adsl2_data['estimated_speed'] + ")")
                    continue

                try:
                    new_detail.crow_fly_distance = adsl2_data['crow_fly_distance']
                    new_detail.cable_length = adsl2_data['cable_length']
                    new_detail.estimated_speed = adsl2_data['estimated_speed']
                except KeyError:
                    continue

            # Allow the address to be seen
            new_detail.status = "U"
            new_detail.save()

            # Get nearby railways
            logger.debug("... ... Getting nearby railways.")
            distances = gmaps.get_distance_from_railways(address)

            if distances:
                for distance in distances:
                    try:
                        RailwayPosition.objects.create(**{
                            'detail': new_detail,
                            'line_name': distance['line_name'],
                            'distance': distance['distance']
                        })
                    except KeyError:
                        continue

            logger.debug("... ...  ... added address.")

        browser.close()

        if settings.USE_HIDDEN_DISPLAY:
            display.stop()
