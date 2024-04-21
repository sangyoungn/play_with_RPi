import serial

uart = serial.Serial('/dev/ttyUSB0', baudrate=115200, rtscts=True)

with open('./LICENSE') as in_file:
    for line in in_file.read():
        uart.write(line.encode('utf-8'))

print('Send complete')

uart.close()