import socket

s = socket.socket()

port = 52347

s.connect(('127.0.0.1', port))

data = s.recv(1000000000)
filename = 'some_image.jpg'
with open(filename, 'wb') as f:
	f.write(data)
s.close()
