import time

from django.conf import settings

from bs4 import BeautifulSoup

import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys


"""
Functions for retrieving information from adsl2exchanges.com.au
"""
class ADSL2:

    """
    @max_attempts:
        Amount of attempts that can be made when trying to retrieve
        data from the adsl2exchanges.com.au page
    """
    def __init__(self, max_attempts=2):
        self.max_attempts = max_attempts

    """
    Get line distance and possible speed for an address from 
    adsl2exchanges.com.au

    @address:
        The address to check against in the form of
        a string

    @browser:
        A selenium browser object

    @retry_wait:
        The amount of time in seconds before retrying an address
    """
    def get(self, address, browser, retry_wait=1):
        attempts = 0
        wait = ui.WebDriverWait(browser, 3)

        while (True):
            browser.get(settings.ADSL_URL)
            form = browser.find_elements_by_tag_name("form")[2]
            form_address = form.find_element_by_name("Address")
            form_address.send_keys(address + Keys.RETURN)

            try:
                try:
                    wait.until(lambda browser: browser.find_element_by_id("map").get_attribute("innerHTML").strip() != "")
                except TimeoutException:
                    pass

                adsl_source = BeautifulSoup(browser.find_element_by_id("map").get_attribute("innerHTML"))
                divs = [x for x in adsl_source.findAll("div") if "Estimated" in x.getText()]
                adsldata = divs[len(divs) - 1]

                # TODO: Split this data up!
                return adsldata

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