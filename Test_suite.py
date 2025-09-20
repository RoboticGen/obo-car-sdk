from machine import Pin
import time
from obocar import OBOCar
import framebuf

speed = 300  # max 512

# Initialize the OBOCar
car = OBOCar()

# === Logos ===
roboticgen_logo = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x078\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x06\x03\x80\x00\x00\x00\x00\x00\x00\x07\xfc\x00\x00\xf0\x00\x00\x0e\x07\x80\x00\x0f\x80\x00\x00\x00\x07\xfe\x00\x00p\x00\x00\x0e\x07\x80\x00?\xe0\x00\x00\x00\x07\xff\x00\x00p\x00\x00\x0e\x03\x00\x00\x7f\xe0\x00\x00\x00\x07\x07\x80\x00`\x00\x00\x0e\x00\x00\x00\xf0`\x00\x00\x00\x07\x03\x83\xf0\x7f\xc0~\x1f\xf3\x87\xe1\xe0\x00|\x07\xc0\x07\x01\xc7\xf8\x7f\xe0\xff\x1f\xf3\x8f\xf9\xc0\x01\xff?\xe0\x07\x01\xcf\xfc\x7f\xf1\xff\x9f\xf3\x9f\xf9\xc0\x01\xef?\xf0\x07\x01\xde\x1exs\xc3\x8e\x03\x9c1\x80\x03\x8e<p\x07\x03\x9c\x0eps\x81\xce\x03\x9c\x01\x80s\x9e88\x07\x8f\x9c\xcew;\x99\xce\x03\xb8\x01\xc0s\x1c88\x07\xff\x1c\xcec3\x99\xce\x03\xb8\x01\xc0s888\x07\xfe\x1c\x0eps\x81\xce\x03\xbc\x01\xe0s\xf088\x07\xfe\x1e\x1cx\xf3\xc3\x87\x03\x9e0\xf0s\xe288\x07\x0e\x0f\xfc?\xf1\xff\x87\xf3\x9f\xf8\x7f\xf1\xff88\x07\x07\x07\xf8?\xe0\xff\x03\xf3\x8f\xf8?\xe0\xff88\x07\x07\x03\xf0\x0f\x80~\x01\xf3\x83\xe0\x1f\xc0|\x180\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
obocar_logo = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<\x00\x7f\x06\x00\x0f\x80\x00\x01\xe0\x00\x1c\x0f\xfe\x00\x01\xff\x80~\x07\x00\x7f\xe0\x00\x0f\xfc\x00\x1c\x0f\xff\x80\x03\x00\xc0`\x01\x80\xe00\x00\x18\x06\x004\x00\x00\xc0\x06\x00``\x00\x81\x80\x18\x000\x03\x00&\x00\x00`\x0c\x000`\x00\xc3\x00\x0c\x00`\x01\x80b\x00\x00 \x08\x00\x10`\x00\xc2\x00\x06\x10@\x00\xc0C\x00\x000\x18\x00\x18`\x00\xc6\x00\x02\x00\xc0\x00\x00\xc1\x00\x000\x108\x08`\x01\x86\x00\x02\x00\x80\x00\x00\x81\x80\x000\x10|\x08`\x03\x84\x00\x03\x00\x80\x00\x01\x80\x80\x000\x10~\x08`?\x04\x00\x03\x00\x80\x00\x01\x80\xc0\x000\x10|\x08`\x03\x04\x00\x03\x00\x80\x00\x01\x00\xc0\x00\x00\x10<\x08`\x01\x86\x00\x02\x00\x80\x00\x03\x00@\xc0\x00\x10\x18\x18`\x00\x86\x00\x02\x00\xc0\x00\x02\x00``\x00\x18\x00\x18`\x00\xc2\x00\x06\x10@\x00\x86\x00 8\x00\x0c\x000`\x00\xc3\x00\x04\x10`\x01\x84\x000\x1c\x00\x04\x00``\x00\xc1\x80\x0c\x000\x01\x0c\x00\x10\x06\x00\x07\x00\xc0`\x01\x80\xc08\x00\x18\x07\x0c\x00\x18\x03\x00\x01\xc3\x80`\x03\x00p\xf0\x00\x0e\x1c\x08\x00\x08\x01\x80\x00~\x00`>\x00\x1f\xc0\x00\x03\xf0\x18\x00\x0c\x00\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

fb = framebuf.FrameBuffer(roboticgen_logo, 128, 33, framebuf.MONO_HLSB)
car.OLED.framebuf.blit(fb, 0, 14)
car.OLED.show()

car.start_tone()

fb = framebuf.FrameBuffer(obocar_logo, 128, 25, framebuf.MONO_HLSB)
car.OLED.fill(0)
car.OLED.framebuf.blit(fb, 0, 20)
car.OLED.show()
time.sleep(2)

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

def draw_highlighted_text(oled, text, x, y, highlight=False):
    text_height = 8
    screen_width = 128
    if highlight:
        oled.framebuf.fill_rect(0, y - 1, screen_width, text_height + 2, 1)
        oled.text(text, x, y, 0)
    else:
        oled.text(text, x, y, 1)

def show_error(sensor_name):
    car.OLED.fill(0)
    car.OLED.text("Error in", 20, 20)
    car.OLED.text(sensor_name, 20, 30)
    car.OLED.show()
    time.sleep(2)
    return True

def check_ultrasonic_connections(car):
    sensors = {
        "Front_US": car.ultrasonic,
        "Left_US": car.ultrasonicL,
        "Right_US": car.ultrasonicR
    }
    for name, sensor in sensors.items():
        valid_count = 0
        for _ in range(20):
            try:
                dist = sensor.distance_cm()
                if 2 <= dist <= 400:
                    valid_count += 1
            except OSError:
                pass
            time.sleep(0.03)
        car.OLED.fill(0)
        if valid_count >= 15:
            car.OLED.text(f"{name}", 30, 20)
            car.OLED.text(f"works", 40, 30)
            
            
        else:
            car.OLED.text(f"Error", 40, 20)
            car.OLED.text(f"{name} ", 30, 30)
            
        car.OLED.show()
        time.sleep(4)

def test_ultrasonic(car):
    time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text("Testing US", 18, 25)
    car.OLED.show()
    time.sleep(0.5)
    check_ultrasonic_connections(car)
    car.OLED.fill(0)
    car.OLED.text("Done", 40, 20)
    car.OLED.show()
    time.sleep(2)

def test_motor_controller(car):
    time.sleep(0.5)
    car.OLED.fill(0)    
    car.OLED.text("Speeding", 30, 20)
    car.OLED.text("Up", 50, 30)
    car.OLED.show()
    for i in range(1, 3):
        car.move_forward(200 + 50 * i)
        time.sleep(1)
        car.stop()
        time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text("Moving", 35, 20)
    car.OLED.text("Backward", 30, 30)
    car.OLED.show()
    car.move_backward(speed)
    time.sleep(1)
    car.stop()
    time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text("Turning Left", 20, 25)
    car.OLED.show()
    car.turn_left(speed)
    time.sleep(1)
    car.stop()
    time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text("Turning Right", 20, 25)
    car.OLED.show()
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
    car.OLED.text("Testing", 30, 20)
    car.OLED.text("Buzzer", 35, 30)
    car.OLED.show()
    car.start_tone()
    time.sleep(1)
    car.OLED.fill(0)
    car.OLED.text("Done", 40, 20)
    car.OLED.show()
    time.sleep(2)
    return True

def draw_rect(oled, x, y, width, height, color):
    for i in range(height):
        for j in range(width):
            oled.pixel(x + j, y + i, color)


import time

def draw_rect(oled, x, y, width, height, color):
    """
    Draw a filled rectangle on the OLED display.
    """
    for i in range(height):
        for j in range(width):
            if 0 <= x + j < oled.width and 0 <= y + i < oled.height:
                oled.pixel(x + j, y + i, color)

# Test IR sensors by comparing readings with black and white paper
# Test IR sensors by comparing readings with black and white paper
def test_ir_sensors(car):
    """
    Test the IR sensor array by prompting the user to place black paper under the IR array,
    collect 30 readings while displaying a real-time bar chart, then place white paper and
    collect another 30 readings with the bar chart. Check if readings within each instance
    are consistent (max - min <= 100) and if the average readings differ significantly
    between black and white paper (difference > 100). Display 'Sensor [i] works' if both
    conditions are met, otherwise 'Error in Sensor [i]'. Sensors are tested and displayed
    in numerical order (1, 2, 3, 4, 5, 6).
    """
    start_x = 10
    start_y = 0
    bar_width = 8
    spacing = 12
    y_bottom = 64          # Bottom of OLED
    y_top_limit = 28       # Maximum bar height reaches this y
    max_bar_height = y_bottom - y_top_limit  # = 43

    # Prompt for black paper
    time.sleep(0.5)
    car.OLED.fill(0)
    car.OLED.text(f"Place", 40, 20)
    car.OLED.text(f"Black Paper", 20, 30)
    car.OLED.text(f"Under IR Array", 10, 40)
    car.OLED.show()
    time.sleep(5)
    car.OLED.fill(0)
    

    # Get IR sensor labels and sort them numerically
    ir_sensors = sorted(car.ir_panel.ir_sensors.keys(), key=int)  # e.g., ['1', '2', '3', '4', '5', '6']
    
    # Dictionary to store readings for each sensor
    black_readings = {sensor: [] for sensor in ir_sensors}
    

    for i in range(30):
        draw_rect(car.OLED, 0, start_y, 128, y_bottom - start_y, 0)  # Clear OLED region

        for sensor_label in ir_sensors:
            try:
                value = car.get_ir_sensor(sensor_label)
                if value is None:
                    raise ValueError("Sensor returned None")

                black_readings[sensor_label].append(value)

                # Calculate bar height
                bar_height = max(1, int((value / 1024) * max_bar_height))
                x = start_x + ir_sensors.index(sensor_label) * spacing
                y_top = y_bottom - bar_height  # Bar grows upward

                # Draw sensor label at top and vertical bar below it
                car.OLED.text(f"Sensor_No", 30, 0)
                car.OLED.text(f"{sensor_label}", x+20, 20)
                draw_rect(car.OLED, x+20, y_top, bar_width, bar_height, 1)

            except Exception:
                x = start_x + ir_sensors.index(sensor_label) * spacing
                car.OLED.text(f"S{sensor_label} Err", x, 0)

        car.OLED.show()
        time.sleep(0.04)

    # Prompt for white paper
    car.OLED.fill(0)
    car.OLED.text(f"Place", 40, 20)
    car.OLED.text(f"White Paper", 20, 30)
    car.OLED.text(f"Under IR Array", 10, 40)
    car.OLED.show()
    time.sleep(5)
    car.OLED.fill(0)
    


    # Dictionary to store readings for white paper
    white_readings = {sensor: [] for sensor in ir_sensors}


    for i in range(30):
        draw_rect(car.OLED, 0, start_y, 128, y_bottom - start_y, 0)  # Clear OLED region

        for sensor_label in ir_sensors:
            try:
                value = car.get_ir_sensor(sensor_label)
                if value is None:
                    raise ValueError("Sensor returned None")

                white_readings[sensor_label].append(value)

                # Calculate bar height
                bar_height = max(1, int((value / 1024) * max_bar_height))
                x = start_x + ir_sensors.index(sensor_label) * spacing
                y_top = y_bottom - bar_height  # Bar grows upward

                # Draw sensor label at top and vertical bar below it
                car.OLED.text(f"Sensor_No",30, 0)
                car.OLED.text(f"{sensor_label}", x+20, 20)
                draw_rect(car.OLED, x+20, y_top, bar_width, bar_height, 1)

            except Exception:
                x = start_x + ir_sensors.index(sensor_label) * spacing
                car.OLED.text(f"S{sensor_label} Err", x, 0)

        car.OLED.show()
        time.sleep(0.04)


    # Check consistency and difference for each sensor
    for sensor_label in ir_sensors:
        is_valid = True
        black_vals = black_readings[sensor_label]
        white_vals = white_readings[sensor_label]

            # Check consistency within each instance (max - min <= 100)
        black_consistent = (max(black_vals) - min(black_vals)) <= 100
        white_consistent = (max(white_vals) - min(white_vals)) <= 100
            # Check if average readings differ significantly (difference > 100)
        black_avg = sum(black_vals) / len(black_vals) if black_vals else 0
        white_avg = sum(white_vals) / len(white_vals) if white_vals else 0
        diff_valid = abs(white_avg - black_avg) > 100
        print(f"Sensor {sensor_label} Black Avg: {black_avg:.2f}, White Avg: {white_avg:.2f}")
            # Sensor is valid only if both instances are consistent and averages differ
        is_valid = black_consistent and white_consistent and diff_valid

        # Display result for the current sensor
        car.OLED.fill(0)
        if is_valid:
            car.OLED.text(f"Sensor {sensor_label}", 30, 20)
            car.OLED.text("works", 40, 30)
        else:
            car.OLED.text("Error in", 30, 20)
            car.OLED.text(f"Sensor {sensor_label}", 30, 30)
        car.OLED.show()
        time.sleep(4)

    car.OLED.fill(0)
    car.OLED.text("Done", 40, 20)
    car.OLED.show()
    time.sleep(2)
    return True

def show_main_menu(selected):
    car.OLED.fill(0)
    draw_medium_text(car.OLED, "MENU", 40, 0)
    draw_highlighted_text(car.OLED, "1.Test", 30, 20, highlight=(selected == 0))
    draw_highlighted_text(car.OLED, "2.Play", 30, 30, highlight=(selected == 1))
    car.OLED.show()

test_options = [
    ("1.Ultrasonic", test_ultrasonic),
    ("2.Motor Check", test_motor_controller),
    ("3.Buzzer", test_buzzer),
    ("4.IR Array", test_ir_sensors),
    ("5.Sensor_1", test_buzzer)
]

def show_test_menu(selected):
    car.OLED.fill(0)
    draw_medium_text(car.OLED, "MENU", 40, 0)
    max_visible = 4
    start_index = 0
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
    while not car.is_buttonL_pressed():
        time.sleep(0.1)
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



