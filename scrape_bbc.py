"""
Python Wind Computation tool
Copyright (C) 2017  Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# coding: utf-8
#!/usr/bin/env python

# import the library used to query a website
import urllib2
# import the Beautiful soup functions to parse
# the data returned from the website
from bs4 import BeautifulSoup
import sys


class BBCScraper:

    loc_id = None

    reading = []

    day = None

    location_name = None

    def __init__(self):
        """
        No implemented
        """
        pass

    def set_location_id(self, loc_id):
        """
        The BBC weather operates based on ID system where each location contain
        its unique ID.

        The method allows to set the location ID

        """
        self.loc_id = loc_id
        self.create_soup()

    def set_day(self, d):
        """
        The bbc allows to set the day with a GET variable ?day=
        the method allows to select particular day

        :param d: day to select (0-6)
        """
        if 0 <= d <= 6:
            self.day = d
        else:
            print("Invalid day, the day can be INT between 0-6")

    def fetch_forecast(self, soup):
        """
        :param soup: objec including the website data ready for extractions
        :return: void
        """

        # Get the time of the day
        hour = soup.find_all("span", class_="hour")

        # Get the corresponding temperature
        class_ = "units-value temperature-value temperature-value-unit-c"
        temperature = soup.find_all("span", class_)

        # Get the corresponding humidity
        humidity = soup.find_all("tr", class_="humidity")
        humidity = humidity[0].find_all('td', class_="value hours-1")

        # Get the corresponding wind speed
        class_ = "units-value windspeed-value windspeed-value-unit-kph"
        wind = soup.find_all('span', class_)

        class_ = "location-name"
        self.location_name = soup.find('span', class_).get_text()

        data = []

        for n in range(len(hour)):

            # Scrap the hour of the day
            _hour = int(hour[n].get_text())

            # Scrap the temperature
            _temperature = temperature[n].get_text()
            _temperature = float(_temperature.encode('utf-8').replace("°C", ""))
            # Scrap the Humidity
            _humidity = humidity[n].get_text()
            _humidity = _humidity.strip().encode('utf-8').replace("%", "")
            # Scrap the wind speed
            _wind = wind[n].get_text().encode("utf-8").replace(" km/h", "")

            _insert = [_hour, _temperature, float(_humidity), float(_wind)]
            data.append(_insert)

            # Debug print
            # print(data)

        return data

    def create_soup(self):
        """
        Build the URL for the web scraping

        :param:  void
        :return: void
        """

        # default day is the first
        if self.day is None:
            self.day = 0

        # URL to fetch the weather data from
        url = "http://www.bbc.co.uk/weather/{}?day={}"
        url = url.format(str(self.loc_id), str(self.day))
        print url  # Debug the URL

        try:
            # Fetch the page for scraping
            page = urllib2.urlopen(url)
            # Object containing the website ready for scrapping
            self.reading = self.fetch_forecast(BeautifulSoup(page, "lxml"))
        except urllib2.URLError:
            print("No internet connection")
            sys.exit()

    def get_data(self):
        """
        return the modelled extracted data from the website
        for further use

        :return: list with the data
        """
        return self.reading

    def get_location_name(self):
        """
        Get location for the weather data

        :return: location name
        """
        return self.location_name
