'''
Bluetooth Controlling OBO Car 
This example demonstrates how to control the OBO Car using Bluetooth Low Energy (BLE).
Add this code to the boot.py file on your OBO Car's MicroPython environment.
'''

from machine import Pin
from obocar import OBOCar
import ubluetooth
import time
import framebuf


# UUIDs for the service and characteristic
# MicroPython
SERVICE_UUID = ubluetooth.UUID(0xFFE0)  # 16-bit
CHAR_UUID = ubluetooth.UUID(0xFFE1)     # 16-bit

# Variable to store the received command
received_command = None

speed = 512  # max 512

# Initialize the OBOCar
car = OBOCar()

obocar_logo = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<\x00\x7f\x06\x00\x0f\x80\x00\x01\xe0\x00\x1c\x0f\xfe\x00\x01\xff\x80~\x07\x00\x7f\xe0\x00\x0f\xfc\x00\x1c\x0f\xff\x80\x03\x00\xc0`\x01\x80\xe00\x00\x18\x06\x004\x00\x00\xc0\x06\x00``\x00\x81\x80\x18\x000\x03\x00&\x00\x00`\x0c\x000`\x00\xc3\x00\x0c\x00`\x01\x80b\x00\x00 \x08\x00\x10`\x00\xc2\x00\x06\x10@\x00\xc0C\x00\x000\x18\x00\x18`\x00\xc6\x00\x02\x00\xc0\x00\x00\xc1\x00\x000\x108\x08`\x01\x86\x00\x02\x00\x80\x00\x00\x81\x80\x000\x10|\x08`\x03\x84\x00\x03\x00\x80\x00\x01\x80\x80\x000\x10~\x08`?\x04\x00\x03\x00\x80\x00\x01\x80\xc0\x000\x10|\x08`\x03\x04\x00\x03\x00\x80\x00\x01\x00\xc0\x00\x00\x10<\x08`\x01\x86\x00\x02\x00\x80\x00\x03\x00@\xc0\x00\x10\x18\x18`\x00\x86\x00\x02\x00\xc0\x00\x02\x00``\x00\x18\x00\x18`\x00\xc2\x00\x06\x10@\x00\x86\x00 8\x00\x0c\x000`\x00\xc3\x00\x04\x10`\x01\x84\x000\x1c\x00\x04\x00``\x00\xc1\x80\x0c\x000\x01\x0c\x00\x10\x06\x00\x07\x00\xc0`\x01\x80\xc08\x00\x18\x07\x0c\x00\x18\x03\x00\x01\xc3\x80`\x03\x00p\xf0\x00\x0e\x1c\x08\x00\x08\x01\x80\x00~\x00`>\x00\x1f\xc0\x00\x03\xf0\x18\x00\x0c\x00\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
fb = framebuf.FrameBuffer(obocar_logo, 128, 25, framebuf.MONO_HLSB)
car.OLED.fill(0)
car.OLED.framebuf.blit(fb, 0, 20)
car.OLED.show()


def ble_irq(event, data):
    global received_command
    if event ==3 :  # _IRQ_GATTS_WRITE
        conn_handle, attr_handle = data
        value = ble.gatts_read(attr_handle)
        print(f"Raw value received: {value}")
        try:
            received_command = value.decode('utf-8')
            print(f"Received command: {received_command}")
        except UnicodeDecodeError:
            print(f"Non-UTF-8 command: {value}")
            received_command = value
    elif event == 1:  # _IRQ_CENTRAL_CONNECT
        conn_handle, addr_type, addr = data
        print("Connected by:", addr)
    elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
        conn_handle, addr_type, addr = data
        print("Disconnected from:", addr)
        advertise()
    elif event == 5:  # _IRQ_GATTS_INDICATE_DONE
        print("GATTS indicate done")
    elif event == 6:  # _IRQ_GATTS_READ_REQUEST
        print("GATTS read request")
    else:
        print(f"Unhandled event: {event}, data: {data}")

def advertise():
    
    name = "Obo Car" 
    # Advertisement data: Flags + Complete Local Name + Service UUID (16-bit)
    service_uuid_bytes = bytearray([0xE0, 0xFF])  # 0xFFE0
    adv_data = (
        bytearray(b'\x02\x01\x06') +  # Flags: General discoverable
        bytearray((len(name) + 1, 0x09)) + name.encode() +  # Complete Local Name
        bytearray((len(service_uuid_bytes) + 1, 0x03)) + service_uuid_bytes  # 16-bit Service UUID
    )

    try:
        ble.gap_advertise(100, adv_data=adv_data)
        print(f"Advertising as '{name}' with service UUID: {SERVICE_UUID}")
    except Exception as e:
        print(f"Advertising failed: {e}")

# Initialize BLE
ble = ubluetooth.BLE()
ble.active(True)
time.sleep(0.5)  # Allow BLE to initialize

# Register GATT service and characteristic
ble.irq(ble_irq)
service = (SERVICE_UUID, ((CHAR_UUID, ubluetooth.FLAG_READ | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_WRITE_NO_RESPONSE),),)
try:
    ble.gatts_register_services((service,))
    print(f"GATT services registered: Service UUID: {SERVICE_UUID}, Char UUID: {CHAR_UUID}")
except Exception as e:
    print(f"Failed to register GATT services: {e}")

# Start advertising
advertise()

speed_left_F = speed_right_F = 256
speed_left_B = speed_right_B = 256
# Main loop to process received commands
while True:
    if received_command:
        print(f"Processing command: {received_command}")
        if 'M' in received_command:
            if 'F' in received_command:
                
                if 'L' in received_command:
                    speed_left_F = int(received_command[3:])
                elif 'R' in received_command:
                    speed_right_F = int(received_command[3:])
            elif 'B' in received_command:
                
                
                if 'L' in received_command:
                    speed_left_B = int(received_command[3:])
                elif 'R' in received_command:
                    speed_right_B = int(received_command[3:])
                
        elif received_command == 'F':
            car.move_forward(speed_left=speed_left_F, speed_right=speed_right_F)
        elif received_command == 'B':
            car.move_backward(speed_left_B, speed_right_B)  
        elif received_command == 'L':
            car.turn_left(speed_left_F, speed_right_F)
        elif received_command == 'R':
            car.turn_right(speed_left_F, speed_right_F)
        elif received_command == 'S':
            car.stop()
        elif received_command == 'H':
            car.beep()
        else:
            print(f"Unknown command: {received_command}")
        received_command = None  # Clear command after processing
    time.sleep(0.1)  # Small delay to prevent tight loop

