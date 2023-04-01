# This is to use a previous project as a module
# With this, we can import a project in the parent directory as a module
import sys
sys.path.append('..')

# Refer to https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
# for RPi_GPIO module
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Import all classes and constants from the previous project
from led_control.led_toggle import *

class SEVEN_SEG_LED:
    '''
    Class to represent 7-segment LED

    pins is a tuple which has GPIO numbers for each segment - A to G and DP in turns.
    init_val is a value to present after initilization.
    isCC is to indicate the 7-segment in use is Common-Carhod if True or Comman-Anode oterwise.
    '''
    def __init__(self, pins:tuple, init_val=None, isCC=True):
        '''
        Initialize a 7-segment LED.
        '''

        # self.led_array is a list which has LED instances with given GPIO# in pins.
        self.led_array = list()
        
        # Initialize self.led_array with LED instances.
        for pin in pins:
            self.led_array.append(LED(pin, 
                                     POLARITY.ACTIVE_HIGH if isCC == True else POLARITY.ACTIVE_LOW))
        
        # Update display with the initial value. It doesn't matter what init_val is. update() methode will handle. 
        self.update(init_val)

    def update(self, val=None, dot=False):
        '''
        Update the display with a givein init_val.

        init_val is to be a number ranged 0~9, A~F in case of the hexa-decimal number or can be its string representation.
        '''

        # look_up_table is a truth table corresponding to each value. DP is not included because it is independent.
        # Lookup table is implemented with dict for ease of search.
        # 'Digit': (A, B, C, D, E, F, G)
        look_up_table  = {  '0': (True, True, True, True, True, True, False),
                            '1': (False, True, True, False, False, False, False),
                            '2': (True, True, False, True, True, False, True),
                            '3': (True, True, True, True, False, False, True),
                            '4': (False, True, True, False, False, True, True),
                            '5': (True, False, True, True, False, True, True),
                            '6': (True, False, True, True, True, True, True),
                            '7': (True, True, True, False, False, False, False),
                            '8': (True, True, True, True, True, True, True),
                            '9': (True, True, True, True, False, True, True),
                            'a': (False, False, True, True, True, False, True),
                            'A': (False, False, True, True, True, False, True),
                            'b': (False, False, True, True, True, True, True),
                            'B': (False, False, True, True, True, True, True),
                            'c': (False, False, False, True, True, False, True),
                            'C': (False, False, False, True, True, False, True),
                            'd': (False, True, True, True, True, False, True),
                            'D': (False, True, True, True, True, False, True),
                            'e': (True, True, False, True, True, True, True),
                            'E': (True, True, False, True, True, True, True),
                            'f': (True, False, False, False, True, True, True),
                            'F': (True, False, False, False, True, True, True) }
        
        # First, change the type of val to str if it is not.
        if type(val) != str:
            val = str(val) 


        if val not in look_up_table:
            # If the val is not a supported value, turn off all segments.
            for each_led in self.led_array:
                each_led.off()
        else:
            # Update each segment per truth table. A segment will be turn on if the value in truth table is True.
            for each_led in self.led_array:
                if self.led_array.index(each_led) == 7: # It looks a little messy but we don't update DP here.
                    break
                # Turn on the LED of current index if the value on the truth table of current index is True.
                each_led.on() if look_up_table[val][self.led_array.index(each_led)] == True else each_led.off()

        # Finally, update DP here.
        self.led_array[-1].on() if dot==True else self.led_array[-1].off()

# Below is a code to show a demo of calss SEVEN_SEG_LED if this file is executed.
if __name__=='__main__':
    import time # Import time module for the delay.

    # Initialize a SEVEN_SEG_LED instance. 
    # A: GPIO 3, B: GPIO 2, C: GPIO 15, D: GPIO 23, E: GPIO 24, F: GPIO 17, G:GPIO 27, DP: GPIO 14
    a = SEVEN_SEG_LED((3, 2, 15, 23, 24, 17, 27, 14))

    # while(True):
    toggle = False
    for num in range(0, 10): # Will display 0 to 9.
        a.update(num, dot=toggle) # Update the 7-segment LED with a given number.
        time.sleep(1) # Delay for a second.
        toggle = True if toggle==False else False # Toggle the variable to toggle DP.

    a.update(None) # Turn off all segments.
        