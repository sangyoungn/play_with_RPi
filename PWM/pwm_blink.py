import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.OUT)

pwm = GPIO.PWM(2, 1000)

dc = 100 # Initial value of Duty Cycle
pwm.start(dc) # Start PWM
direction = -1 # Initial Direction: Decreasing

try:
    while(True): #Ininite Loop except for break by user
        dc = dc + direction # Update Duty Cycle
        pwm.ChangeDutyCycle(dc) # Apply change
        if(dc <= 0 and direction == -1): # If Duty Cycle was decreasing and now reach to 0
            direction = 1
        elif(dc >= 100 and direction == 1): # If Ducy Cycle was increasing and now reach to 100
            direction = -1
        sleep(0.01)

except KeyboardInterrupt:
    pwm.stop()

GPIO.output(2, GPIO.LOW)