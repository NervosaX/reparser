import os
import time
import selenium.webdriver.support.ui as ui

from math import radians, cos, sin, asin, sqrt

from django.core.management.base import BaseCommand
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pyvirtualdisplay import Display

from bs4 import BeautifulSoup
from googlemaps import GoogleMaps

class Command(BaseCommand):
    args = ""
    help = ""

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km 

    def handle(self, *args, **options):
        options = {
            'basic_info': True,
            'features': True,
            'railways': True,
            'adsl2': True,
            'metlink': True,

            'use_display': False,
        }

        if (options['use_display']):
            display = Display(visible=0, size=(800, 600))
            display.start()

        browser = webdriver.Firefox()

        filename = os.path.join(settings.PROJECT_ROOT, 'tests', 'test1.html')
        template = BeautifulSoup(open(filename, 'r').read())

        resultBodies = template.findAll("div", class_="resultBody")

        # Info!
        for results in resultBodies:
            current = results
            address = current.find("a", class_="name").getText()
            
            # Skip any 'address' that needs to be requested.
            # Screw that
            if 'request' in address or 'available' in address or "/" in address:
                continue

            title = current.find("h3", class_="title").getText()
            price = current.find("p", class_="price").find("span").getText()
            url = current.find("a", class_="name")["href"]

            try:
                agent = current.find("div", class_="agentTextLight").img["alt"]
            except AttributeError:
                try:
                    agent = current.findAll("img")[5]["alt"]
                except Exception:
                    agent = "Unknown"

            if (options['basic_info']):
                self.stdout.write(
                "\n" +
                "########################################\n" +
                "#              Basic Info              #\n" +
                "########################################"
                )        

                self.stdout.write("Address: " + address)
                self.stdout.write("Title: " + title)
                self.stdout.write("Agent: " + agent)
                self.stdout.write("Price: " + price)
                self.stdout.write("Link: " + url)


            features = current.find("ul", class_="propertyFeatures").findAll('li')
            rooms = features[0].span.getText()
            bathrooms = features[1].span.getText()
            cars = features[2].span.getText()

            if (options['features']):
                self.stdout.write(
                "\n" +
                "########################################\n" +
                "#               Features               #\n" +
                "########################################"
                )

                self.stdout.write("Rooms: " + rooms)
                self.stdout.write("Bathrooms: " + bathrooms)
                self.stdout.write("Carport/garage: " + cars)


            if (options['railways']):
                self.stdout.write(
                "\n" +
                "########################################\n" +
                "#               Railways               #\n" +
                "########################################"
                )

                success = False
                attempts = 0
                while (success == False and attempts <= 3):
                    try:
                        gmaps = GoogleMaps()
                        lat, lng = gmaps.address_to_latlng(address)

                        gaddress = gmaps.local_search('railway near ' + address)
                        for result in gaddress['responseData']['results']:
                            if int(result["accuracy"]) > 5:
                                continue

                            self.stdout.write(result['titleNoFormatting'])
                            self.stdout.write("distance: " +   
                                str(self.haversine(lng, lat, float(result["lng"]), float(result["lat"]))) + " km")
                        success = True
                    except:
                        self.stdout.write("NoSuchElementException!!!!")
                        browser.close()
                        browser = webdriver.Firefox()
                        browser.get('http://www.adsl2exchanges.com.au/')
                        time.sleep(500)
                        attempts += 1
                        self.stdout.write("Attempt " + str(attempts))


            if (options['adsl2']):
                self.stdout.write(
                "\n" +
                "########################################\n" +
                "#              ADSL2 Speed             #\n" +
                "########################################"
                )
  
                wait = ui.WebDriverWait(browser, 10)

                success = False
                attempts = 0
                while (success == False and attempts <= 3):
                    browser.get('http://www.adsl2exchanges.com.au/')
                    form = browser.find_elements_by_tag_name("form")[2]
                    form_address = form.find_element_by_name("Address")
                    form_state = form.find_element_by_name("State")

                    form_state.send_keys("VIC")
                    form_address.send_keys(address + Keys.RETURN)

                    try:
                        try:
                            wait.until(lambda browser: browser.find_element_by_id("map").get_attribute("innerHTML").strip() != "")
                        except TimeoutException:
                            pass
        
                        adsl_source = BeautifulSoup(browser.find_element_by_id("map").get_attribute("innerHTML"))
                        divs = [x for x in adsl_source.findAll("div") if "Estimated" in x.getText()]
                        adsldata = divs[len(divs) - 1]

                        print adsldata

                        success = True
                    except NoSuchElementException:
                        browser.close()
                        browser = webdriver.Firefox()
                        time.sleep(500)
                        attempts += 1
                        self.stdout.write("Attempt " + str(attempts))


            if (options['metlink']):
                self.stdout.write(
                "\n" +
                "########################################\n" +
                "#              Metlink time            #\n" +
                "########################################"
                )
                wait = ui.WebDriverWait(browser, 10)
                browser.get('http://jp.ptv.vic.gov.au/ptv/XSLT_TRIP_REQUEST2?language=en&itdLPxx_view=advanced')
                
                # Set to departing
                browser.find_element_by_name("itdTripDateTimeDepArr").send_keys("Departing")
                # Set to 4th day of Feb, 2013 (A Monday) at 8:00 AM
                browser.find_element_by_id("itdDateDay").send_keys("04")
                browser.find_element_by_name("itdDateYearMonth").send_keys("Feb 2013")
                browser.find_element_by_name("itdTimeHour").send_keys("8")
                browser.find_element_by_name("itdTimeMinute").send_keys("0")
                browser.find_element_by_name("itdTimeAMPM").send_keys("AM")
                # Set fast walking pace
                browser.find_element_by_name("changeSpeed").send_keys("Fast (6 km/hr)")
                # Set longer walking distance
                browser.find_element_by_name("trITMOTvalue100").send_keys("15 min")

                # Select address
                browser.find_element_by_id("tab1Link_origin").click()
                # Insert address
                browser.find_element_by_id("input_origin").send_keys(address)
                # Insert Richmond station
                browser.find_element_by_id("input_destination").send_keys("Richmond Railway Station" + Keys.RETURN)

                try:
                    wait.until(lambda browser: browser.find_element_by_name("tripRequest").get_attribute("innerHTML").strip() != "")
                except TimeoutException:
                    pass

                source = BeautifulSoup(browser.find_element_by_class_name("p4").get_attribute("innerHTML"))

                tds = source.findAll("td")
                departTime = tds[1].getText()
                arriveTime = tds[2].getText()
                duration = tds[3].getText()

                self.stdout.write("Depart Time: " + departTime)
                self.stdout.write("Arrive Time: " + arriveTime)
                self.stdout.write("Duration: " + duration)


            self.stdout.write(
            "\n" +
            "***********************************************************************************\n" +
            "***********************************************************************************\n"
            )

        browser.close()

        if (options['use_display']):
            display.stop()