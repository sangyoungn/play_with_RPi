import serial
import xmodem

ser = serial.Serial('/dev/ttyUSB0', 
                    baudrate=115200, 
                    bytesize=serial.EIGHTBITS, 
                    parity = serial.PARITY_NONE, 
                    stopbits=serial.STOPBITS_ONE, 
                    rtscts=True)

def getc(size, timeout=1):
    return ser.read(size) or None

def putc(data, timeout=1):
    return ser.write(data) or None

modem = xmodem.XMODEM(getc, putc, pad=b'\00')

with open('./LICENSE', "rb") as source_file:
    result = modem.send(source_file)

if result == True:
    print("File transferred successfully.")

ser.close()