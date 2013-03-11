from django.conf import settings

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

import logging
logger = logging.getLogger("applog")

"""
Collects various data from a realestate.com.au
search
"""
class CollectData:

    """
    @browser:
        A selenium browser object

    @search_string:
        The real-estate string to begin searching with.
        This can be found on realestate.com.au/buy/ and
        entering some form of search. The string is
        everything succeeding /buy/

    @max_pages: 
        The amount of pages to do before
        ending the search. All pages will be searched
        if 0. Up to or under for any other number.
    """
    current_page = 0

    def __init__(self, browser, search_string="", max_pages=0):
        self.browser = browser
        self.search_string = "/buy/" + search_string
        self.max_pages = max_pages

    """
    Retrieves all addresses with basic data and returns
    it as an array of dicts
    """
    def get(self):
        addresses = []

        startUrl = settings.REAL_ESTATE_URL + self.search_string

        # Open page with search string
        self.browser.get(startUrl)
        logger.debug("... current url: ..." + startUrl[-100:])
        # Scan current page (if values exist)
        addresses += self._scanPage(startUrl)

        # Continue scanning until there is no 'next' button
        while(True):

            self.current_page += 1

            # Exit loop if we exceed our max pages
            if self.max_pages != 0 and self.current_page >= self.max_pages:
                break

            # Check for next button
            try:
                nextBtn = self.browser.find_element_by_class_name("nextLink")
                nextBtn.click()
                logger.debug("... current url: ..." + self.browser.current_url[-100:])
                addresses += self._scanPage(self.browser.current_url)
            except NoSuchElementException:
                break

        return addresses

    """
    Scans a realestate page and returns all bodies of
    detail found
    """
    def _scanPage(self, currentUrl):

        addresses = []

        source = BeautifulSoup(
            self.browser.find_element_by_id("searchResultsTbl").get_attribute("innerHTML"))
        resultBodies = source.findAll("div", class_="resultBody")
        
        for resultBody in resultBodies:
            address = self._scanBody(resultBody)

            if (address):
                addresses.append(address)

        return addresses


    """
    Scans a single realestate detail body and returns
    a basic list of details

    @body:
        A selenium result from a div containg the class "resultBody"
    """
    def _scanBody(self, body):
        address = body.find("a", class_="name").getText()

        # Ignore 'address on request' results and units
        # TODO: Make units searchable... Maybe change this to a regex
        banned = ["request", "available", "/", "-", "Lot", "&"]
        for ban in banned:
            if ban.lower() in address.lower():
                return None

        title = body.find("h3", class_="title").getText()

        if body.find("p", class_="price") != None:
            price = body.find("p", class_="price").find("span").getText()
        else: 
            # This is probably a whole bunch of plots of land that aren't
            # built yet, and I don't care about these. Pass.
            return None

        url = body.find("a", class_="name")["href"]

        try:
            features = body.find("ul", class_="propertyFeatures").findAll('li')
        except AttributeError:
            return None

        # Usualy this means it's a business... Should at least have
        # bedroom and bathroom, right?
        if len(features) < 2:
            return None

        bedrooms = int(features[0].span.getText())
        bathrooms = int(features[1].span.getText())
        if len(features) >= 3:
            carspaces = int(features[2].span.getText())
        else:
            carspaces = 0

        data = {
            'address': address,
            'title': title,
            'price': price,
            'url': url,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'carspaces': carspaces
        }

        return data