#Intro

This example shows how make live chart in web-browser with accelerometer readings from MPU-6050 breakout board connected to Raspberry PI.

![Live chart](http://freakone.pl/content/charts.png)
![Raspberry PI setup](http://freakone.pl/content/raspi.jpg)

#Hardware requirements

Connect pins from accelerometer board directly to RPi pins in order shown below.

RPi | MPU-6050
:---: | :---:
1 (3V3) | 1 (VCC)
3 (SDA) | 4 (SDA)
5 (SCL) | 3 (SCL)
9 (GND) | 2 (GND)

#Software requirements
* i2c interface enabled, for instructions go [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)
* i2c-tools - for finding accelerometer addess (optional)
* python, python-dev and python-smbus
* python packages installed from pip: bottle, gevent-websocket

#Installation
* clone this repo
* edit index.html, line 56
* run `websockets_accelerometer.py`
* go to `raspi_address:8080`

