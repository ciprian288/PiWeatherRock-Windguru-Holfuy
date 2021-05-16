# PiWeatherRock-Windguru-Holfuy
 Displays local weather and wind on a Raspberry Pi
 
| Daily forecast                                               | Hourly forecast                                        | Wind data   |
| ------------------------------------------------------------ | ------------------------------------------------------ | ----------- |
| ![screenshot1](screenshots/screenshot1.jpeg) |![screenshot2](screenshots/screenshot2.jpeg)| ![screenshot3](screenshots/screenshot3.jpeg) |             |

## Introduction

PiWeatherRock is an internet-connected weather station. Its purpose is to display local
weather and wind condtions. It was created with the goal of having a simple way to check 
the weather and wind before a nautical activity (kiting, windsurfing, sailing). 
The end result is a modern version of a weather rock.

* The build of this project originated with the code written by Gene Liverman and
  published at
  https://piweatherrock.technicalissues.us .
  
* Right now all data is pulled from:
     - OpenWetherMap  https://openweathermap.org/api/one-call-api
     - Windguru https://www.windguru.cz
     - Holfuy https://api.holfuy.com/

# Install requirements:

   ```sh
   sudo apt-get install python3
   ```
   ```sh
   sudo apt-get install python3-pip
   ```
   ```sh
   git clone https://github.com/ciprian288/PiWeatherRock-Windguru-Holfuy.git PiWeatherRockWind
   ```
   ```sh
   pip3 install -r ~/PiWeatherRockWind/requirements.txt
   ```   

# Scripts for autostart

* The xhost command needs an active X server to run, it can run at the login screen, for example when lightdm loads. You can enable it by editing /etc/lightdm/lightdm.conf and adding the line:    `xserver-command=X -s 0 -dpms`

   ```sh
   sudo cp ~/PiWeatherRockWind/scripts/{PiWeatherRock.service,PiWeatherRockConfig.service} /etc/systemd/system/
   ```
   ```sh
   sudo systemctl enable PiWeatherRockConfig.service
   ```
   ```sh
   sudo systemctl enable PiWeatherRock.service
   ```
   ```sh
   sudo systemctl start PiWeatherRockConfig.service
   ```
   ```sh
   sudo systemctl start PiWeatherRock.service
   ```
* For instaling clock font:
   ```sh
   sudo cp -r ~/PiWeatherRockWind/fonts/digital.ttf /usr/share/fonts/truetype/digital.ttf
   ```
   ```sh
   fc-cache -f -v
   ```
* For your locale:
   ```sh
   locale -a   # find your locale
   ```
   ```sh
   sudo update-locale LC_TIME=xx_XX.UTF-8    # replace xx-XX with your locale 
   ```
   ```sh
   sudo reboot
   ```
   or
   ```sh
   sudo dpkg-reconfigure locales   # reconfigure all locales 
   ```
   ```sh
   sudo reboot
   ```
# Usage

* When PiWeatherRock starts, on the left side of the screen is your *RaspberryPi IP* (like: 10.0.2.15:8888 from screenshots) 
* Put in any web browser *RaspberryPi IP* . It provides a web interface for configuring PiWeatherRock
* Wave your mouse over the titles for instructions
```diff
- The "API Meteo" key MUST BE CHANGED because it is a TEST key 
```
* After `Update` your configuration restart PiWeatherRock.service with:

   ```sh
   sudo systemctl restart PiWeatherRock.service
   ```
* If the wind is set, the color of the watch and the wind data (blue, green, orange, brown, purple) changes according to the wind speed       

# To EXIT PiWeatherRock-Windguru-Holfuy -- press Q

