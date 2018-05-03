#this code wxtracts gps,height,heading etc data from a mavlink stream 
import sys
import array
import struct
import serial
PORT='/dev/ttyUSB0'                     # typical mac port
BAUD=57600                         # baud rate for radio connection

#-----------------------------------------------------------------------
# manifest constants
#-----------------------------------------------------------------------

MAV_STARTB=0xfe      # this byte indicates start of mavlink packet
xdumpf=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
def xdump(src, length=16):
    """dump a string in classic hexdump format
       adapted from http://code.activestate.com/recipes/142812-hex-dumper
    """
    STREAM=''
    N=0;
    while src:
        s,src = src[:length],src[length:]
        hexa = ' '.join(["%02X"%ord(x) for x in s])
        s = s.translate(xdumpf)
        STREAM+=hexa
        print "%04X   %-*s   %s" % (N, length*3, hexa, s)
        N+=length
    extractgps(STREAM)


def extractgps(STREAM):
    height=STREAM[74]+STREAM[75]+STREAM[71]+STREAM[72]+STREAM[68]+STREAM[69]+STREAM[65]+STREAM[66]
    lat=STREAM[39]+STREAM[40]+STREAM[36]+STREAM[37]+STREAM[33]+STREAM[34]+STREAM[30]+STREAM[31]
    lon=STREAM[50]+STREAM[51]+STREAM[47]+STREAM[48]+STREAM[45]+STREAM[46]+STREAM[42]+STREAM[43]
    print lat
    print lon
    print height
    height=int(height,16)
    lat=int(lat,16)
    lon=int(lon,16)
    print('%d')%(height)
    if STREAM[74]=='F':
            height=str(twos_comp(height, 32))
            height=float(height)
            print('%f meters')%(height/1000)  
    else:
        height=float(height)
        print('%f meters')%(height/1000)
    if STREAM[39]=='F':
        lat=str(twos_comp(lat, 32))
        lat=float(lat)
        print('the latitude is %f degrees')%(lat/10000000)
    else:
        lat=float(lat)
        print('the latitude is %f degrees')%(lat/10000000)    
    if STREAM[50]=='F':
            lon=str(twos_comp(lon, 32))
            lon=float(lon)
            print('the longitude is %f meters')%(lon/10000000)
    else:
        lon=float(lon)
        print('the longitude is %f degrees')%(lon/10000000)

def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is
#-----------------------------------------------------------------------
# checksum special note:
#
# each message type (0,1,2,...) has an extra one-byte magic number.
# heartbeat (message 0) has magic number of 50, so you can index this
# table with the message number to get the magic number.  After
# accumulating the bytes of the message, accumulate the magic number.
# this table is copied from the mavlink source.
#-----------------------------------------------------------------------

MAVLINK_MESSAGE_CRCS=[
  50,124,137,0,237,217,104,119,0,0,0,89,0,0,0,0,0,0,0,0,214,159,220,168,
  24,23,170,144,67,115,39,246,185,104,237,244,222,212,9,254,230,28,28,
  132,221,232,11,153,41,39,214,223,141,33,15,3,100,24,239,238,30,240,183,
  130,130,0,148,21,0,243,124,0,0,0,20,0,152,143,0,0,127,106,0,0,0,0,0,0,
  0,231,183,63,54,0,0,0,0,0,0,0,175,102,158,208,56,93,0,0,0,0,235,93,124,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,42,
  241,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,204,49,
  170,44,83,46,0]

#-----------------------------------------------------------------------
class x25crc(object):
    """x25 CRC - based on checksum.h from mavlink library"""

    def __init__(self, buf=''):
        self.crc = 0xffff
        self.accumulate(buf)

    def accumulate(self, buf):
        '''add in some more bytes'''
        bytes = array.array('B')
        if isinstance(buf, array.array):
            bytes.extend(buf)
        else:
            bytes.fromstring(buf)
        accum = self.crc
        for b in bytes:
            tmp = b ^ (accum & 0xff)
            tmp = (tmp ^ (tmp<<4)) & 0xFF
            accum = (accum>>8) ^ (tmp<<8) ^ (tmp<<3) ^ (tmp>>4)
            accum = accum & 0xFFFF
        self.crc = accum

#-----------------------------------------------------------------------
def decode2(buf):
    """decode and process a command"""
    # we don't do anything here
    pass

#-----------------------------------------------------------------------
lastseq=255
def decode(buf):
    """decode a mavlink message"""

    global lastseq
    
    
    magic, mlen, seq, srcSystem, srcComponent, msgId = struct.unpack('<6B', buf[:6])
    b0,b1=struct.unpack('2B',buf[6+mlen:])
    
    givenCk=b0+b1*256
    crc=x25crc()
    crc.accumulate(buf[1:len(buf)-2]) # skip magic and cksum
    crc.accumulate(chr(MAVLINK_MESSAGE_CRCS[msgId]))
    if msgId==33:
        if crc.crc==givenCk:
            print '-----------'
            xdump(buf)
            print 'mlen=%d, seq=%d, sys=(%d,%d), msgId=%d, sums=(%04x,%04x)'%\
                  (mlen,seq,srcSystem,srcComponent,msgId,givenCk,crc.crc)

            if crc.crc == givenCk:
                # good message, process it
                if seq != (lastseq+1)%256:
                    print 'WARNING, lost message? seq=%d,lastseq=%d'%(seq,lastseq)
                lastseq=seq
                decode2(buf)
            else:
                # complain!
                print 'BAD CRC on message'
        

#-----------------------------------------------------------------------
def timedread(ser,n):
    """read octets, complain upon timeout"""

    while True:
        x = ser.read(n)
        if len(x) == 0:
            print "TIMEOUT"
        else:
            return x

#-----------------------------------------------------------------------
def process(ser):
    """process the mavlink input stream"""

    while True:
        # scan stream until we see sync byte
        x = timedread(ser,1)
        if ord(x) == MAV_STARTB:
            #  read the length and rest of message, and process
            len=timedread(ser,1)
            rest=timedread(ser,4+ord(len)+2)
            buf=x
            buf+=len
            buf+=rest
            decode(buf)

#-----------------------------------------------------------------------
def connect():
    """connect to the mavlink device"""

    autoselect=1

    # here's some autoselect logic for mac
    if autoselect and sys.platform == 'darwin':
        import glob
        candidates=glob.glob('/dev/tty*usb*')
        print 'candidate ports (%d):'%(len(candidates))
        for c in candidates:
            print '   ',c
        myport=candidates[0]
        mybaud=57600
        mybaud=115200
    else:
        myport=PORT
        mybaud=BAUD

    print 'connecting to:', myport
    ser = serial.Serial()
    ser.port=myport
    ser.baudrate=mybaud
    ser.parity=serial.PARITY_NONE
    ser.stopbits=serial.STOPBITS_ONE
    ser.bytesize=serial.EIGHTBITS
    ser.timeout=2
    ser.open()
    return ser

#-----------------------------------------------------------------------
def main():
    """the main thing!"""

    ser=connect()
    print 'STARTING'
    process(ser)

#-----------------------------------------------------------------------
if __name__=="__main__":
    main()
