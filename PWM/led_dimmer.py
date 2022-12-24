# This is to use a previous project as a module
# With this, we can import a project in the parent directory as a module
import sys
sys.path.append('..')

# Refer to https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
# for RPi_GPIO module
import RPi.GPIO as GPIO

# Import all classes and constants from the previous project
from led_control.led_toggle import *

DEFAULT_FREQ = 1000

class DIMMER(LED):
    '''
    Class for LED Dimming control
    Inherits class LED
    '''
    def __init__(self, gpio, polarity=POLARITY.ACTIVE_HIGH):
        '''
        Initialize self. Specify gpio and polarity.
        The polarity is ACTIVE_HIGH by default.
        '''
        super().__init__(gpio, polarity)
        self.is_dimming_running = False
        self.dim = GPIO.PWM(gpio, DEFAULT_FREQ)
        self.level = 0
 
    def dimming(self, duty_cycle):
        '''
        Dimming the LED per duty_cycle
        0 <= duty_cycle <= 100
        '''       
        if duty_cycle > 100:
            duty_cycle = 100
        if duty_cycle < 0:
            duty_cycle = 0
        # if (self.is_dimming_running):
        #     self.dim.ChangeDutyCycle(duty_cycle)
        #     if duty_cycle == 0:
        #         self.is_dimming_running = False
        #         self.dim.stop()
        # else:
        #     self.dim.start(duty_cycle)
        #     self.is_dimming_running = True
        self.level = duty_cycle
        if self.level == 0:
            self.dim.stop()
        else:
            self.dim.start(self.level)

    def get_current_level(self):
        '''
        Return current dimming level
        '''

        return self.level

# main
if __name__ == '__main__':
    # import time module for sleep to delay
    # Used only here so imported in this block
    import time
    import pdb
    
    GPIO.setmode(GPIO.BCM) # Specify the GPIO numbering mode.
    GPIO.setwarnings(False)

    # Functions for demo
    def demo0(led_array):
        '''
        Run this demo for about 5 sec
        On/Off all LEDs
        '''
        start_time = time.time_ns()
        current_time = time.time_ns()
        while((current_time-start_time)<5000000000):
            # Turn on all LEDs
            for led in led_array: 
                led.on()
            # Delay to get LEDs on
            time.sleep(0.5)

            # Turn off all LEDs
            for led in led_array: 
                led.off()
            # Delay to get LEDs off
            time.sleep(0.5)
            current_time = time.time_ns()

    def demo1(led_array):
        '''
        Run this demo for about 5 sec
        Dim up and down all LEDs
        '''
        start_time = time.time_ns()
        current_time = time.time_ns()
        current_dim_level = 100 # Initial Level
        current_dim_direct = -1 # Initial Direction of Dimming
        while((current_time-start_time)<5000000000):
            # Update the level of all LEDs
            for led in led_array:
                led.dimming(current_dim_level)
            
            # Calculate next level 
            current_dim_level = current_dim_level + current_dim_direct
            if current_dim_level < 0 and current_dim_direct == -1:
                # The level was decreasing and we reach to 0
                current_dim_level = 0
                current_dim_direct = 1
            if current_dim_level > 100 and current_dim_direct == 1:
                # The level was incrasing and we reach to 100
                current_dim_level = 100
                current_dim_direct = -1

            # Delay
            time.sleep(0.005)
            current_time = time.time_ns()

        # Stop PWM
        for led in led_array:
            led.dimming(0)

    def demo2(led_array):
        '''
        Run this demo for about 10 sec
        Dimming LEDs sequentially 
        '''

        decay = 20
        start_time = time.time_ns()
        current_time = time.time_ns()

        # Initialize dimming level of each LEDs for demo
        dim_levels = dict()
        for led in led_array:
            dim_levels[led] = 100

        while((current_time-start_time)<10000000000):
            for led in led_array:
                # Dimming each LED
                # 0 if the calculated level < 0, 100 if the calculated level > 100
                led.dimming(0 if dim_levels[led]<0 else 100 if dim_levels[led]>100 else dim_levels[led])

            for led in led_array:
                # Decay the level of the first LED
                if led_array.index(led) == 0:
                    dim_levels[led] = dim_levels[led]- decay
                else:
                    # Decay the level of remaining LEDs depending on the previous LED
                    if dim_levels[led_array[led_array.index(led)-1]] <= (100-2*decay) :
                        dim_levels[led] = dim_levels[led] - decay
                if led_array.index(led) == len(led_array)-1 and dim_levels[led] < 0:
                    # We've done a cycle
                    for led in led_array: # Re-init the levels
                        dim_levels[led] = 100
                    time.sleep(0.5) # Delay
            time.sleep(0.1)
            current_time = time.time_ns()

        # Stop PWM
        for led in led_array:
            led.dimming(0)

    # Main routine starts here
    gpios = (2,3,4,17,27) # GPIOs to be configured
    led_array = list() # List for LEDs in the array

    # Initialize the array of LEDs with the class instance
    for gpio in gpios:
        led_array.append(DIMMER(gpio))

    try:
        while(True):
            demo0(led_array)
            time.sleep(1)
            demo1(led_array)
            time.sleep(1)
            demo2(led_array)
    except KeyboardInterrupt: # Ctrl+C will bering us here.
        GPIO.cleanup()
        exit(0)