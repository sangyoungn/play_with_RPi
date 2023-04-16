# led_control

## About
This example demonstrates the GPIO output control using the RPi.GPIO module.

## Prerequisite
* Hardware
    * Raspberry Pi - Tested on RPi 4 Model B, which is preferred. But this should work on any RPi.
    * 2x LEDs - The coloer doesn't matter.
    * 2x Registers - 100 or 1000 ohm
* Software
    * Python 3 as is on Raspbery Pi OS

## Set Up
Refer to<br /> https://neighborhoodunclelab.tistory.com/entry/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC-%ED%8C%8C%EC%9D%B4Raspberry-Pi%EC%97%90%EC%84%9C-RPiGPIO-Python-module%EC%9D%84-%EC%82%AC%EC%9A%A9%ED%95%9C-GPIO-%EC%B6%9C%EB%A0%A5-%EC%A0%9C%EC%96%B4-%EA%B7%B8%EB%A6%AC%EA%B3%A0-Drive-Strength%EC%97%90-%EB%8C%80%ED%95%98%EC%97%AC <br />where further description can be found. (*Korean*)

## How to run
Clone the repository.
```bash
# You can bypass follow 2 commands if you already have cloned.
git clone https://github.com/sangyoungn/play_with_RPi.git
cd led_control
```
Run the script.
```bash
python led_toggle.py
```
Press *Ctrl+C* to exit.

## What to learn from this
* GPIO output control using Python **RPi.GPIO module**
* The concept of **class** in Python
* Ways to import Python modules
