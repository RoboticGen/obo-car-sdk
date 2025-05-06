############################################
# RC_OBO Code
############################################

import bluetooth
import struct
import time
from micropython import const
from obocar import OBOCar
from machine import Pin, PWM

# using oborcar functionalities like move fd, back ...
oboCar = OBOCar()


_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x03)
_ADV_TYPE_UUID32_COMPLETE = const(0x05)
_ADV_TYPE_UUID128_COMPLETE = const(0x07)
_ADV_MAX_PAYLOAD = const(31)


def advertising_payload(name=None, services=None):
    """
    Builds a minimal advertising payload with flags, optional name, and
    optional services (128-bit UUID).
    """
    payload = bytearray()

    def _append(adv_type, value):
        payload.extend(struct.pack("BB", len(value) + 1, adv_type))
        payload.extend(value)

    flags = b"\x04"  # 0x04 = BREDR not supported
    _append(_ADV_TYPE_FLAGS, flags)

    # Device Name
    if name:
        _append(_ADV_TYPE_NAME, name.encode())

    # Optional 128-bit (or 16/32-bit) service UUID(s)
    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, b)
            elif len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    if len(payload) > _ADV_MAX_PAYLOAD:
        raise ValueError(
            "Advertising payload too large ({} bytes)".format(len(payload))
        )

    return payload


#
# --- Nordic UART Service Setup ---
#

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

# Nordic UART Service UUID
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

# TX characteristic (ESP32 -> Phone), Notify
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_NOTIFY,
)

# RX characteristic (Phone -> ESP32), Write
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE,
)

_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


class BLEUART:
    def __init__(self, ble, name="OBo", rxbuf=100):
        """
        :param ble: The bluetooth.BLE() instance
        :param name: Short device name to fit within 31 bytes advertisement
        :param rxbuf: Size of the RX buffer
        """
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)

        # Register the Nordic UART Service
        ((self._tx_handle, self._rx_handle),) = ble.gatts_register_services(
            (_UART_SERVICE,)
        )

        # Increase the RX buffer for the RX characteristic
        ble.gatts_set_buffer(self._rx_handle, rxbuf, True)

        self._connections = set()
        self._rx_buffer = bytearray()
        self._handler = None

        # Build an advertising payload
        #  name "OBO"
        # - 128-bit UART service
        self._payload = advertising_payload(
            name=name,
            services=[_UART_UUID],  # Advertise the 128-bit UART UUID
        )
        self._advertise()

    def irq(self, handler):
        """Set a callback function that is called when data arrives."""
        self._handler = handler

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Central connected:", conn_handle)

        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("Central disconnected:", conn_handle)
            # Re-advertise for new connections
            self._advertise()

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            # If data is being written to our RX characteristic
            if conn_handle in self._connections and value_handle == self._rx_handle:
                self._rx_buffer += self._ble.gatts_read(self._rx_handle)
                if self._handler:
                    self._handler()

    def any(self):
        """Return how many bytes are waiting in the RX buffer."""
        return len(self._rx_buffer)

    def read(self, size=None):
        """Read bytes from the RX buffer."""
        if size is None:
            size = len(self._rx_buffer)
        result = self._rx_buffer[:size]
        self._rx_buffer = self._rx_buffer[size:]
        return result

    def write(self, data):
        """Send data to all connected centrals."""
        if isinstance(data, str):
            data = data.encode()
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def close(self):
        """Disconnect from any centrals and clear connections."""
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)
        self._connections.clear()

    def _advertise(self, interval_us=500000):
        """Start BLE advertising."""
        print("Advertising with payload length:", len(self._payload))
        self._ble.gap_advertise(interval_us, adv_data=self._payload)


#
# --- Main "demo" or "RC" logic ---
#


def ble_car_demo():
    """
    Creates a BLE UART device named "OBO_Car".
    Waits for phone commands:
      F, B, L, R, STOP
    This example doesn't actually move hardware.
    Replace `do_command()` with your real OBOCar or motor control code.
    """
    import bluetooth

    ble = bluetooth.BLE()

    # Use a short name in the advertisement, "OBO", to avoid 31-byte limit.
    # The user-facing name in code can be "OBO_Car" or just "OBO".
    uart = BLEUART(ble, name="OBO")

    # ---------------------------------------------------------------------------------------------------------------
    # The next function must have to be changed accrodring to the RC_Controller (App) you are using
    # This code is compatibale with the controller named Dabble
    # ---------------------------------------------------------------------------------------------------------------
    def on_rx():
        raw_data = (
            uart.read()
        )  # raw_data is a bytes object, e.g. b'\xff\x01\x01\x01\x02\x00\x02\x00'
        print("Raw packet:", raw_data)

        # Check if we have at least 8 bytes
        if len(raw_data) < 8:
            print("Packet too short, ignoring.")
            return

        # If your protocol always starts with 0xFF:
        if raw_data[0] != 0xFF:
            print("Invalid header, ignoring.")
            return

        field6 = raw_data[6]
        field5 = raw_data[5]
        print(field5)
        # Maybe interpret field3 as a "command"
        if field6 == 0x01:
            oboCar.move_forward(speed=200)
        elif field6 == 0x08:
            oboCar.turn_right(speed=200)
        elif field6 == 0x02:
            oboCar.move_backward(speed=200)
        elif field6 == 0x04:
            oboCar.turn_left(speed=200)

        elif field5 == 32:
            PWM(Pin(2)).duty(256)

        else:
            oboCar.stop()
            PWM(Pin(2)).duty(0)

    # Set the RX callback
    uart.irq(handler=on_rx)

    print("BLE RC is running. Connect via phone BLE UART app to 'OBO'.")
    print("Send commands: F, B, L, R, STOP")

    import time

    try:
        while True:
            # Example: send heartbeat every 3 seconds
            uart.write("Car Ready...\n")
            time.sleep(3)
    except KeyboardInterrupt:
        pass

    uart.close()
    print("BLE RC stopped.")


# If run directly, start the demo automatically
if __name__ == "__main__":
    ble_car_demo()
