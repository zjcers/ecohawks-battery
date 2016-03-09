Prius Battery Control System
============================
Project Goal
------------
This project aims to test the feasibility of using nearly-depleted batteries from hybrid/electric vehicles as the basis for distributed grid storage.
Hardware
--------
All of the controlling logic will run on a RaspberryPi 2 connected to two current sensors (Texas Instruments INA219), one of which also measures pack voltage. Since the power to charge to battery pack will come from solar panels that the project cannot directly interface with, a luminosity sensor on the roof (TAOS TS2561) connected to the Pi over wifi using an Expressif ESP8266 running the Arduino framework.
Parts of the Project (Codewise)
-------------------------------
### Control Logic
This is implemented in Python2.x, but may eventually be ported to 3.x. Care has been taken to make the design as modular as possible. Threading is used to ensure the main thread is not blocked by sensor access.
### Device Drivers
More Python. All of the sensor drivers are implementations of the abstract sensor.Sensor class to emulate interfaces.
### ESP8266 bits
The only non-Python part of the project, so far. This is really simple since the only job of the ESP8266 is to read the luminosity sensor and report back the Pi.
