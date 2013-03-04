import os
import modules

from django.core.management.base import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyvirtualdisplay import Display

from base.models import Detail, RailwayPosition


class Command(BaseCommand):
    args = ""
    help = ""

    def handle(self, *args, **options):

        browser = webdriver.Firefox()

        file = os.path.join(settings.PROJECT_ROOT, 'addresses.txt')
        open_file = open(file, 'r')

        lines = [line.strip('\n') for line in open_file.readlines()]

        for line in lines:
            print "Checking address... ", line
            
            try:
                detail = Detail.objects.get(address=line)
            except Detail.DoesNotExist:
                continue

            details = {}

            # Check for PT data
            if True:#detail.pt_depart_time == "":
                # Get public travel time from address
                pt = modules.ptmelb.PublicTransport()
                pt_data = pt.get(line, browser)

                if pt_data:
                    details.update({
                        'pt_depart_time': pt_data['departTime'],
                        'pt_arrive_time': pt_data['arriveTime'],
                        'pt_duration': pt_data['duration'],
                    })
            else:
                print "Already got PT data"

            # Check for adsl2_data
            if True:#detail.crow_fly_distance == "":
                # Get possible ADSL2+ speed
                adsl2 = modules.adsl2.ADSL2()
                adsl2_data = adsl2.get(line, browser)
                if adsl2_data:
                    details.update({
                        'crow_fly_distance': adsl2_data['crow_fly_distance'],
                        'cable_length': adsl2_data['cable_length'],
                        'estimated_speed': adsl2_data['estimated_speed'],
                    })
            else:
                print "Already got ADSL2 data"

            detail.__dict__.update(details)
            detail.save()

            # Check for railway data
            if True:#detail.railwayposition_set.count() == 0:
                detail.railwayposition_set.all().delete()
                # Get nearby railways
                gmaps = modules.gmaps.GMaps()
                distances = gmaps.get_distance_from_railways(line)

                if distances:
                    for distance in distances:
                        RailwayPosition.objects.create(**{
                            'detail': detail,
                            'line_name': distance['line_name'],
                            'distance': distance['distance']
                        })
            else:
                print "Already got railway data"

        browser.close()