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
Refer to<br /> https://neighborhoodunclelab.tistory.com/entry/%EC%95%84%EB%82%A0%EB%A1%9C%EA%B7%B8Analog%EC%9D%98-%ED%91%9C%ED%98%84-PWM-Pulse-Width-Modulation <br />where further description can be found. (*Korean*)

## How to run
Clone the repository.
```bash
# You can bypass follow 2 commands if you already have cloned.
git clone https://github.com/sangyoungn/play_with_RPi.git
cd PWM
```
Run scripts.
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

