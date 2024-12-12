# OBOCar SDK Documentation
<p align="center">
<img width="736" height="400" src="https://github.com/RoboticGen/obo-car-sdk/blob/main/IMG/obocar_image.png?raw=true" text="OBO CAR">
  <p align="center">
    <em>OBO CAR</em>
    </p> 
---

## Introduction

The **OBOCar SDK** is a lightweight MicroPython library designed for controlling the OBOCar using the ESP32 microcontroller. It supports motor control, buzzer interaction, OLED display, and button inputs. This guide is tailored for use with **Thonny IDE**.

---

## Features

- **Motor Control**:
  - Forward, backward, left, and right motion with speed control (max: **512**).
- **Buzzer**:
  - Generate single beeps or play sequences of tones.
- **OLED Display**:
  - Display text messages on an SSD1306 OLED screen.
- **Buttons**:
  - Detect left and right button presses.

---

## Prerequisites

1. Install **MicroPython** firmware on your ESP32.
   - Download: [MicroPython.org](https://micropython.org/).
2. Install **Thonny IDE**.
   - Download: [Thonny.org](https://thonny.org/).

---

## Setup

### Hardware Connections

| **Component**    | **ESP32 Pin** | **Details**                  |
| ---------------- | ------------- | ---------------------------- |
| Motor Left (L1)  | GPIO 5        | Motor forward-left control   |
| Motor Left (L2)  | GPIO 4        | Motor backward-left control  |
| Motor Right (R1) | GPIO 19       | Motor forward-right control  |
| Motor Right (R2) | GPIO 18       | Motor backward-right control |
| Buzzer           | GPIO 2        | Sound output                 |
| OLED SCL         | GPIO 22       | I2C clock                    |
| OLED SDA         | GPIO 21       | I2C data                     |
| Button Left      | GPIO 17       | Detect left button press     |
| Button Right     | GPIO 16       | Detect right button press    |

### Upload SDK to ESP32

1. Save the SDK code as a file (e.g., `obocar.py`).
2. Open **Thonny IDE**:
   - Connect your ESP32.
   - Upload the file to your device.

---

## Initialization

Initialize the OBOCar using the following example:

```python
from obocar import OBOCar

# Initialize OBOCar
car = OBOCar(
    motor_pins={'L1': 5, 'L2': 4, 'R1': 19, 'R2': 18},
    buzzer_pin=2,
    oled={'scl': 22, 'sda': 21, 'width': 128, 'height': 64},
    buttonL_pin=17,
    buttonR_pin=16
)

```

## Motor Control

```python
car.move_forward(speed=512)  # Move forward at maximum speed
car.move_backward(speed=256)  # Move backward at half speed
car.turn_left(speed=512)  # Turn left at maximum speed
car.turn_right(speed=512)  # Turn right at maximum speed
car.stop()  # Stop the car

```

## Buzzer

```python

car.beep(freq=1000, duration=0.5)  # Play a 1000 Hz tone for 0.5 seconds
car.start_tone()  # Play startup tone sequence

```

## OLED Display

```python

car.display("Hello, OBOCar!", 0, 0)  # Display a message on the OLED

```

## Button Interaction

```python

if car.is_buttonL_pressed():
    print("Left button pressed!")

if car.is_buttonR_pressed():
    print("Right button pressed!")


```

## Convert Image to byteArray

```python

import convert.py
converted = convert.image_to_buffer(r"/Users/sanjulagathsara/Desktop/GitHub Repos/obocar/img2.png")
buffer = converted[0]
buffer

```

## Show Image

```python

import framebuf

roboticgen_logo = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x078\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x06\x03\x80\x00\x00\x00\x00\x00\x00\x07\xfc\x00\x00\xf0\x00\x00\x0e\x07\x80\x00\x0f\x80\x00\x00\x00\x07\xfe\x00\x00p\x00\x00\x0e\x07\x80\x00?\xe0\x00\x00\x00\x07\xff\x00\x00p\x00\x00\x0e\x03\x00\x00\x7f\xe0\x00\x00\x00\x07\x07\x80\x00`\x00\x00\x0e\x00\x00\x00\xf0`\x00\x00\x00\x07\x03\x83\xf0\x7f\xc0~\x1f\xf3\x87\xe1\xe0\x00|\x07\xc0\x07\x01\xc7\xf8\x7f\xe0\xff\x1f\xf3\x8f\xf9\xc0\x01\xff?\xe0\x07\x01\xcf\xfc\x7f\xf1\xff\x9f\xf3\x9f\xf9\xc0\x01\xef?\xf0\x07\x01\xde\x1exs\xc3\x8e\x03\x9c1\x80\x03\x8e<p\x07\x03\x9c\x0eps\x81\xce\x03\x9c\x01\x80s\x9e88\x07\x8f\x9c\xcew;\x99\xce\x03\xb8\x01\xc0s\x1c88\x07\xff\x1c\xcec3\x99\xce\x03\xb8\x01\xc0s888\x07\xfe\x1c\x0eps\x81\xce\x03\xbc\x01\xe0s\xf088\x07\xfe\x1e\x1cx\xf3\xc3\x87\x03\x9e0\xf0s\xe288\x07\x0e\x0f\xfc?\xf1\xff\x87\xf3\x9f\xf8\x7f\xf1\xff88\x07\x07\x07\xf8?\xe0\xff\x03\xf3\x8f\xf8?\xe0\xff88\x07\x07\x03\xf0\x0f\x80~\x01\xf3\x83\xe0\x1f\xc0|\x180\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
fb = framebuf.FrameBuffer(roboticgen_logo, 128, 33, framebuf.MONO_HLSB)
car.OLED.framebuf.blit(fb, 0, 14)
car.OLED.show()


```
