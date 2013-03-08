import time
from django.conf import settings

from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class PublicTransport:

    """
    @max_attempts:
        Amount of attempts that can be made when trying to retrieve
        data from the adsl2exchanges.com.au page
    """
    def __init__(self, max_attempts=2):
        self.max_attempts = max_attempts

    """
    Get a possible traveling time with walking and public transport
    from an address to Richmond Station

    @address:
        The address to check against in the form of
        a string

    @browser:
        A selenium browser object

    @retry_wait:
        The amount of time in seconds before retrying an address
    """
    def get(self, address, browser, retry_wait=2):

        attempts = 0
        wait = ui.WebDriverWait(browser, 3)

        while True:
            browser.get(settings.METLINK_SEARCH_URL) 

            # Set to departing
            browser.find_element_by_name("itdTripDateTimeDepArr").send_keys("Departing")
            # Set to 4th day of Feb, 2013 (A Monday) at 8:00 AM
            browser.find_element_by_id("itdDateDay").send_keys("04")
            browser.find_element_by_name("itdDateYearMonth").send_keys("Feb 2013")
            browser.find_element_by_name("itdTimeHour").send_keys("5")
            browser.find_element_by_name("itdTimeMinute").send_keys("0")
            browser.find_element_by_name("itdTimeAMPM").send_keys("PM")
            # Set fast walking pace
            browser.find_element_by_name("changeSpeed").send_keys("Fast (6 km/hr)")
            # Set longer walking distance
            browser.find_element_by_name("trITMOTvalue100").send_keys("15 min")

            # Select address
            browser.find_element_by_id("tab1Link_destination").click()
            # Insert Richmond station
            browser.find_element_by_id("input_origin").send_keys("Collingwood Railway Station/Hoddle St")
            # Insert address
            browser.find_element_by_id("input_destination").send_keys(address + Keys.RETURN)

            try:
                try:
                    wait.until(lambda browser: browser.find_element_by_name("tripRequest").get_attribute("innerHTML").strip() != "")
                except TimeoutException:
                    pass

                source = BeautifulSoup(browser.find_element_by_class_name("p4").get_attribute("innerHTML"))

                tds = source.findAll("td")
                departTime = tds[1].getText()
                arriveTime = tds[2].getText()
                duration = tds[3].getText()

                print "Found PTMelb data..."
                return {
                    'departTime': departTime,
                    'arriveTime': arriveTime,
                    'duration': duration
                }

            except NoSuchElementException:
                # Some sort of error occurred! Either the address is malformed,
                # or the server is having some sort of issue. We'll wait a little bit
                # and try again
                if attempts < self.max_attempts:
                    attempts += 1
                    # Wait 1 seconds before trying again
                    time.sleep(retry_wait)
                    print "Failed to parse the address. Trying again. Attempt #", attempts
                    continue
                else:
                    return None