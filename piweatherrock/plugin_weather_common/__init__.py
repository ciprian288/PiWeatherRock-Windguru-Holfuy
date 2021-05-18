# -*- coding: utf-8 -*-
# Copyright (c) 2014 Jim Kemp <kemp.jim@gmail.com>
# Copyright (c) 2017 Gene Liverman <gene@technicalissues.us>
# Distributed under the MIT License (https://opensource.org/licenses/MIT)

import datetime
import pygame
import time
from os import path


UNICODE_DEGREE = u'\xb0'
font_name = "dejavusans"
font_clock = "digital7"

import netifaces
netifaces.gateways()
iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

class PluginWeatherCommon:
    """
    This plugin is resposible for displaying the information on the top
    half of the screen when either the daily or hourly forecast is being
    displayed on the lower half. Both 'plugin_weather_daily' and
    'plugin_weather_hourly' call display_weather_top() to do this.

    This plugin also provides the display_subwindow() function that is used
    by 'plugin_weather_daily' and 'plugin_weather_hourly'.
    """

    def __init__(self, weather_rock):
        self.screen = None
        self.weather = None
        self.wind = None
        self.config = None        
        self.xmax = None
        self.ymax = None
        self.time_date_small_text_height = None
        self.time_date_text_height = None
        self.time_date_y_position = None
        self.time_date_small_y_position = None
        self.subwindow_text_height = None
        self.icon_size = None
 
        self.get_rock_values(weather_rock)

    def get_rock_values(self, weather_rock):
        self.screen = weather_rock.screen
        self.weather = weather_rock.weather
        self.wind = weather_rock.wind

        self.config = weather_rock.config        
        self.xmax = weather_rock.xmax
        self.ymax = weather_rock.ymax
        self.time_date_small_text_height = weather_rock.time_date_small_text_height
        self.time_date_text_height = weather_rock.time_date_text_height
        self.time_date_y_position = weather_rock.time_date_y_position
        self.time_date_small_y_position = weather_rock.time_date_small_y_position
        self.subwindow_text_height = weather_rock.subwindow_text_height
        self.icon_size = weather_rock.icon_size

    def disp_weather_top(self, weather_rock):
        self.get_rock_values(weather_rock)

        # Fill the screen with black
        self.screen.fill((0, 0, 0))
        xmin = 1
        lines = 5
        line_color = (0, 0, 0)
        text_color = (255, 255, 255)
        #font_name = "freesans"
        
        self.disp_time_date(font_name, text_color)
        self.disp_current_temp(font_name, text_color)
        if self.config["12hour_disp"]:
            self.display_clock_line('', time.strftime("%I:%M.%p", time.localtime()), False)
        else:
            self.display_clock_line('', time.strftime("%H:%M", time.localtime()), False)

    def disp_time_date(self, font_name, text_color):
        # Time & Date
        time_date_font = pygame.font.SysFont(
            font_name, int(self.ymax * self.time_date_text_height), bold=1)
        # Small Font for Seconds
        small_font = pygame.font.SysFont(
            font_name,
            int(self.ymax * self.time_date_small_text_height), bold=1)

        if self.config["12hour_disp"]:
            time_string = time.strftime("%A - %b %d", time.localtime())
            am_pm_string = ""
        else:
            time_string = time.strftime("%A - %d %B", time.localtime())
            am_pm_string = ""

        rendered_time_string = time_date_font.render(time_string.capitalize(), True,
                                                     (255, 182, 32))
        (rendered_time_x, rendered_time_y) = rendered_time_string.get_size()
        rendered_am_pm_string = small_font.render(am_pm_string, True,
                                                  text_color)
        (rendered_am_pm_x, rendered_am_pm_y) = rendered_am_pm_string.get_size()

        full_time_string_x_position = self.xmax / 2 - (rendered_time_x +
                                                       rendered_am_pm_x) / 2
        self.screen.blit(rendered_time_string, (full_time_string_x_position,
                                                self.time_date_y_position))
        self.screen.blit(rendered_am_pm_string,
                         (full_time_string_x_position + rendered_time_x + 3,
                          self.time_date_small_y_position))

    def disp_current_temp(self, font_name, text_color):        

        # Outside Temp
        if 'error' in self.wind.values() or 'error' in self.wind:
            outside_temp_font = pygame.font.SysFont(
                font_name, int(self.ymax * 0.25), bold=1)
            txt = outside_temp_font.render(
                str(int(round(self.weather['hourly'][0]['temp']))), True, text_color)            
        
        # wind Temp 
        else:            
            outside_temp_font = pygame.font.SysFont(
                font_name, int(self.ymax * 0.25), bold=1)
            txt = outside_temp_font.render(
                str(int(round(self.wind['temperature']))), True, text_color)
        
        (txt_x, txt_y) = txt.get_size()
        degree_font = pygame.font.SysFont(
            font_name, int(self.ymax * 0.25), bold=1)
        degree_txt = degree_font.render(UNICODE_DEGREE, True, text_color)
        (rendered_am_pm_x, rendered_am_pm_y) = degree_txt.get_size()
        degree_letter = outside_temp_font.render(
            self.get_temperature_letter(self.config["units"]),
            True, text_color)
        (degree_letter_x, degree_letter_y) = degree_letter.get_size()    
        # Position text
        x = self.xmax * 0.23 - (txt_x * 1.02 + rendered_am_pm_x +
                                degree_letter_x) / 2
        self.screen.blit(txt, (x, self.ymax * 0.21))
        x = x + txt_x
        self.screen.blit(degree_txt, (x, self.ymax * 0.21))
        x = x + (rendered_am_pm_x * 0.8)
        self.screen.blit(degree_letter, (x, self.ymax * 0.21))

    
    
    def display_clock_line(self, label, cond, is_temp, multiplier=None): 
        if self.config["12hour_disp"]:
            conditions_text_height = 0.24            # text hight for clock
            y_start_position = 0.34                  # y position clock
            second_column_x_start_position = 0.7     # x position clock
        else:
            conditions_text_height = 0.36            # text hight for clock
            y_start_position = 0.32                  # y position clock
            second_column_x_start_position = 0.7     # x position clock
        
        line_spacing_gap = 0.065
        degree_symbol_height = 0.1
        degree_symbol_y_offset = 0.001
        x_start_position = 0.35        
        #font_name = "freesans"

        if multiplier is None:
            y_start = y_start_position
        else:
            y_start = (y_start_position + line_spacing_gap * multiplier)
        
        
        if 'error' in self.wind.values() or 'error' in self.wind:
            text_color = (51, 187, 255)
        
        elif self.config["holfuy_api_key"] == "null":
            if 0 <= self.wind['wind_max'] <= 16:
                text_color = (51, 187, 255)
            if 16.1 < self.wind['wind_max'] <= 20:
                text_color = (97, 209, 97)
            if 20.1 < self.wind['wind_max'] <= 24:
                text_color = (255, 182, 32)
            if 24.1 < self.wind['wind_max'] <= 30:
                text_color = (255, 102, 0)
            if 30.1 < self.wind['wind_max'] <= 500:
                text_color = (255, 26, 140)  
            
        else:
            if 0 <= self.wind['wind']['gust'] <= 16:
                text_color = (51, 187, 255)
            if 16.1 < self.wind['wind']['gust'] <= 20:
                text_color = (97, 209, 97)
            if 20.1 < self.wind['wind']['gust'] <= 24:
                text_color = (255, 182, 32)
            if 24.1 < self.wind['wind']['gust'] <= 30:
                text_color = (255, 102, 0)
            if 30.1 < self.wind['wind']['gust'] <= 500:
                text_color = (255, 26, 140)    

        conditions_font = pygame.font.SysFont(font_clock, int(self.ymax * conditions_text_height), bold=1)
        small_font = pygame.font.SysFont(font_name, 15, bold=1)

        ip_text = small_font.render("IP " + str(ip) + ":8888", True, (128, 128, 128))
        ip_text_render = pygame.transform.rotate(ip_text, 90)
        ip_text_rect = ip_text_render.get_rect(center=(10, self.ymax * 0.25))
        self.screen.blit(ip_text_render, ip_text_rect)

        txt = conditions_font.render(str(cond), True, text_color)
        txt_rect = txt.get_rect(center=(self.xmax * second_column_x_start_position, self.ymax * y_start))
        self.screen.blit(txt, txt_rect)

    def get_temperature_letter(self, unit):
        """
        Determines the single letter that represents temperature based on
        unit a user has chosen. ex: 'F' to represent 'Degrees Fahrenheit'
        """
        return self.units_decoder(unit)['temperature'].split(' ')[-1][0].upper()

    def get_abbreviation(self, phrase):
        """
        Create an abbreviation from a phrase by combining the first letter
        of each word in lower case.
        """
        abbreviation = ''.join(item[0].lower() for item in phrase.split())
        return abbreviation

    def units_decoder(self, units):
 
        metric_dict = {            
            'temperature': 'Degrees Celsius',
            'temperatureMin': 'Degrees Celsius',
            'temperatureMax': 'Degrees Celsius',            
        }
        imperial_dict = {            
            'temperature': 'Degrees Fahrenheit',
            'temperatureMin': 'Degrees Fahrenheit',
            'temperatureMax': 'Degrees Fahrenheit',
        }
        standard_dict = {            
            'temperature': 'Degrees Kelvin ',
            'temperatureMin': 'Degrees Kelvin ',
            'temperatureMax': 'Degrees Kelvin ',
        }        
        switcher = {
            'standard': standard_dict,
            'imperial': imperial_dict,
            'metric': metric_dict,
        }
        return switcher.get(units, "Invalid unit name")

    #######################################################################
    #    Everything above here is used exclusively by disp_weather_top    #
    #######################################################################

    # pt meteo zilnic
    def display_subwindow_daily(self, data, day, c_times, index):
        subwindow_centers = 0.125
        subwindows_y_start_position = 0.530
        line_spacing_gap = 0.065
        rain_percent_line_offset = 5.95
        rain_present_text_height = 0.048
        text_color = (255, 255, 255)
        #font_name = "freesans"

        forecast_font = pygame.font.SysFont(
            font_name, int(self.ymax * self.subwindow_text_height), bold=1)
        rpfont = pygame.font.SysFont(
            font_name, int(self.ymax * rain_present_text_height), bold=1)

        txt = forecast_font.render(day, True, text_color)
        (txt_x, txt_y) = txt.get_size()
        self.screen.blit(txt, (self.xmax *
                               (subwindow_centers * c_times) - txt_x / 2,
                               self.ymax * (subwindows_y_start_position +
                                            line_spacing_gap * 0)))
                           
        txt = forecast_font.render(
            str(int(round(self.weather['daily'][index]['temp']['min']))) +
            UNICODE_DEGREE +
            ' / ' +
            str(int(round(self.weather['daily'][index]['temp']['max']))) +
            UNICODE_DEGREE + self.get_temperature_letter(
                self.config["units"]),
            True, text_color)
        rptxt = rpfont.render(str(int(round(self.weather['daily'][index]['pop'] * 100))) + '%',
            True, text_color)
    
        (txt_x, txt_y) = txt.get_size()
        self.screen.blit(txt, (self.xmax *
                               (subwindow_centers * c_times) - txt_x / 2,
                               self.ymax * (subwindows_y_start_position +
                                            line_spacing_gap * 5)))
        
        (txt_x, txt_y) = rptxt.get_size()
        self.screen.blit(rptxt, (self.xmax *
                                 (subwindow_centers * c_times) - txt_x / 2,
                                 self.ymax * (subwindows_y_start_position +
                                              line_spacing_gap *
                                              rain_percent_line_offset)))
        

        icon_forecast = self.weather['daily'][index]['weather'][0]['icon']
        icon = pygame.image.load(
            self.icon_mapping(icon_forecast, self.icon_size)).convert_alpha()        
        (icon_size_x, icon_size_y) = icon.get_size()        
        if icon_size_y < 90:
            icon_y_offset = (90 - icon_size_y) / 2
        else:
            icon_y_offset = self.config["icon_offset"]

        self.screen.blit(icon, (self.xmax *
                            (subwindow_centers * c_times) -
                            icon_size_x / 2,
                            self.ymax *
                            (subwindows_y_start_position +
                             line_spacing_gap
                             * 1.2) + icon_y_offset))

    def display_subwindow_hourly(self, data, day, c_times, index):
        subwindow_centers = 0.125
        subwindows_y_start_position = 0.530
        line_spacing_gap = 0.065
        rain_percent_line_offset = 5.95
        rain_present_text_height = 0.048
        text_color = (255, 255, 255)
        #font_name = "freesans"

        forecast_font = pygame.font.SysFont(
            font_name, int(self.ymax * self.subwindow_text_height), bold=1)
        rpfont = pygame.font.SysFont(
            font_name, int(self.ymax * rain_present_text_height), bold=1)

        txt = forecast_font.render(day, True, text_color)
        (txt_x, txt_y) = txt.get_size()
        self.screen.blit(txt, (self.xmax *
                               (subwindow_centers * c_times) - txt_x / 2,
                               self.ymax * (subwindows_y_start_position +
                                            line_spacing_gap * 0)))
        
        txt = forecast_font.render(
            str(int(round(self.weather['hourly'][index]['temp']))) +
            UNICODE_DEGREE + self.get_temperature_letter(
                self.config["units"]),
            True, text_color)
        rptxt = rpfont.render(str(int(round(self.weather['hourly'][index]['pop'] * 100))) + '%',
            True, text_color)
        (txt_x, txt_y) = txt.get_size()
        self.screen.blit(txt, (self.xmax *
                           (subwindow_centers * c_times) - txt_x / 2,
                           self.ymax * (subwindows_y_start_position +
                                        line_spacing_gap * 5)))
    
        (txt_x, txt_y) = rptxt.get_size()
        self.screen.blit(rptxt, (self.xmax *
                             (subwindow_centers * c_times) - txt_x / 2,
                             self.ymax * (subwindows_y_start_position +
                                          line_spacing_gap *
                                          rain_percent_line_offset)))
        
        icon_forecast = self.weather['hourly'][index]['weather'][0]['icon']
        icon = pygame.image.load(self.icon_mapping(icon_forecast, self.icon_size)).convert_alpha()
        (icon_size_x, icon_size_y) = icon.get_size()        
        if icon_size_y < 90:
            icon_y_offset = (90 - icon_size_y) / 2
        else:
            icon_y_offset = self.config["icon_offset"]

        self.screen.blit(icon, (self.xmax *
                            (subwindow_centers * c_times) -
                            icon_size_x / 2,
                            self.ymax *
                            (subwindows_y_start_position +
                             line_spacing_gap
                             * 1.2) + icon_y_offset))
    
    def icon_mapping(self, icon_forecast, size):        
        
        if icon_forecast == '01d':
            icon_path = 'icons/{}/clear.png'.format(size)
        if icon_forecast == '01n':
            icon_path = 'icons/{}/nt_clear.png'.format(size)

        if icon_forecast == '02d':
            icon_path = 'icons/{}/mostlysunny.png'.format(size)
        if icon_forecast == '02n':
            icon_path = 'icons/{}/nt_mostlysunny.png'.format(size)
        
        if icon_forecast == '03d':
            icon_path = 'icons/{}/cloudy.png'.format(size)
        if icon_forecast == '03n':
            icon_path = 'icons/{}/nt_cloudy.png'.format(size)
        
        if icon_forecast == '04d':
            icon_path = 'icons/{}/mostlycloudy.png'.format(size)
        if icon_forecast == '04n':
            icon_path = 'icons/{}/nt_mostlycloudy.png'.format(size)
        
        if icon_forecast == '09d':
            icon_path = 'icons/{}/chancerain.png'.format(size)
        if icon_forecast == '09n':
            icon_path = 'icons/{}/nt_chancerain.png'.format(size)
        
        if icon_forecast == '10d':
            icon_path = 'icons/{}/rain.png'.format(size)
        if icon_forecast == '10n':
            icon_path = 'icons/{}/nt_rain.png'.format(size)
        
        if icon_forecast == '11d':
            icon_path = 'icons/{}/chancetstorms.png'.format(size)
        if icon_forecast == '11n':
            icon_path = 'icons/{}/nt_chancetstorms.png'.format(size)
        
        if icon_forecast == '13d':
            icon_path = 'icons/{}/snow.png'.format(size)
        if icon_forecast == '13n':
            icon_path = 'icons/{}/nt_snow.png'.format(size)
        
        if icon_forecast == '50d':
            icon_path = 'icons/{}/fog.png'.format(size)
        if icon_forecast == '50n':
            icon_path = 'icons/{}/nt_fog.png'.format(size)       
       

        return path.join(path.dirname(__file__), icon_path)

