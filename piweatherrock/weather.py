# -*- coding: utf-8 -*-
# Copyright (c) 2014 Jim Kemp <kemp.jim@gmail.com>
# Copyright (c) 2017 Gene Liverman <gene@technicalissues.us>
# Distributed under the MIT License (https://opensource.org/licenses/MIT)

# standard imports
import datetime
import os
import platform
import signal
import sys
import time
import json
import logging
import logging.handlers

# third party imports
import pygame
import requests

import locale
#now = datetime.datetime.now()
locale.setlocale(locale.LC_TIME, "")

url_holfuy = "http://api.holfuy.com/live/?s={s}&pw={pw}&&m=JSON&tu=C&su=knots&batt"
url_owm = "https://api.openweathermap.org/data/2.5/onecall?"

# globals
UNICODE_DEGREE = u'\xb0'

def exit_gracefully(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, exit_gracefully)


class Weather:
    """
    Fetches weather reports from Dark Sky for displaying on a screen.
    """

    def __init__(self, config_file):
        with open(config_file, "r") as f:
            self.config = json.load(f)

        self.last_update_check = 0
        self.weather = {}
        self.wind = {}
        self.get_forecast()
        
        if platform.system() == 'Darwin':
            pygame.display.init()
            driver = pygame.display.get_driver()
            print(f"Using the {driver} driver.")
        else:
            # Based on "Python GUI in Linux frame buffer"
            # http://www.karoltomala.com/blog/?p=679
            disp_no = os.getenv("DISPLAY")
            if disp_no:
                print(f"X Display = {disp_no}")

            # Check which frame buffer drivers are available
            # Start with fbcon since directfb hangs with composite output
            drivers = ['x11', 'fbcon', 'directfb', 'svgalib']
            found = False
            for driver in drivers:
                # Make sure that SDL_VIDEODRIVER is set
                if not os.getenv('SDL_VIDEODRIVER'):
                    os.putenv('SDL_VIDEODRIVER', driver)
                try:
                    pygame.display.init()
                except pygame.error:
                    print("Driver: {driver} failed.")
                    continue
                found = True
                break

            if not found:
                print("No suitable video driver found!")
        #size = (800,480)
        size = (pygame.display.Info().current_w,
                pygame.display.Info().current_h)
        
        self.sizing(size)

        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.mouse.set_visible(0)
        pygame.display.update()

        self.subwindow_text_height = 0.059 # text hight meteo daily
        self.time_date_text_height = 0.13 # text hight data 
        self.time_date_small_text_height = 0.072 # text hight wind
        self.time_date_y_position = 8
        self.time_date_small_y_position = 18

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def sizing(self, size):
        """
        Set various asplect of the app related to the screen size of
        the display and/or window.
        """

        print(f"Framebuffer Size: {size[0]} x {size[1]}")

        if self.config["fullscreen"]:
            self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
            self.xmax = pygame.display.Info().current_w -5 #  - 35 Why not use full screen in "fullescreen"?
            self.ymax = pygame.display.Info().current_h #  - 5 Why not use full screen in "fullescreen"?
        else:
            self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            pygame.display.set_caption('PiWeatherRock')
            self.xmax = pygame.display.get_surface().get_width() - 15
            self.ymax = pygame.display.get_surface().get_height() - 5           

        if 0 <= self.xmax <= 780:
            self.icon_size = '64'
        if 781 <= self.xmax <= 1024:
            self.icon_size = '128'
        if 1025 <= self.xmax:
            self.icon_size = '256'
            
    def get_forecast(self):
        """
        Gets updated information if the 'update_freq' amount of time has
        passed since last querying the api.
        """
        if (time.time() - self.last_update_check) > self.config["update_freq"]:
            self.last_update_check = time.time()
            try:
                querystring_owm = {
                "lat": self.config["lat"],
                "lon": self.config["lon"],
                "units": self.config["units"],
                "apikey": self.config["ds_api_key"],
                "exclude": "minutely"                
                }
                self.weather = requests.request("GET", url_owm, params=querystring_owm).json()

                if self.config["holfuy_api_key"] == "null":
                    url = 'https://www.windguru.cz/int/iapi.php?q=station_data_current&id_station={s}&date_format=Y-m-d%20H%3Ai%3As%20T&_mha=f4d18b6c'.format(s=self.config["id_station"])
                    url_h = 'https://www.windguru.cz/station/{s}'.format(s=self.config["id_station"])
                    headers = {'Referer' : url_h}
                    self.wind = requests.get(url, headers = headers).json()
                else:
                    querystring_h = {
                    "s": self.config["id_station"],
                    "pw": self.config["holfuy_api_key"]
                    }
                    self.wind = requests.request("GET", url_holfuy, params=querystring_h).json()                

            except requests.exceptions.RequestException as e:
                print(f"Request exception: {e}")
                return False
            except AttributeError as e:
                print(f"Attribute error: {e}")
                return False
        return True

    def screen_cap(self):
        """
        Save a jpg image of the screen
        """
        pygame.image.save(self.screen, "screenshot.jpeg")
        print("Screen capture complete.")

