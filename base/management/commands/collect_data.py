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
        
        if settings.USE_HIDDEN_DISPLAY:
            display = Display(visible=0, size=(800, 600))
            display.start()

        browser = webdriver.Firefox()

        realestate = modules.realestate.CollectData(**{
            'browser': browser,
            'search_string': settings.REAL_ESTATE_SEARCH_STRING,
            # 'max_pages': 1,
        })

        details = realestate.get()

        for detail in details:
            address = detail['address']

            detail_obj = Detail.objects.filter(address=address)

            if not detail_obj:
                # Get nearby railways
                gmaps = modules.gmaps.GMaps()
                distances = gmaps.get_distance_from_railways(address)

                # Get possible ADSL2+ speed
                adsl2 = modules.adsl2.ADSL2()
                adsl2_data = adsl2.get(address, browser)

                # Get public travel time from address
                pt = modules.ptmelb.PublicTransport()
                pt_data = pt.get(address, browser)

                # Add to database
                print "Does not exist, creating...", address
                
                details = {
                    'address': detail['address'],
                    'title': detail['title'],
                    'price': detail['price'],
                    'url': detail['url'],
                    'bedrooms': detail['bedrooms'],
                    'bathrooms': detail['bathrooms'],
                    'carspaces': detail['carspaces'],
                }

                if pt_data:
                    details.update({
                        'pt_depart_time': pt_data['departTime'],
                        'pt_arrive_time': pt_data['arriveTime'],
                        'pt_duration': pt_data['duration'],
                    })

                if adsl2_data:
                    details.update({
                        'crow_fly_distance': adsl2_data['crow_fly_distance'],
                        'cable_length': adsl2_data['cable_length'],
                        'estimated_speed': adsl2_data['estimated_speed'],
                    })

                new_detail = Detail.objects.create(**details)

                if distances:
                    for distance in distances:
                        RailwayPosition.objects.create(**{
                            'detail': new_detail,
                            'line_name': distance['line_name'],
                            'distance': distance['distance']
                        })
            else:
                print "Already got it...", address

        browser.close()

        if settings.USE_HIDDEN_DISPLAY:
            display.stop()