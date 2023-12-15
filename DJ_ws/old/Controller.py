import sys
import evdev
import serial
from evdev import InputDevice, ecodes, categorize

# UART 설정
uart_port = '/dev/ttyACM0'
uart_baudrate = 115200

# 시리얼 포트 초기화
ser = serial.Serial(uart_port, uart_baudrate)

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
count = 0

for device in devices:
    print(device.path, device.name, device.phys)
    if device.name.startswith('Logitech'):
        controller = InputDevice(device.path)
        count = 1
        break

if count < 1:
    print("No Controller found")
    sys.exit()

motorState = "Stop"
for event in device.read_loop():
    if event.type == ecodes.EV_ABS:
        absEvent = categorize(event)

        if ecodes.bytype[absEvent.event.type][absEvent.event.code] == "ABS_HAT0X":
            if absEvent.event.value == -1:
                motorState = "Left"
            elif absEvent.event.value == 1:
                motorState = "Right"
            elif absEvent.event.value == 0:
                motorState = "Stop"
        elif ecodes.bytype[absEvent.event.type][absEvent.event.code] == "ABS_HAT0Y":
            if absEvent.event.value == -1:
                motorState = "Go"
            elif absEvent.event.value == 1:
                motorState = "Back"
            elif absEvent.event.value == 0:
                motorState = "Stop"
                
        print(motorState)

        if motorState == "Go":
            axisUARTMessage = "v 0 -2\nv 1 2\n"
        elif motorState == "Back":
            axisUARTMessage = "v 0 2\nv 1 -2\n"
        elif motorState == "Left":
            axisUARTMessage = "v 0 -2\nv 1 0\n"
        elif motorState == "Right":
            axisUARTMessage = "v 0 0\nv 1 2\n"       
        elif motorState == "Stop":
            axisUARTMessage = "v 0 0\nv 1 0\n"
        
        # 모터 상태를 UART로 전송
        ser.write(axisUARTMessage.encode())

