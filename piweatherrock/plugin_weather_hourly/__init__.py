# -*- coding: utf-8 -*-
# Copyright (c) 2014 Jim Kemp <kemp.jim@gmail.com>
# Copyright (c) 2017 Gene Liverman <gene@technicalissues.us>
# Distributed under the MIT License (https://opensource.org/licenses/MIT)

import datetime
import pygame

from piweatherrock.plugin_weather_common import PluginWeatherCommon


class PluginWeatherHourly:
    """
    This plugin is resposible for displaying the screen with the hourly
    forecast.
    """

    def __init__(self, weather_rock):
        self.config = None
        self.screen = None
        self.weather = None
        self.weather_common = None

    def get_rock_values(self, weather_rock):
        self.config = weather_rock.config
        self.screen = weather_rock.screen
        self.weather = weather_rock.weather
        self.weather_common = PluginWeatherCommon(weather_rock)

    def disp_hourly(self, weather_rock):
        self.get_rock_values(weather_rock)

        self.weather_common.disp_weather_top(weather_rock)

        # Current hour
        this_hour = self.weather['hourly'][0]['dt']
        this_hour_24_int = int(datetime.datetime.fromtimestamp(
            this_hour).strftime("%H"))
        if this_hour_24_int <= 11:
            ampm = 'a.m.'
        else:
            ampm = 'p.m.'
        this_hour_12_int = int(datetime.datetime.fromtimestamp(
            this_hour).strftime("%I"))
        if self.config["12hour_disp"]:
            this_hour_string = "{} {}".format(str(this_hour_12_int), ampm)
        else:
            this_hour_string = "{} {}".format(str(this_hour_24_int), "Std")
        multiplier = 1
        self.weather_common.display_subwindow_hourly(this_hour, this_hour_string, multiplier, 0)

       
        # counts from 0 to 2
        for i in range(3):
            this_hour = self.weather['hourly'][i + 1]['dt']
            this_hour_24_int = int(datetime.datetime.fromtimestamp(
                this_hour).strftime("%H"))
            if this_hour_24_int <= 11:
                ampm = 'a.m.'
            else:
                ampm = 'p.m.'
            this_hour_12_int = int(datetime.datetime.fromtimestamp(
                this_hour).strftime("%I"))
            if self.config["12hour_disp"]:
                this_hour_string = "{} {}".format(str(this_hour_12_int), ampm)
            else:
                this_hour_string = "{} {}".format(str(this_hour_24_int), "Std")
            multiplier += 2
            self.weather_common.display_subwindow_hourly(this_hour, this_hour_string, multiplier, i + 1)

        # Update the display
        pygame.display.update()
