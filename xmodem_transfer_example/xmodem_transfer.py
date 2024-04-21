# @file xmodem_transfer.py

'''
Package Check
'''
import pkg_resources
try:
    xmodem_package_version = pkg_resources.get_distribution("xmodem").version
    if xmodem_package_version < "0.4.6":
        print("You might need xmodem package whose version is 0.4.6 or higher.")
except:
    print("xmodem package is required.")
    exit(1)
try:
    pyserial_package_version = pkg_resources.get_distribution("pyserial").version
    if pyserial_package_version < "3.5":
        print("You might need pyserial package whose version is 3.5 or higher.")
except:
    print("pyserial package is required.")
    exit(1)

'''
Implementation
'''
import serial
import xmodem

class XmodemTransfer():
    '''
    Class to initialize the XMODEM file transfer

    Usage: 
      modem = XmodemTransfer('/dev/ttyUSB0')
    '''
    def __init__(self, portname:str):
        self.port = None

        if portname == None:
            raise ValueError('portname must be specified.')

        if not (isinstance(portname, str)):
            raise TypeError('Wrong type of arguments')

        try:
            '''
            Initialize a serial port with 115200 bps of the datarate,
            8 bits of the data size, none parity, and one stopbit.
            '''
            self.port = serial.Serial(portname, 
                                      baudrate=115200, 
                                      bytesize=serial.EIGHTBITS,
                                      parity=serial.PARITY_NONE,
                                      stopbits=serial.STOPBITS_ONE,
                                      rtscts=True)
        except serial.SerialException:
            print('Check the port name again.')
            raise ValueError

    def __del__(self):
        if self.port != None:
            self.port.close()

    def _getc(self, size, timeout=3):
        '''
        A method to get a byte from a port for the XMODEM operation
        '''
        return self.port.read(size) or None

    def _putc(self, data, timeout=3):
        '''
        A method to put a byte to a port for the XMODEM operation
        '''
        return self.port.write(data) or None


    class Send():
        '''
        Class to transmit a file

        Usage:
          transfer = modem.Send(modem, '/home/pi/test.file')
          transfer.report()
        '''
        def __init__(self, outter_instance, filepath:str, verbose=False):
            self.transfer_channel_instance = outter_instance
            self.verbose = verbose
            self.status = False
            self.total_packets = 0
            self.success_count = 0
            self.error_count = 0

            try:
                self.source = open(filepath, 'rb')
            except:
                raise ValueError('Cannot open the file.')
            
            self._send()
                      
        def __del__(self):
            if self.source != None:
                self.source.close()

        def _callback(self, total_packets, success_count, error_count):
            if self.verbose:
                print(f'Tx: Success {success_count} and Error {error_count} out of {total_packets} packets')
            self.total_packets = total_packets
            self.success_count = success_count
            self.error_count = error_count

        def _send(self):
            self.modem = xmodem.XMODEM(self.transfer_channel_instance._getc, 
                                       self.transfer_channel_instance._putc, 
                                       pad=b'\x00')
            self.status = self.modem.send(self.source, callback=self._callback)

        def report(self):
            print(f'Result: Success {self.success_count} and Error {self.error_count} out of {self.total_packets} packets')
            print(f'File transmission {"succeeded." if self.status else "failed."}')

            return self.status

    class Receive():
        '''
        Class to receive a file

        Usage:
          transfer = modem.Receive(modem, '/home/pi/test.rcv')
          transfer.report()
        '''
        def __init__(self, outter_instance, filepath:str, verbose=False):
            self.transfer_channel_instance = outter_instance
            self.verbose = verbose
            self.status = False
            self.total_packets = 0
            self.success_count = 0
            self.error_count = 0

            try:
                self.dest = open(filepath, 'wb')
            except:
                raise SystemError('Cannot create a file.')
            
            self._rcv()
          
        def __del__(self):
            if self.dest != None:
                self.dest.close()

        def _callback(self, total_packets, success_count, error_count, packet_size):
            if self.verbose:
                print(f'Rx: Success {success_count} and Error {error_count} out of {total_packets} packets, Packet Size {packet_size}')
            self.total_packets = total_packets
            self.success_count = success_count
            self.error_count = error_count

        def _rcv(self):
            self.modem = xmodem.XMODEM(self.transfer_channel_instance._getc, 
                                       self.transfer_channel_instance._putc)
            
            if xmodem_package_version >= "0.4.7":
                self.success_bytes = self.modem.recv(self.dest, callback=self._callback)
            else:
                self.success_bytes = self.modem.recv(self.dest)
            self.status = True if self.success_bytes != None else False

        def report(self):
            if xmodem_package_version >= "0.4.7":
                print(f'Result: Success {self.success_count} and Error {self.error_count} out of {self.total_packets} packets')
            print(f'Result: {self.success_bytes} received.')
            print(f'File reception {"succeeded." if self.status else "failed."}')

            return self.status
   
if __name__ == '__main__':
    '''
    usage: xmodem_transfer.py [-h] -p [port] -m [T or R] -f [path] [-v]

    XMODEM File Transfer through Serial Port

    options:
    -h, --help            show this help message and exit
    -p [port], --port [port]
                            Serial Port for File Transfer
    -m [T or R], --mode [T or R]
                            Transmit or Receive
    -f [path], --filepath [path]
                            File Path to Read from for Transmission or Write to
                            for Reception
    -v, --verbose         Verbose mode
    '''
    import argparse

    opts_parser = argparse.ArgumentParser(description='XMODEM File Transfer through Serial Port')
    opts_parser.add_argument('-p', '--port', nargs='?', metavar='port', type=str, required=True, help='Serial Port for File Transfer')
    opts_parser.add_argument('-m', '--mode', nargs='?', metavar='T or R', choices=['T', 'R'], required=True, help='Transmit or Receive')
    opts_parser.add_argument('-f', '--filepath', nargs='?', metavar='path', type=str, required=True, 
                             help='File Path to Read from for Transmission or Write to for Reception')
    opts_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    args = opts_parser.parse_args()

    '''
    Start transfer per the command line options.    
    '''
    modem = XmodemTransfer(args.port)

    if args.mode == 'T':
        operation = modem.Send(modem, args.filepath, verbose=True if args.verbose else False)
    else:
        operation = modem.Receive(modem, args.filepath, verbose=True if args.verbose else False)

    '''
    Print the final result and return with a exit code depending on the final error result. 
    The report() method returns True in case of no error and Fales in case of any error.
    '''
    if(operation.report()):
        exit(0)
    exit(1)
