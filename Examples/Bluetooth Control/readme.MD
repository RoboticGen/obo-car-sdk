
# OBOCar Bluetooth Controller

This repository contains the code and instructions for controlling your **OBOCar** via Bluetooth using a **gamepad-style** interface. The right-hand buttons include movement controls and a horn (square icon), while the left-hand directional pad (D-pad) allows for forward, backward, left, and right movements.

## Features

1. **Movement Controls**  
   - **Up / Down / Left / Right**: Move the OBOCar in the corresponding direction.  
   - **Square Icon**: Triggers the **horn**.  
   - Additional icons (triangle, circle, cross, etc.) can also be mapped for custom actions if desired.

2. **App Integration**  
   - We use the **[Dabble App](https://play.google.com/store/apps/details?id=io.dabbleapp)** for the Bluetooth-based controller.  
   - Once installed, you can use the Dabble “Gamepad” module or interface to connect to the OBOCar’s BLE service and send button commands directly.

3. **Easy Setup**  
   - **BLE** (Bluetooth Low Energy) connection from your phone/tablet to the ESP32-based OBOCar.  
   - Simple ASCII or binary commands can be mapped to each button for custom motor or horn logic.

## Getting Started

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/obo-car/OBOCar Bluetooth Controller.git
   ```
2. **Upload the Code** to your ESP32 device (using [Thonny](https://thonny.org/) or another MicroPython-friendly tool).
3. **Open the Dabble App** on your phone or tablet:
   - Install from [this link](https://play.google.com/store/apps/details?id=io.dabbleapp) if not already installed.
   - Enable Bluetooth and **connect** to the OBOCar’s BLE service.
   - Select the **Gamepad** interface (or the relevant module).
4. **Press the Buttons**:
   - The **D-Pad** (arrows) controls forward/backward/left/right movement.
   - The **Square** icon triggers the **horn**.
   - Other icons on the right side (Triangle, Circle, X) can also be customized if needed.

![WhatsApp Image 2025-01-13 at 16 30 53_47854e11](https://github.com/user-attachments/assets/3b21763c-9e5a-4d66-b248-1d211155ac3d)


<details>
<summary>Sample Gamepad Layout</summary>

![Gamepad Layout]

- **Square** = Horn  
- **Triangle, Circle, X** = Additional movement or custom actions  
- **D-Pad** = Basic directional controls  

</details>

## Contributing

Feel free to open **issues** or create **pull requests** if you have suggestions or want to add features (e.g., new button mappings, additional BLE services, sensor feedback, etc.).

**Enjoy controlling your OBOCar via a BLE gamepad interface!** 
