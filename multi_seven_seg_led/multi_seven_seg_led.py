# This is to use a previous project as a module
# With this, we can import a project in the parent directory as a module
import sys
sys.path.append('..')

# Refer to https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
# for RPi_GPIO module
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Refer to https://docs.python.org/3/library/threading.html
from threading import Thread

# Refer to https://docs.python.org/3/library/time.html
import time

# Let's import the work we've done previously.
from seven_seg_led.seven_seg_led import *

import pdb

class MULTI_SEVEN_SEG_LED:
    '''
    Example: 

    leds = MULTI_SEVEN_SEG_LED((3, 2, 15, 23, 24, 17, 27, 14), (9,10))
    leds.display_start()
    leds.update(12)
    ...
    leds.display_stop()
    '''
    def __init__(self, pins: tuple, common_pins: tuple, isCC=True):     # Initializer
        '''
        Initilazer

        pins: A tuple containing GPIO numbers to control each LED in a seven segment LED
        common_pins: A tuple containing GPIO numbers connected to each common pin
        isCC: True if the configuration is common-cathode, False if common-anode.
        '''
        # Output pins are same for all digits. 
        # So a single SEVEN_SEG_LED instance is engough.
        self.isCC = isCC
        self.digits = SEVEN_SEG_LED(pins, isCC=self.isCC) 

        # Instead, we have the same number of common pins as the number of digits.
        self.common_pins = common_pins
        for pin in self.common_pins:
            GPIO.setup(pin, GPIO.OUT)
            if (isCC): # To disable the output, the default output is to be HIGH for Common Cathode.
                GPIO.output(pin, GPIO.HIGH)
            else: # Else the default output is to be LOW for Common Anode.
                GPIO.output(pin, GPIO.LOW)

        # Following instance variables are for Thread operation.
        self.display_task = None
        self.keepRunning = True

        # This is an instance varialble to store the value to be displayed.
        self.display_value = "" # For a value to be displayed
        # Below is a list indicating whether of not to turn on DPs of each digit.
        self.DPs = list([False]*len(self.common_pins))

    def __del__(self):      # Destructor
        if(self.display_task != None):  # In case the display task was running,
            self.display_task.join()    # Wait until the task ends.

    def _display(self):     # Task loop for display
        DELAY = 0.005
        while(self.keepRunning): # This value will become False in display_stop() method.
            value = self.display_value # Copy display_value to a temporary variable
            if(len(self.common_pins) > len(value)):
                # The value to be displayed is shorter than available digits.
                # Pad (a) space(s) in front.
                value = ' '*(len(self.common_pins)-len(value)) + value
            else:
                # Longer or same
                # We will display the last digits.
                value = value[-len(self.common_pins):]

            index = 0
            for pin in self.common_pins: # Repeat as many as available digits.
                # Update the digit at index
                self.digits.update(value[index], \
                                dot = True if self.DPs[index] else False)
                
                # Now make the forward bias. 
                # In case of the common-cathode, the common pin should be LOW,
                # to foreward-bias.
                if (self.isCC):
                    GPIO.output(pin, GPIO.LOW)
                else:
                    GPIO.output(pin, GPIO.HIGH)

                # Delay to retain the current state at the digit at index.
                time.sleep(DELAY)

                # Now turn off the foreward-bias state.
                if (self.isCC):
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    GPIO.output(pin, GPIO.LOW)

                # Increment index and prepare to move forward to next digit.
                index += 1

    def display_start(self):    # Start display
        # Initialize Thread instance with the target of _display method.
        self.display_task = Thread(target=self._display)
        # Start Thread operation.
        self.display_task.start()

    def display_stop(self):     # Stop display
        self.keepRunning = False # Make this value False to escape from displaying loop.
    
    def update(self, value):       # Update display
        if (type(value)==str): # If the type of value is str,
            # Just use as is.
            self.display_value = value
        else: # Else,
            # Convert to str.
            self.display_value = str(value)

    def set_DP(self, position: int):
        if(position < len(self.DPs)):
            self.DPs[position] = True
        # Else do nothing

    def unset_DP(self, position: int):
        if(position < len(self.DPs)):
            self.DPs[position] = False
        #Else do nothing 

if __name__ == "__main__":
    print("Demo started")

    # Initialize a MULTI_SEVEN_SEG_LED instance.
    a = MULTI_SEVEN_SEG_LED((3, 2, 15, 23, 24, 17, 27, 14), (9,10))

    # Start display, which starts a thread.
    a.display_start()

    # Set a decimal point position.
    # The position doesn't necessarily need to be uniquely single
    # but could be multiple.
    a.set_DP(0)

    # Demo 1 
    # Display 1 to 99 every second.
    for i in range(1,100):
        a.update(i)
        time.sleep(1)

    # Unset the previousely set decimal point.
    a.unset_DP(0)

    # Demo 2
    # Display 1 to 255 every second in hexa-decimal form.
    for i in range(1,256):
        a.update(hex(i)[2:])
        time.sleep(1)

    # Stop display, which stops the function in thread.
    a.display_stop()

    print("Demo ended")
