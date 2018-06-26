from pysony import SonyAPI, ControlPoint
import urllib2
import time
import os
import sys
import thread
import shutil
import os
reload(sys)
sys.setdefaultencoding('utf8')

def getImage():

    search = ControlPoint()
    cameras =  search.discover(5)

    if len(cameras):
        camera = SonyAPI(QX_ADDR=cameras[0])

    else:
        print("No camera found, aborting")
        quit()

    mode = camera.getAvailableApiList()
    if 'startRecMode' in (mode['result'])[0]:
        camera.startRecMode()
        time.sleep(2)

    import socket

    s = socket.socket()
    print "Socket successfully created"

    port = 52347

    s.bind(('', port))
    print "socket binded to %s" %(port)

    s.listen(5)
    print "socket is listening"

    while True:

       c, addr = s.accept()
       print 'Got connection from', addr
       toSend = camera.actTakePicture()
       pic_url = toSend['result'][0][0]
       img = urllib2.urlopen(pic_url).read()
       c.send(str(img))
       c.close()
getImage()
