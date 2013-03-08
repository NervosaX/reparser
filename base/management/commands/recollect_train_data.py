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

        for detail in Detail.objects.filter(pt_duration=''):

            print detail.address
            print "Was", detail.pt_duration

            # Get public travel time from address
            pt = modules.ptmelb.PublicTransport()
            pt_data = pt.get(detail.address, browser)
            
            try:
                print "Is now", pt_data['duration']
                detail.pt_duration = pt_data['duration']
                detail.save()
            except TypeError:
                continue

        browser.close()