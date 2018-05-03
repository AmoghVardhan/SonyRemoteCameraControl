# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 52345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server
data = s.recv(1000000000)
filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
with open(filename, 'wb') as f:
	f.write(data)
# close the connection
s.close()
