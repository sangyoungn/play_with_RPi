# multi_seven_seg_led

## About
This example demonstrates displaying with multiple 7-segment LEDs via GPIO control using the RPi.GPIO module.

## Prerequisite
* Hardware
    * Raspberry Pi - Tested on RPi 4 Model B, which is preferred. But this should work on any RPi.
    * 2 or more 7-segment LED - In the demo code, a common-cathod one is used.
    * 8x Registers - 1000 ohm
* Software
    * Python 3 as is on Raspbery Pi OS

## Set Up
Refer to<br /> https://neighborhoodunclelab.tistory.com/entry/%EC%97%AC%EB%9F%AC-%EA%B0%9C%EC%9D%98-7-Segment-LED-%ED%91%9C%EC%8B%9C%ED%95%98%EA%B8%B0 <br />where further description can be found. (*Korean*)

## How to run
Clone the repository.
```bash
# You can bypass follow 2 commands if you already have cloned.
git clone https://github.com/sangyoungn/play_with_RPi.git
cd multi_seven_seg_led
```
Run the script.
```bash
# Run the script.
python multi_seven_seg_led.py
```