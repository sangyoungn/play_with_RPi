import serial

uart = serial.Serial('/dev/ttyAMA2', baudrate=115200, rtscts=True)

while True:
    byte = uart.read()
    print(byte.decode("utf-8"), end='')

uart.close()