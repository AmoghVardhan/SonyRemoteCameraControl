from pysony import SonyAPI, ControlPoint
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def liveview():

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

    #sizes = camera.getLiveviewSize()
    #print('Supported liveview size:', sizes)

    url = camera.liveview()

    lst = SonyAPI.LiveviewStreamThread(url)
    lst.start()
    print('LiveviewStreamThread startedr.')
    # t_end=time.time() + 60*1
    # i=0
    # while time.time()<t_end:
    #     #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    # first of all import the socket library


    import socket

    # next create a socket object
    s = socket.socket()
    print "Socket successfully created"

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 52345

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print "socket binded to %s" %(port)

    # put the socket into listening mode
    s.listen(5)
    print "socket is listening"

    # a forever loop until we interrupt it or
    # an error occurs
    while True:

       # Establish connection with client.
       c, addr = s.accept()
       print 'Got connection from', addr

       # send a thank you message to the client.
       #print c.recv(10000)
       c.send(str(lst.get_latest_view()))
       # Close the connection with the client
       c.close()
    #print lst.get_latest_view()
    #     #print(type(lst.get_latest_view))
    #     i+=1
    # print(i)
    #return lst.get_latest_view
liveview()
