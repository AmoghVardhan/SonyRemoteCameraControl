from pysony import SonyAPI, ControlPoint
import time
import base64
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
    t_end=time.time() + 60*1
    i=0
#    while time.time()<t_end:
        #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print lst.get_latest_view()
        #print(type(lst.get_latest_view))
 #       i+=1
    print(i)
    #return lst.get_latest_view
liveview()

'''  add this in ground station code
filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(lst.get_latest_view())
'''
