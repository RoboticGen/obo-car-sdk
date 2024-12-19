# OBOCar SDK Documentation
<p align="center">
<img width="100%" src="https://github.com/RoboticGen/obo-car-sdk/blob/main/IMG/obocar_image.png?raw=true" text="OBO CAR">
  <p align="center">
    </p> 

---

## Introduction

The **OBOCar SDK** is a lightweight MicroPython library designed for controlling the OBOCar using the ESP32 microcontroller. It supports motor control, buzzer interaction, OLED display, Ultrasonic Sensors and button inputs. This guide is tailored for use with **Thonny IDE**.

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
- **Ultrasonic**:
  - Measure distances for obstacle detection using front, left, and right sensors.

---

## Prerequisites

1. **Install Thonny IDE**:

   - Download and install Thonny IDE from [Thonny.org](https://thonny.org/).

2. **Install MicroPython on ESP32**:

   - Open Thonny IDE.
   - Go to `Run -> Configure Interpreter`.
   - In the "Interpreter" section, select:
     - **MicroPython (ESP32)** under "MicroPython family."
     - For the "Port," choose **< Try to detect port Automatically >**
   - Click **Install or update MicroPython (esptool)**.
   - Choose:
     - For the "Target Port," choose the correct **Target Port** for your ESP32 (e.g., `COM3`, `COM4`, `/dev/ttyUSB0`).
     - **MicroPython family**: ESP32.
     - **Variant**: Espressif ESP32 / WROOM.
   - Click **Install** to flash MicroPython onto your ESP32.

3. **Upload the OBOCar SDK**:
   - Create a new file in Thonny.
   - Copy the contents of `obocar.py` into the file.
   - Save the file as `obocar.py` directly onto the ESP32.

---

## Once MicroPython is installed, you can connect to the ESP32 via Thonny and start using the SDK. Continue with the usage examples and SDK features listed above!

## Troubleshooting MicroPython on ESP32

If you encounter issues such as a **"Backend not ready"** warning or the program seems stuck, follow these steps to reset your ESP32:

1. **Press the Stop Button**:

   - In Thonny, click the red **Stop** button located at the top to interrupt any running code.

2. **Reset via Shell**:

   - If pressing the stop button doesn’t resolve the issue:
     - Make sure you do not click or interact with the shell section in Thonny.
     - Instead, press **Ctrl + C** twice in quick succession to force a reset of the ESP32.

3. **Reconnect the Device**:

   - If the device still doesn't respond, unplug and replug your ESP32.
   - Go to `Run -> Configure Interpreter` and verify the **Target Port** is still correctly set.

4. **Reinstall MicroPython** (Optional):
   - If the problem persists, you may need to reinstall MicroPython using the instructions provided above.

With these steps, you should be able to regain control of your ESP32 and continue using the OBOCar SDK.

## Setup

### Hardware Connections

| **Component**                | **ESP32 Pin** | **Details**                  |
| ---------------------------- | ------------- | ---------------------------- |
| **Motor Left (L1)**          | GPIO 5        | Motor left control 1         |
| **Motor Left (L2)**          | GPIO 4        | Motor left control 2         |
| **Motor Right (R1)**         | GPIO 19       | Motor right control 1        |
| **Motor Right (R2)**         | GPIO 18       | Motor right control 2        |
| **Buzzer**                   | GPIO 2        | Sound output                 |
| **OLED SCL**                 | GPIO 22       | I2C clock                    |
| **OLED SDA**                 | GPIO 21       | I2C data                     |
| **Button Left**              | GPIO 17       | Detect left button press     |
| **Button Right**             | GPIO 16       | Detect right button press    |
| **Ultrasonic Trigger Front** | GPIO 32       | Trigger pin for front sensor |
| **Ultrasonic Echo Front**    | GPIO 39       | Echo pin for front sensor    |
| **Ultrasonic Trigger Left**  | GPIO 13       | Trigger pin for left sensor  |
| **Ultrasonic Echo Left**     | GPIO 15       | Echo pin for left sensor     |
| **Ultrasonic Trigger Right** | GPIO 23       | Trigger pin for right sensor |
| **Ultrasonic Echo Right**    | GPIO 36       | Echo pin for right sensor    |

---

## Initialization

Initialize the OBOCar using the following example:

```python
from obocar import OBOCar

# Initialize OBOCar
car = OBOCar()

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

#### **Ultrasonic Sensors**

The OBOCar SDK includes support for ultrasonic sensors for obstacle detection in three directions: **front**, **left**, and **right**.

```python
# Measure the front distance
front_distance = car.get_front_distance()
print(f"Front distance: {front_distance:.2f} cm")

# Measure the left distance
left_distance = car.get_left_distance()
print(f"Left distance: {left_distance:.2f} cm")

# Measure the right distance
right_distance = car.get_right_distance()
print(f"Right distance: {right_distance:.2f} cm")
```

---

### Ultrasonic Obstacle Detection

The ultrasonic sensors can be used for obstacle detection in all three directions. Example:

```python

# Simple obstacle avoidance

from obocar import OBOCar
import time
car = OBOCar()

while True:
    front_distance = car.get_front_distance()
    if front_distance < 20:  # If an obstacle is closer than 20 cm
        car.move_backward(512)
        time.sleep(0.3)
        car.turn_left(512)
        print("Obstacle detected! Turning...")
        time.sleep(0.5)
    else:
        car.move_forward(speed=512)
    time.sleep(0.1)

```

---

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

**Contribute:**  
Suggestions and improvements are welcome! This SDK is designed to be extensible for further development in OBOCAR.
