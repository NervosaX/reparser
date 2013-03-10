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
        
        # browser = webdriver.Firefox()

        gmaps = modules.gmaps.GMaps()

        for detail in Detail.objects.filter(oak_summary=''):
            directions = gmaps.get_travel_time_between(detail.address, "Melbourne, Oakleigh, Victoria, Australia")
            if directions:
                print "Found", detail.address, "has:", directions
                detail.oak_summary = directions
                detail.save()
            else:
                print "Failed to get detail."

        # browser.close()