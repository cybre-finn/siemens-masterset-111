# SIP Software for the Siemens Masterset 111

[Based on hnesland's work](https://github.com/hnesland/aselektriskbureau) I revitalized a Siemens Masterset 111 with a Rotary Dial. The Phone speaks voip (SIP) now and uses the Raspberry Pi Zero W's Wifi capability for remote Internet access.
It works over an USB 5V jack (and therefore with a power bank).

## Hardware
* Masterset 111
* Raspberry Pi Zeroi W
* Voltage Regulator from Aliexpress with microUSB jack soldered on it
* Step-up converter from aliexpress (for the bells, running with 60V alternating current)
* H bridge from Aliexpress (bunch of transistors in an IC, used to generate discrete alternating current)

## Software
* python
* wrapper around linphone
* removed the webserver
* rebuilt the Rotary Input algorithm
* PWM for the H bridge

[Instructions will follow...]

## Images
![img_20181030_015621](https://user-images.githubusercontent.com/20602537/47710689-b3a24880-dc33-11e8-867e-719c4c82b0e0.jpg)
![img_20181030_015801](https://user-images.githubusercontent.com/20602537/47710690-b3a24880-dc33-11e8-9f04-9c47cc0a335e.jpg)
![img_20181030_015921](https://user-images.githubusercontent.com/20602537/47710692-b3a24880-dc33-11e8-8630-ab7a18492de9.jpg)
![img_20181030_020826](https://user-images.githubusercontent.com/20602537/47710694-b3a24880-dc33-11e8-8215-7097cb5790c7.jpg)
![img_20181030_020858](https://user-images.githubusercontent.com/20602537/47710696-b43adf00-dc33-11e8-839a-c810a3492af2.jpg)
