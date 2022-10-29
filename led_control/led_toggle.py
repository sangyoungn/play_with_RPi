# Import required modules
import RPi.GPIO as GPIO # RPi.GPIO module to contol GPIOs
from enum import Enum   # import Enum class to inherit and use enumumerators

class POLARITY(Enum):
    '''
    Enumerators for LED polarity
    ACTIVE_HIGH means LED is on when the state of GPIO is high and vice versa.
    '''
    ACTIVE_HIGH = 1
    ACTIVE_LOW = 0

class LED:
    '''
    Class for LED On/Off control
    '''
    def __init__(self, gpio, polarity=POLARITY.ACTIVE_HIGH):
        '''
        Initialize self. Specify gpio and polarity.
        The polarity is ACTIVE_HIGH by default.
        '''
        self.gpio = gpio
        self.polarity = polarity
        GPIO.setup(self.gpio, GPIO.OUT)
        self.off()
    def on(self):
        '''
        Turn on the LED
        '''
        GPIO.output(self.gpio, GPIO.HIGH if self.polarity == POLARITY.ACTIVE_HIGH else GPIO.LOW)
    def off(self):
        '''
        Turn off the LED
        '''
        GPIO.output(self.gpio, GPIO.LOW if self.polarity == POLARITY.ACTIVE_HIGH else GPIO.HIGH)

if __name__ == '__main__':
    # import time module for sleep to delay
    # Used only here so imported in this block
    import time
    
    GPIO.setmode(GPIO.BCM) # Specify the GPIO numbering mode.

    # Configure 2 LEDs
    led1 = LED(2)
    led2 = LED(3)

    # State flag to toggle LEDs
    on = False

    try:
        while(True):
            if (on):
                led1.on()
                led2.off()
                on = False # Invert the state
            else:
                led1.off()
                led2.on()
                on = True # Invert the state
            
            # Time delay for 1 sec
            time.sleep(1)
    except KeyboardInterrupt: # Ctrl+C will bering us here.
        GPIO.cleanup()
        exit(0)