import datetime
import pygame
#import time
import requests
from os import path
import json

font_name = "dejavusans"

class PluginInfo:

    def __init__(self, weather_rock):
        self.config = None
        self.screen = None 
        self.wind = None
        self.last_update_check = None
        self.xmax = None
        self.ymax = None
        self.get_rock_values(weather_rock)

    def get_rock_values(self, weather_rock):
        self.config = weather_rock.config
        self.screen = weather_rock.screen        
        self.wind = weather_rock.wind
        self.last_update_check = weather_rock.last_update_check
        self.xmax = weather_rock.xmax
        self.ymax = weather_rock.ymax
        
    def deg_to_compass(self, degrees):
        val = int((degrees/22.5)+.5)
        dirs = ["N", "NNE", "NE", "ENE",
                "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW",
                "W", "WNW", "NW", "NNW"]
        return dirs[(val % 16)]

    def disp_info(self, weather_rock):
        self.get_rock_values(weather_rock)
        self.screen.fill((0, 0, 0))
        xmin = 10
        lines = 5
        line_color = (0, 0, 0)
        text_color = (255, 255, 255)
        #font_name = "digital7"

        if 0 <= self.xmax <= 780:
            icon_wind_size = '200'
        if 781 <= self.xmax <= 1024:
            icon_wind_size = '400'
        if 1025 <= self.xmax:
            icon_wind_size = '700'

        regular_font = pygame.font.SysFont(font_name, int(self.ymax * 0.16), bold=1)
        small_font = pygame.font.SysFont(font_name, int(self.ymax * 0.13), bold=1)
        error_font = pygame.font.SysFont(font_name, int(self.ymax * 0.05), bold=1)


        if 'error' in self.wind.values() or 'error' in self.wind:

            text = "ERROR"
            text_render = error_font.render(text, True, (255, 0, 0))
            text_rect = text_render.get_rect(center=(self.xmax * 0.5, self.ymax * 0.2))
            self.screen.blit(text_render, text_rect)

            text = "Wrong wind data in config.py ."
            text_render = error_font.render(text, True, (255, 0, 0))
            text_rect = text_render.get_rect(center=(self.xmax * 0.5, self.ymax * 0.4))
            self.screen.blit(text_render, text_rect)

            kite_path = path.join(path.dirname(__file__), 'icons/logo/{}/windguru.png'.format(icon_wind_size))
            kite = pygame.image.load(kite_path)
            self.screen.blit(kite, (self.xmax * 0.6, self.ymax * 0.72))
            
        
        elif self.config["holfuy_api_key"] == "null":
            wind_speed = self.wind['wind_avg']
            wind_gust = self.wind['wind_max']
            wind_dir = self.wind['wind_direction']

            if 0 <= wind_speed <= 14:
                text_regular = (51, 187, 255)
                icon_wind = path.join(path.dirname(__file__), 'icons/blue/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))
            if 14.1 < wind_speed <= 17:
                text_regular = (97, 209, 97)
                icon_wind = path.join(path.dirname(__file__), 'icons/green/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))
            if 17.1 < wind_speed <= 24:
                text_regular = (255, 182, 32)
                icon_wind = path.join(path.dirname(__file__), 'icons/orange/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))
            if 24.1 < wind_speed <= 30:
                text_regular = (255, 102, 0)
                icon_wind = path.join(path.dirname(__file__), 'icons/brown/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))
            if 30.1 < wind_speed <= 500:
                text_regular = (255, 26, 140)
                icon_wind = path.join(path.dirname(__file__), 'icons/purple/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))

            #text = "24.5 nd"
            text = ("{} knt").format(wind_speed)
            text_render = regular_font.render(text, True, text_regular)
            text_rect = text_render.get_rect(center=(self.xmax * 0.78, self.ymax * 0.18))
            self.screen.blit(text_render, text_rect)

            #text = "30.5 nd"
            text = ("{} knt").format(wind_gust)
            text_render = regular_font.render(text, True, text_regular)
            text_rect = text_render.get_rect(center=(self.xmax * 0.78, self.ymax * 0.37))
            self.screen.blit(text_render, text_rect)
            
            text = "%s° " % wind_dir
            text_render = small_font.render(text, True, text_color)
            text_rect = text_render.get_rect(center=(self.xmax * 0.78, self.ymax * 0.58))
            self.screen.blit(text_render, text_rect)
        
            icon_load = pygame.image.load(icon_wind).convert_alpha()
            self.screen.blit(icon_load, (self.xmax * 0.04, self.ymax * 0.08))
        
            kite_path = path.join(path.dirname(__file__), 'icons/logo/{}/windguru.png'.format(icon_wind_size))
            kite = pygame.image.load(kite_path)
            self.screen.blit(kite, (self.xmax * 0.6, self.ymax * 0.72))

        else:
            wind_speed = self.wind['wind']['speed']
            wind_gust = self.wind['wind']['gust']
            wind_dir = self.wind['wind']['direction']

            if 0 <= wind_speed <= 14:
                text_regular = (51, 187, 255)
                icon = path.join(path.dirname(__file__), 'icons/blue/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))
            if 14.1 < wind_speed <= 17:
                text_regular = (97, 209, 97)
                icon = path.join(path.dirname(__file__), 'icons/green/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))
            if 17.1 < wind_speed <= 24:
                text_regular = (255, 182, 32)
                icon = path.join(path.dirname(__file__), 'icons/orange/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))
            if 24.1 < wind_speed <= 30:
                text_regular = (255, 102, 0)
                icon = path.join(path.dirname(__file__), 'icons/brown/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))
            if 30.1 < wind_speed <= 500:
                text_regular = (255, 26, 140)
                icon = path.join(path.dirname(__file__), 'icons/purple/{}/{}.png'.format(icon_wind_size, self.deg_to_compass(wind_dir)))

            #text = "24.5 nd"
            text = ("{} knt").format(wind_speed)
            text_render = regular_font.render(text, True, text_regular)
            text_rect = text_render.get_rect(center=(self.xmax * 0.78, self.ymax * 0.18))
            self.screen.blit(text_render, text_rect)

            #text = "30.5 nd"
            text = ("{} knt").format(wind_gust)
            text_render = regular_font.render(text, True, text_regular)
            text_rect = text_render.get_rect(center=(self.xmax * 0.78, self.ymax * 0.37))
            self.screen.blit(text_render, text_rect)
            
            text = "%s° " % wind_dir
            text_render = small_font.render(text, True, text_color)
            text_rect = text_render.get_rect(center=(self.xmax * 0.78, self.ymax * 0.58))
            self.screen.blit(text_render, text_rect)
        
            icon_load = pygame.image.load(icon).convert_alpha()
            self.screen.blit(icon_load, (self.xmax * 0.04, self.ymax * 0.08))
        
            kite_path = path.join(path.dirname(__file__), 'icons/logo/{}/holfuy.png'.format(icon_wind_size))
            kite = pygame.image.load(kite_path)
            self.screen.blit(kite, (self.xmax * 0.6, self.ymax * 0.72))

        # Update the display
        pygame.display.update()

    def string_print(self, text, font, x, line_number, text_color):
        """
        Prints a line of text on the display
        """
        rendered_font = font.render(text, True, text_color)
        self.screen.blit(rendered_font, (x, self.ymax * 0.075 * line_number))

    def stot(self, sec):
        mins = sec.seconds // 60
        hrs = mins // 60
        return (hrs, mins % 60)




