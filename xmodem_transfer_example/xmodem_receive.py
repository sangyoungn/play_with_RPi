import serial
import xmodem

ser = serial.Serial('/dev/ttyAMA2', 
                    baudrate=115200, 
                    bytesize=serial.EIGHTBITS, 
                    parity = serial.PARITY_NONE, 
                    stopbits=serial.STOPBITS_ONE, 
                    rtscts=True)

def getc(size, timeout=1):
    return ser.read(size) or None

def putc(data, timeout=1):
    return ser.write(data) or None

modem = xmodem.XMODEM(getc, putc)

with open('./RECEIVED_FILE', "wb") as destination_file:
    result = modem.recv(destination_file)

if result != None:
    print(f"{result} bytes have been received successfully.")

ser.close()