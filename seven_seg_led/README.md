# seven_seg_led

## About
This example demonstrates the 7-segment display via GPIO using the RPi.GPIO module.

## Prerequisite
* Hardware
    * Raspberry Pi - Tested on RPi 4 Model B, which is preferred. But this should work on any RPi.
    * 7-segment LED - In the demo code, a common-cathod one is used.
    * 8x Registers - 1000 ohm
* Software
    * Python 3 as is on Raspbery Pi OS

## Set Up
Refer to<br /> https://neighborhoodunclelab.tistory.com/entry/7-Segment-LED-%ED%91%9C%EC%8B%9C%ED%95%98%EA%B8%B0 <br />where further description can be found. (*Korean*)

## How to run
Clone the repository.
```bash
# You can bypass follow 2 commands if you already have cloned.
git clone https://github.com/sangyoungn/play_with_RPi.git
cd seven_seg_led
```
Run the script.
```bash
#Run the script.
python seven_seg_led.py
```