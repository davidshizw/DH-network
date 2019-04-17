from socket import *
import sys
import time
import logging

#define host port and bufferSize
serverName = "127.0.0.1"
serverPort = 8000
bufferSize = 1024

#create client socket
try:
	clientSocket = socket(AF_INET,SOCK_STREAM)
except error as msg:
	print("Strange exception occurred when creating client socket: %s" % msg)
	sys.exit(1)

#connect to server
try:
	clientSocket.connect((serverName,serverPort))
	print("The connection to host " + serverName + " port " + str(serverPort) + " is successful\n")
except gaierror as msg:
	print("Address-related exception occurred when connecting to server: %s" % msg)
	sys.exit(1)
except error as msg:
	print("Connection exception occurred: %s" % msg)
	sys.exit(1)

#create a log file and name the file client.log
logging.basicConfig(filename='client.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logging.info("Client connection established at host " + serverName + " port " + str(serverPort))

while True:
	try:
		#ask for artist name
		artist = input("Input Artist Name: ")
		if len(artist) > bufferSize or artist == "":
			print("Input error: length range(1,1025)")
			continue

		#send data to server
		try:
			start = time.time()
			clientSocket.sendall(artist.encode())
		except error as msg:
			print("Exception occurred when sending data: %s" % msg)
			sys.exit(1)

		#close client socket
		if artist == "quit":
			break
		else:
			logging.info('Artist name "%s" is sent successfully' % artist)
			
		#receive data from server
		try:
			songs = clientSocket.recv(bufferSize).decode()
			done = time.time()
			logging.info('Server response for artist "%s" received' % artist)
			logging.info("It took " + str((done-start)*1000) + " ms to receive a response from the server for the request to get songs for " + artist)
			logging.info("The response length was %s bytes" % len(songs.encode("utf-8")))
			arr = songs.split("|")
			for song in arr: 
				print("From Server: " + song)
			print("-------------------------------------------------------------------")
			print("You can continue searching or close the connection by typing \"quit\"")
		except error as msg:
			print("Exception occurred when receving data: %s" % msg)
			sys.exit(1)
	except KeyboardInterrupt:
		clientSocket.sendall("quit".encode())
		break

clientSocket.close()
logging.info("Client connection terminated at host " + serverName + " port " + str(serverPort))
print("\nThe connection to host " + serverName + " port " + str(serverPort) + " is closed. Goodbye.")
