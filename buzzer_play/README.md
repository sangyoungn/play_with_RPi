# buzzer_play

## About
This example demonstrates playing music by controling PWM to a piezo buzzer in the RPi.GPIO module.

## Prerequisite
* Hardware
    * Raspberry Pi - Tested on RPi 4 Model B, which is preferred. But this should work on any RPi.
    * 1x Piezo Buzzer
    * Resistors or P- or N-MOSFETs are optional
* Software
    * Python 3 as is on Raspbery Pi OS

## Set Up
* Hardware Setup (*Korean*) can be found on
<br /> https://neighborhoodunclelab.tistory.com/entry/%EB%B2%84%EC%A0%80Buzzer-%EC%9A%B8%EB%A6%AC%EA%B8%B0-%ED%94%BC%EC%97%90%EC%A1%B0-%EB%B2%84%EC%A0%80Piezo-Buzzer%EC%9D%98-%EA%B5%AC%EB%8F%99 <br />
* Software Description (*Korean*) can be found on
<br /> https://neighborhoodunclelab.tistory.com/entry/%EB%B2%84%EC%A0%80Buzzer%EB%A1%9C-%EC%9D%8C%EC%95%85-%EC%97%B0%EC%A3%BC%ED%95%98%EA%B8%B0 <br />

## How to run
Clone the repository.
```bash
# You can bypass follow 2 commands if you already have cloned and are in the directory.
git clone https://github.com/sangyoungn/play_with_RPi.git
cd buzzer_play
```
Run the script.
```bash
python buzzer.py
```

## About using the implemented class
```Python
p = Buzzer(2) # Buzzer is connected to GPIO_2 (Pin 3). 

p.play('O4C3D3E3FGABO5C3R2')
```
Buzzer.play(*notes*) is the only method to be considered for playing a music. The argument *notes* is a string which can contain following notes.

**O***x* where *x* is an integer indicating an octave. The notes afterward will be referenced to the specified octave.

**T***y* where *y* is an integer indicating the tempo. The number of the tempo represents the number of quater notes played in a minute.

**R**, **C**, **C#**, **D**, **D#**, **E**, **F**, **F#**, **G**, **G#**, **A**, **A#**, **B** are notes followed by an integer *z*, where *z* is an integer representing the duration of playing. 

**R** represents Rest, **C** to **B** do steps in a musical scale. 

*z* can be *1* representing a whole note, *2* a half note, *3* a quater note, *4* a eighth note, and so on. *0* is used only with **R**. If *z* is omitted, the duration will be same as the previous one, the default of which is a quauter note.