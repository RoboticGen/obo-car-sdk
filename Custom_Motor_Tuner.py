#importing the needed libraries
from machine import Pin, I2C, PWM
import time
import ssd1306


#initializing the motor pins
left_motor_forward = PWM(Pin(05, Pin.OUT), freq=1000)
left_motor_backward = PWM(Pin(04, Pin.OUT), freq=1000)
right_motor_forward = PWM(Pin(19, Pin.OUT), freq=1000)
right_motor_backward = PWM(Pin(18, Pin.OUT), freq=1000)

#initializing the buttons
left_button = Pin(17, Pin.IN)
right_button = Pin(16, Pin.IN)

#initializing the OLED display
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#intializing the buzzer
buzzer = PWM(Pin(2, Pin.OUT))


#variables that will be using to control motor speed
LMS = 510
RMS = 510

motor_selection = 0

#initializing a function for a startup tone
def startup_tone():
    # Play a sequence of tones
    buzzer.freq(1000)   # 1 kHz
    buzzer.duty(512)    # 50% duty
    time.sleep(0.2)

    buzzer.freq(1500)   # 1.5 kHz
    time.sleep(0.2)

    buzzer.freq(2000)   # 2 kHz
    time.sleep(0.2)

    buzzer.duty(0)      # stop sound

#Initializing a function for the display
def display_para(msg, y):
    oled.text(str(msg), 0, y)
    oled.show()
    time.sleep(0.1)

def display(msg):
    oled.fill(0)
    oled.text(str(msg), 0, 0)
    oled.show()
    time.sleep(0.1)

#button reset function
def reset():
    global left
    global right
    left = 0
    right = 0

#function to check the status of the buttons
def press():
    reset()
    global left
    global right
    if(left_button.value() == False):
        left = 1
        time.sleep_ms(100)
        return left
    
    if(right_button.value() == False):
        right = 2
        time.sleep_ms(100)
        return right

#functions for the motors
def forward(Lspeed=LMS, Rspeed=RMS):
    left_motor_forward.duty(Lspeed)
    left_motor_backward.duty(0)
    right_motor_forward.duty(Rspeed)
    right_motor_backward.duty(0)
    

def backward(speedL=LMS, speedR=RMS):
    left_motor_backward.duty(speedL)
    left_motor_forward.duty(0)
    right_motor_backward.duty(speedR)
    right_motor_forward.duty(0)

def stop():
    left_motor_forward.duty(0)
    right_motor_forward.duty(0)
    left_motor_backward.duty(0)
    right_motor_backward.duty(0)


stop()
#main system of the motor tuner
#start massege and tone
startup_tone()
display_para("Welcome!", 0)
display_para("To Motor Tuner", 16)
display_para("by ELECTRO_VIBE", 30)
time.sleep(4)

#state of the machine
run=0

while(run==0):
    forward()
    display("Test Run")
    time.sleep(3)
    stop()
    oled.fill(0)
    display_para("Which Motor?", 0)
    display_para("Left -> L", 16)
    display_para("Right -> R", 30)
    run=1

while(run==1):
    #motor selection
    pressed_button = press()
    if(pressed_button == 1):
        display("Selected Left")
        motor_selection = 1
        time.sleep(2)
        run=2
    
    elif(pressed_button == 2):
        display("Selected Right")
        motor_selection = 2
        time.sleep(2)
        run=2
    
oled.fill(0)
display_para("Press", 0)
display_para("Left -> reduce", 16)
display_para("Right -> increase", 30)

while(run==2):
#motor tuning
    #for left motor
    if(motor_selection == 1):
        if(left_button.value()==False and LMS>0):
            LMS = LMS - 2
            display(LMS)
            forward(LMS,RMS)
            
        elif(right_button.value()==False and LMS<512):
            LMS = LMS + 2
            display(LMS)
            forward(LMS,RMS)
    
    
    #for right motor
    if(motor_selection == 2):
        if(left_button.value()==False and RMS>0):
            RMS = RMS - 2
            display(RMS)
            forward(LMS,RMS)
            
        elif(right_button.value()==False and RMS<512):
            RMS = RMS + 2
            display(RMS)
            forward(LMS,RMS)