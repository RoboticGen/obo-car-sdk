from machine import Pin
import time
from obocar import OBOCar
import framebuf

speed = 512  # max 512

# Initialize the OBOCar
car = OBOCar()


def get_medium_font_bitmap(char):
    font_bitmaps = {
        'M': bytearray([
        0b11000011,
        0b11100111,
        0b11111111,
        0b11011011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b00000000,
        0b00000000,
        ]),
        'E': bytearray([
        0b11111111,
        0b11111111,
        0b11000000,
        0b11000000,
        0b11000000,
        0b11111110,
        0b11111110,
        0b11000000,
        0b11000000,
        0b11000000,
        0b11000000,
        0b11000000,
        0b11111111,
        0b11111111,
        0b00000000,
        0b00000000,
        ]),
        'N': bytearray([
        0b11000011,
        0b11100011,
        0b11110011,
        0b11011011,
        0b11001111,
        0b11000111,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b00000000,
        0b00000000,
        ]),
        'U': bytearray([
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11000011,
        0b11111110,
        0b01111100,
        0b00000000,
        0b00000000,
        ]),
    }
    return font_bitmaps.get(char)


def draw_medium_text(oled, text, x, y):
    for i, char in enumerate(text):
        bmp = get_medium_font_bitmap(char)
        if bmp is None:
            continue
        fb = framebuf.FrameBuffer(bmp, 8, 16, framebuf.MONO_HLSB)
        oled.framebuf.blit(fb, x + i * 10, y)



# === NEW draw_highlighted_text: highlight full row ===
def draw_highlighted_text(oled, text, x, y, highlight=False):
    text_height = 8
    screen_width = 128

    if highlight:
        # Fill entire row width
        oled.framebuf.fill_rect(0, y - 1, screen_width, text_height + 2, 1)
        oled.text(text, x, y, 0)  # draw black text on white
    else:
        oled.text(text, x, y, 1)  # normal white text

# === Error display ===
def show_error(sensor_name):
    car.OLED.fill(0)
    car.OLED.text("Error in", 20, 20)
    car.OLED.text(sensor_name, 20, 30)
    car.OLED.show()
    time.sleep(2)
    return True

# === Test functions ===
def test_ultrasonic(car):
    time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text("Testing Ultrasonic", 0, 0)
    car.OLED.show()
    time.sleep(0.5)
    
    start_time = time.time()
    duration = 10  # seconds
    
    front_all_zero = True
    left_all_zero = True
    right_all_zero = True
    
    while time.time() - start_time < duration:
        front = car.get_front_distance()
        left = car.get_left_distance()
        right = car.get_right_distance()
        
        if front > 0.0:
            front_all_zero = False
        if left > 0.0:
            left_all_zero = False
        if right > 0.0:
            right_all_zero = False
        
        car.OLED.fill(0)
        car.OLED.text(f"F: {front:.1f}", 0, 48)
        car.OLED.text(f"L: {left:.1f}", 0, 16)
        car.OLED.text(f"R: {right:.1f}", 0, 32)
        car.OLED.show()
        time.sleep(0.5)
    
    # After the test duration, show errors for sensors always zero while showing all distances
    car.OLED.fill(0)
    car.OLED.text(f"F: {front:.1f}", 0, 0)
    car.OLED.text(f"L: {left:.1f}", 0, 16)
    car.OLED.text(f"R: {right:.1f}", 0, 32)
    
        
    if front_all_zero:
        car.OLED.text("Errorf", 70, 48)
        
    if left_all_zero:
        car.OLED.text("ErrorL", 70, 16)
        
    if right_all_zero:
        car.OLED.text("ErrorR", 70,32)
        
        
    car.OLED.show()
    time.sleep(4)
    
    # Return False if any error found, else True
    if front_all_zero or left_all_zero or right_all_zero:
        return False
    
    car.OLED.fill(0)
    car.OLED.text("Done", 40, 20)
    car.OLED.show()
    time.sleep(3)
    return True

  
def test_motor_controller(car):
    time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text("Testing Motors", 0, 0)
    car.OLED.show()
    for i in range(1, 5):
        car.move_forward(300 + 50 * i)
        time.sleep(1)
        car.stop()
        time.sleep(0.5)

    car.OLED.fill(0)
    car.OLED.text("Moving Backward", 10, 10)
    car.move_backward(speed)
    time.sleep(1)
    car.stop()
    time.sleep(0.5)

    car.OLED.fill(0)
    car.OLED.text("Turning Left", 10, 10)
    car.turn_left(speed)
    time.sleep(1)
    car.stop()
    time.sleep(0.5)

    car.OLED.fill(0)
    car.OLED.text("Turning Right", 10, 10)
    car.turn_right(speed)
    time.sleep(1)
    car.stop()
    time.sleep(0.5)

    car.OLED.fill(0)
    car.OLED.text("Done", 40, 20)
    car.OLED.show()
    time.sleep(2)
    return True

def test_buzzer(car):
    time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text("Testing Buzzer", 0, 0)
    car.OLED.show()
    car.start_tone()
    time.sleep(1)
    
    car.OLED.fill(0)
    car.OLED.text("Done", 40, 20)
    car.OLED.show()
    time.sleep(2)
    return True

def test_ir_array(car):
    time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text("Testing IR Array", 0, 0)
    car.OLED.show()
    start_time = time.time()
    duration = 10
    previous_readings = None
    unchanged_start = None
    max_unchanged = 3

    while time.time() - start_time < duration:
        readings = car.ir_array.read_IR()
        if readings is None or any(r is None for r in readings):
            show_error("IR Sensor")
            return False

        if previous_readings is None:
            previous_readings = readings.copy()
            unchanged_start = time.time()
        elif readings == previous_readings:
            if time.time() - unchanged_start >= max_unchanged:
                show_error("IR Sensor")
                return False
        else:
            previous_readings = readings.copy()
            unchanged_start = time.time()

        car.OLED.fill(0)
        for i, (k, v) in enumerate(list(readings.items())[:6]):
            x = (i % 3) * 42
            y = 20 if i < 3 else 40
            car.OLED.text(f"{k}:{v}", x, y)
        car.OLED.show()
        time.sleep(0.5)

    car.OLED.fill(0)
    car.OLED.text("Done", 40, 20)
    car.OLED.show()
    time.sleep(2)
    return True

# === Menu display ===
def show_main_menu(selected):
    car.OLED.fill(0)
    draw_medium_text(car.OLED, "MENU", 40, 0)
    draw_highlighted_text(car.OLED, "1.Test", 10, 20, highlight=(selected == 0))
    draw_highlighted_text(car.OLED, "2.Play", 10, 30, highlight=(selected == 1))
    car.OLED.show()

test_options = [
    ("1.Ultrasonic", test_ultrasonic),
    ("2.Motor Check", test_motor_controller),
    ("3.Buzzer", test_buzzer),
    ("4.IR Array", test_ir_array),
    ("5.Color sensor", test_ir_array)
]

def show_test_menu(selected):
    car.OLED.fill(0)
    draw_medium_text(car.OLED, "MENU", 40, 0)

    max_visible = 4  # Only show 4 options at once
    start_index = 0

    # Scroll window logic
    if selected >= max_visible:
        start_index = selected - max_visible + 1

    for i in range(start_index, min(start_index + max_visible, len(test_options))):
        draw_highlighted_text(car.OLED, test_options[i][0], 10, 20 + (i - start_index) * 10, highlight=(i == selected))

    car.OLED.show()
    
def wait_for_left_button_start():
    car.OLED.fill(0)
    car.OLED.text("Press Left Btn", 10, 20)
    car.OLED.text("to Start Test", 10, 30)
    car.OLED.show()
    # Wait until left button is pressed
    while not car.is_buttonL_pressed():
        time.sleep(0.1)
    # Wait for button release to avoid immediate double press
    while car.is_buttonL_pressed():
        time.sleep(0.1)
   


# === State ===
in_main_menu = True
main_menu_selection = 0
in_test_menu = False
test_menu_selection = 0
play_mode = False

show_main_menu(main_menu_selection)

# === MAIN LOOP ===
try:
    while True:
        time.sleep(0.01)

        if car.is_buttonL_pressed():
            counter = 0
            for i in range(20):
                time.sleep(0.01)
                counter += 1
                if not car.is_buttonL_pressed():
                    break

            if in_main_menu:
                if counter < 20:
                    main_menu_selection = (main_menu_selection - 1) % 2
                    show_main_menu(main_menu_selection)
                else:
                    in_main_menu = False
                    car.OLED.fill(0)
                    car.OLED.show()

            elif in_test_menu:
                if counter < 20:
                    test_menu_selection = (test_menu_selection - 1) % len(test_options)
                    show_test_menu(test_menu_selection)
                else:
                    in_test_menu = False
                    in_main_menu = True
                    show_main_menu(main_menu_selection)

            time.sleep(0.2)

        if car.is_buttonR_pressed():
            counter = 0
            for i in range(20):
                time.sleep(0.01)
                counter += 1
                if not car.is_buttonR_pressed():
                    break

            if in_main_menu:
                if counter < 20:
                    main_menu_selection = (main_menu_selection + 1) % 2
                    show_main_menu(main_menu_selection)
                else:
                    if main_menu_selection == 0:
                        in_main_menu = False
                        in_test_menu = True
                        show_test_menu(test_menu_selection)
                    elif main_menu_selection == 1:
                        play_mode = True
                        in_main_menu = False
                        car.OLED.fill(0)
                        car.OLED.text("Play Mode", 20, 20)
                        car.OLED.show()
                        time.sleep(2)
                        car.OLED.fill(0)
                        car.OLED.show()

            elif in_test_menu:
                if counter < 20:
                    test_menu_selection = (test_menu_selection + 1) % len(test_options)
                    show_test_menu(test_menu_selection)
                else:
                    test_name, test_function = test_options[test_menu_selection]
                    wait_for_left_button_start()
                    result = test_function(car)
                    in_test_menu = True
                    in_main_menu = False
                    show_test_menu(test_menu_selection)


            time.sleep(0.2)

except KeyboardInterrupt:
    car.stop()
    car.OLED.fill(0)
    car.OLED.show()

