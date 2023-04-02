# Pin Assignment
# A: 3, B: 2, C: 15, D: 23, E: 24, F: 17, G:27, DP: 14
# 2: B, 3: A, 14: DP, 15: C, 17: F, 27: G, 23: D, 24: E

import RPi.GPIO as GPIO
import pdb # import pdb for step trace

GPIO.setmode(GPIO.BCM)

GPIO.setup(3, GPIO.OUT) 
GPIO.setup(2, GPIO.OUT) 
GPIO.setup(14, GPIO.OUT) 
GPIO.setup(15, GPIO.OUT) 
GPIO.setup(17, GPIO.OUT) 
GPIO.setup(27, GPIO.OUT) 
GPIO.setup(23, GPIO.OUT) 
GPIO.setup(24, GPIO.OUT) 

pdb.set_trace() # Pause the execution
# Debugger is running at this point.
# "step" command will execute each line from now on.

GPIO.output(3, GPIO.HIGH)
GPIO.output(2, GPIO.HIGH)
GPIO.output(14, GPIO.HIGH)
GPIO.output(15, GPIO.HIGH)
GPIO.output(17, GPIO.HIGH)
GPIO.output(27, GPIO.HIGH)
GPIO.output(23, GPIO.HIGH)
GPIO.output(24, GPIO.HIGH)

GPIO.output(3, GPIO.LOW)
GPIO.output(2, GPIO.LOW)
GPIO.output(14, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
