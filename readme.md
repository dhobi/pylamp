# PyLamp Potion

Small hobby project with the aim to control a
 [LED Potion Desk Lamp](https://www.youtube.com/watch?v=4nb1QUmxPlc) 
 from [ThinkGeek, Inc.](https://www.thinkgeek.com)
 with:
 - Infrared Remote Control
 - Web interface / REST / websocket
 - Homekit
 
 ...because the lamp was not geeky enough.

 Can / Should be used as a build status lamp. Works nicely together with Jenkins Websocket.in Notification Plugin.
 
You will not find a How-To or other install instructions here. Just sample code and sample config files.
Take over what you need, have fun.

![Screenshot of web interface](screenshot.png)

## Hardware Ingredients

- Potion Lamp (https://www.youtube.com/watch?v=4nb1QUmxPlc)
- LED - RGB Clear (https://www.sparkfun.com/products/105)
- IR Receiver Diode - TSOP38238 (https://www.sparkfun.com/products/10266)
- Infrared Remote Control (https://www.sparkfun.com/products/14865)

## Software Ingredients
- Python 2.7 (might work on lower / higher versions as well)
- lircd (see sparkfun.lircd.conf)
- pigpiod
- Python libraries
  - twisted & autobahn (webserver)
  - lirc (Remote control reader)
  - pigpio (faster/hw pwm)
- Web interface
  - jQuery
  - spectrum
- Homekit / HAP-NodeJS plugins
  - homebridge-http-rgb-bulb (see homekit.config.json)