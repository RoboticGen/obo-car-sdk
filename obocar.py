"""
OBOCar SDK - Version 1.4.0
=========================

This SDK is designed for controlling the OBOCar, providing easy-to-use APIs for motor control, 
buzzer interaction, and OLED display management, button Inputs. The SDK is built using MicroPython, and it 
simplifies the interface to control an autonomous car with features such as movement, sound alerts, 
and visual display capabilities.

Initial creation by Sanjula Gathsara - RoboticGen (Pvt) Ltd
===========================================================

Features:
---------
- Motor control for forward, backward, and turning motions.
- Buzzer control for beeps and sequences.
- OLED display support for text messages.
- Designed to be easily extensible and adaptable for educational robotics.

Usage Example:
--------------
You can initialize the car with the standard pin configuration:

    car = OBOCar()
    car.move_forward()
    car.display("Hello, World!", 0, 0)
    
Or customize specific pins:

    custom_pins = {
        'motor': {'L1': 12, 'L2': 13},  # Only override specific motor pins
        'buzzer': 15                     # Change buzzer pin
    }
    car = OBOCar(pins=custom_pins)
    
    # Access pins externally
    motor_pin = car.get_pin('motor', 'L1')  # Returns 12
    buzzer_pin = car.get_pin('buzzer')      # Returns 15

"""



from machine import Pin, PWM, SoftI2C, time_pulse_us
import time
import framebuf

MAX_SPEED = 512
            
       
                   
# MicroPython SSD1306 OLED driver

class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin. 
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms


# register definitions
SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)

# ============================
# SSD1306 Class
# ============================   

class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        # Note the subclass must initialize self.framebuf to a framebuffer.
        # This is necessary because the underlying data buffer is different
        # between I2C and SPI implementations (I2C needs an extra byte).
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00, # off
            # address setting
            SET_MEM_ADDR, 0x00, # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30, # 0.83*Vcc
            # display
            SET_CONTRAST, 0xff, # maximum
            SET_ENTIRE_ON, # output follows RAM contents
            SET_NORM_INV, # not inverted
            # charge pump
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        # Add an extra byte to the data buffer to hold an I2C data/command byte
        # to use hardware-compatible I2C transactions.  A memoryview of the
        # buffer is used to mask this byte from the framebuffer operations
        # (without a major memory hit as memoryview doesn't copy to a separate
        # buffer).
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Set first byte of data buffer to Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        # Blast out the frame buffer using a single I2C transaction to support
        # hardware I2C interfaces.
        self.i2c.writeto(self.addr, self.buffer)

    def poweron(self):
        pass


# ============================
# Buzzer Class
# ============================

# Define a sequence of tones (frequency in Hz, duration in seconds)
start_tone_sequence = [
    (600, 0.2),  # Beep 1
    (800, 0.2),  # Beep 2
    (600, 0.2),  # Beep 1
    (800, 0.2),  # Beep 2
    (700, 0.5),  # Beep 3
]

class Buzzer:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
    
    def play_tone(self, freq, duration, duty=512):
        self.pwm.freq(freq)
        self.pwm.duty(duty)
        time.sleep(duration)
        self.pwm.duty(0)  # Turn off the buzzer
    
    def play_sequence(self, tones):
        """
        Play a sequence of tones.
        tones: list of tuples (frequency, duration)
        """
        for freq, duration in tones:
            self.play_tone(freq, duration)
    
    def stop(self):
        self.pwm.deinit()

# ============================
# Button Class
# ============================

class Button:
    def __init__(self, pin):
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)
    
    def is_pressed(self):
        # Return True if the button is pressed (low state)
        return self.button.value() == 0


# ============================
# OBOCar Class
# ============================

class OBOCar:
    """OBOCar - Main class for controlling the OBO autonomous car with motor, sensor, buzzer and display functions"""
    # Default pin configurations
    PINS = {
        'motor': {'L1': 5, 'L2': 4, 'R1': 19, 'R2': 18},
        'buzzer': 2,
        'oled': {'scl': 22, 'sda': 21, 'width': 128, 'height': 64},
        'buttonL': 17,
        'buttonR': 16,
        'triggerF': 32,
        'echoF': 39,
        'triggerL': 13,
        'echoL': 15,
        'triggerR': 23,
        'echoR': 36
    }
    
    def __init__(self, pins=None):
        # Initialize pins with defaults, update with any provided pins
        self.pins = self.PINS.copy()
        if pins:
            for category, value in pins.items():
                if category in self.pins:
                    if isinstance(value, dict) and isinstance(self.pins[category], dict):
                        self.pins[category].update(value)
                    else:
                        self.pins[category] = value
        
        # Motor Control Pins
        self.IA1 = PWM(Pin(self.pins['motor']['L1']))
        self.IB1 = PWM(Pin(self.pins['motor']['L2']))
        self.IA2 = PWM(Pin(self.pins['motor']['R1']))
        self.IB2 = PWM(Pin(self.pins['motor']['R2']))
        
        # Set PWM frequency (adjust according to your motor specs)
        self.IA1.freq(1000)
        self.IB1.freq(1000)
        self.IA2.freq(1000)
        self.IB2.freq(1000)

        # Initialize motors to stop
        self.stop()
        
        # Initialize Buzzer
        self.buzzer = Buzzer(self.pins['buzzer'])
        
        # ESP32 Pin assignment 
        self.i2c = SoftI2C(scl=Pin(self.pins['oled']['scl']), sda=Pin(self.pins['oled']['sda']))
        
        self.OLED = SSD1306_I2C(self.pins['oled']['width'], self.pins['oled']['height'], self.i2c)
        
        self.ultrasonic = HCSR04(trigger_pin=self.pins['triggerF'], echo_pin=self.pins['echoF'])
        self.ultrasonicL = HCSR04(trigger_pin=self.pins['triggerL'], echo_pin=self.pins['echoL'])
        self.ultrasonicR = HCSR04(trigger_pin=self.pins['triggerR'], echo_pin=self.pins['echoR'])
        
        # Initialize Buttons
        self.buttonL = Button(self.pins['buttonL'])
        self.buttonR = Button(self.pins['buttonR'])
        
        self.stop()
        
        self.beep()
    
    # Motor Control Methods
    def stop(self):
        self.IA1.duty(0)
        self.IB1.duty(0)
        self.IA2.duty(0)
        self.IB2.duty(0)
    
    def move_forward(self, speed=512):  # Default speed set to half
        
        if(speed > MAX_SPEED): #Limiting speed
            speed = MAX_SPEED
        elif(speed<0):
            speed = 0
            
        self.IA1.duty(speed)
        self.IB1.duty(0)
        self.IA2.duty(speed)
        self.IB2.duty(0)
        
    def left_motor_forward(self, speed=512):  # Default speed set to half
        
        if(speed > MAX_SPEED): #Limiting speed
            speed = MAX_SPEED
        elif(speed<0):
            speed = 0
            
        self.IA1.duty(speed)
        self.IB1.duty(0)
        
    def left_motor_backward(self, speed=512):  # Default speed set to half
        
        if(speed > MAX_SPEED): #Limiting speed
            speed = MAX_SPEED
        elif(speed<0):
            speed = 0
            
        self.IA1.duty(0)
        self.IB1.duty(speed)
        
    def right_motor_forward(self, speed=512):  # Default speed set to half
        
        if(speed > MAX_SPEED): #Limiting speed
            speed = MAX_SPEED
        elif(speed<0):
            speed = 0
            
        self.IA2.duty(speed)
        self.IB2.duty(0)

    def right_motor_backward(self, speed=512):  # Default speed set to half
        
        if(speed > MAX_SPEED): #Limiting speed
            speed = MAX_SPEED
        elif(speed<0):
            speed = 0
            
        self.IA2.duty(0)
        self.IB2.duty(speed)

        
    def move_backward(self, speed=512):  # Default speed set to half
        
        if(speed > MAX_SPEED): #Limiting speed
            speed = MAX_SPEED
        elif(speed<0):
            speed = 0
        
        self.IA1.duty(0)
        self.IB1.duty(speed)
        self.IA2.duty(0)
        self.IB2.duty(speed)
    
    def turn_left(self, speed=512):
        
        if(speed > MAX_SPEED): #Limiting speed
            speed = MAX_SPEED
        elif(speed<0):
            speed = 0
        
        self.IA1.duty(0)
        self.IB1.duty(speed)
        self.IA2.duty(speed)
        self.IB2.duty(0)

    def turn_right(self, speed=512):
        
        if(speed > MAX_SPEED): #Limiting speed
            speed = MAX_SPEED
        elif(speed<0):
            speed = 0
        
        self.IA1.duty(speed)
        self.IB1.duty(0)
        self.IA2.duty(0)
        self.IB2.duty(speed)

    # Buzzer Control Methods
    def beep(self, freq=1000, duration=0.1):
        self.buzzer.play_tone(freq, duration)
    
    def play_sequence(self, tones):
        self.buzzer.play_sequence(tones)
        
    def display(self, message, x=0, y=0):
        """
        Display a message on the OLED screen.
        message: The message to display
        x: The x-coordinate of the message (default is 0)
        y: The y-coordinate of the message (default is 0)
        """
        if self.OLED:
            self.OLED.fill(0)  # Clear the display
            self.OLED.text(message, x, y, 1)  # Display message
            self.OLED.show()  # Update the display
    
    def start_tone(self):
        self.buzzer.play_sequence(start_tone_sequence)
        
    # Button Control Methods
    def is_buttonL_pressed(self):
        return self.buttonL.is_pressed()
    
    def is_buttonR_pressed(self):
        return self.buttonR.is_pressed()
    
    # Run Method (add any logic you need for operation)
    def run(self, delay=0.1):
        while True:
            # Add logic to control the car
            time.sleep(delay)
            
    def get_front_distance(self):
        return self.ultrasonic.distance_cm()
    
    def get_left_distance(self):
        return self.ultrasonicL.distance_cm()
    
    def get_right_distance(self):
        return self.ultrasonicR.distance_cm()
    
    def get_pin(self, pin_type, pin_name=None):
        """Get pin information from the OBOCar"""
        if pin_type not in self.pins:
            return None
            
        if pin_name is not None and isinstance(self.pins[pin_type], dict):
            if pin_name in self.pins[pin_type]:
                return self.pins[pin_type][pin_name]
            return None
            
        return self.pins[pin_type]




