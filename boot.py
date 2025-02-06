from machine import Pin
import time
from obocar import OBOCar
import framebuf
from logos import ROBOTICGEN_LOGO, OBOCAR_LOGO

speed = 512 #max 512

# Initialize the OBOCar
car = OBOCar()

fb = framebuf.FrameBuffer(ROBOTICGEN_LOGO, 128, 33, framebuf.MONO_HLSB)
car.OLED.framebuf.blit(fb, 0, 14)
car.OLED.show()

car.start_tone()

fb = framebuf.FrameBuffer(OBOCAR_LOGO, 128, 25, framebuf.MONO_HLSB)
car.OLED.fill(0)
car.OLED.framebuf.blit(fb, 0, 20)
car.OLED.show()


try:
    toggleFlag = 0
    while True:
        print(f"Front - {car.get_front_distance()} Left - {car.get_left_distance()} Right - {car.get_right_distance()}")
        time.sleep(0.01)
        if(car.is_buttonL_pressed()):
            counter = 0
            for i in range(0,10):
                time.sleep(0.01)
                counter += 1
                print(counter)
                if(car.is_buttonL_pressed() == False):
                    break
            
            if(counter >= 9):
                toggleFlag = not toggleFlag
                car.display(str(toggleFlag), 35, 20)
                time.sleep(0.5)
                
        if(toggleFlag == 1):
            
            print("Moving Forward")
            car.move_forward(speed)
            time.sleep(1)  # Move forward for 2 seconds
            
            print("Stopping")
            car.stop()
            time.sleep(1)  # Stop for 1 second

            print("Moving Backward")
            car.move_backward(speed)
            time.sleep(1)  # Move backward for 2 seconds
            
            print("Stopping")
            car.stop()
            time.sleep(1)  # Stop for 1 second
            
            print("Turning Left")
            car.turn_left(speed)
            time.sleep(1)  # Move forward for 2 seconds
            
            print("Stopping")
            car.stop()
            time.sleep(1)  # Stop for 1 second

            print("Turning Right")
            car.turn_right(speed)
            time.sleep(1)  # Move backward for 2 seconds
            
            print("Stopping")
            car.stop()
            time.sleep(1)  # Stop for 1 second

except KeyboardInterrupt:
    print("Stopping the car.")
    car.stop()  # Ensure the car stops when interrupted









