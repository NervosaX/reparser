import modules

from django.core.management.base import BaseCommand
from django.conf import settings

from selenium import webdriver
from pyvirtualdisplay import Display


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
            'max_pages': 1,
        })

        details = realestate.get()

        for detail in details:
            address = detail['address']

            # Get nearby railways
            gmaps = modules.gmaps.GMaps()
            distance = gmaps.get_distance_from_railways(address)
            print distance

            # Get possible ADSL2+ speed
            adsl2 = modules.adsl2.ADSL2()
            adsl2_data = adsl2.get(address, browser)
            print adsl2_data

            # Get public travel time from address
            pt = modules.ptmelb.PublicTransport()
            pt_data = pt.get(address, browser)
            print pt_data


        browser.close()

        if settings.USE_HIDDEN_DISPLAY:
            display.stop()