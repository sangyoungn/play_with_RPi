# led_control

## About
Examples here demonstrate the PWM control using the RPi.GPIO module.

## Prerequisite
* Hardware
    * Raspberry Pi - Tested on RPi 4 Model B, which is preferred. But this should work on any RPi.
    * 5x LEDs - The coloer doesn't matter.
    * 5x Registers - 100 ohm
    * 5x 2N7000 N-Channel MOSFET
* Software
    * Python 3 as is on Raspbery Pi OS
    * [../led_control/led_toggle.py](../led_control/led_toggle.py)

## Set Up
Refer to<br /> https:// <br />where further description can be found. (*Korean*)

## How to run
```bash
python pwm_blink.py
```
```bash
python led_dimmer.py
```
Press *Ctrl+C* to exit.

## What to learn from this
* PWM control using Python **RPi.GPIO module**
* The concept of the inheritance of **class** in Python
* Ways to import Python modules
