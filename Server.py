from socket import *
import sys
import threading
import logging
import time

#return the map holding tuples of type artist-song
def readFile(path):
	f = open(path)
	flag = False
	temp = None
	artist_song_map = {}
	while True:
		line = f.readline()

		if not line:
			break
		elif not line[0].isdigit():
			if flag:
				temp = None
				continue
			else:
				flag = True
				if len(line.replace(" ","")) == 0:
					continue
		else:
			flag = False

		artist_song = [x.strip() for x in line.split("  ") if x != ""]
		if temp != None:
			add2Map(artist_song_map,artist_song[0],temp)
			temp = None
		else:
			artist_song[0] = artist_song[0][4:]
			if len(artist_song) == 3:
				add2Map(artist_song_map,artist_song[1],artist_song[0])
			elif len(artist_song) == 2:
				add2Map(artist_song_map,"Unknown Artist",artist_song[0])
			elif len(artist_song) == 1:
				temp = artist_song[0]
	return artist_song_map

def add2Map(hMap,key1,value):
	key = key1.upper()
	if key in hMap.keys():
		if type(hMap[key]) is list:
			temp = hMap[key]
			temp.append(value)
			hMap[key] = temp
		else:
			temp = [hMap[key]]
			temp.append(value)
			hMap[key] = temp
	else:
		hMap[key] = value

#finds all songs associated to the given artist
#if more than one songs are found, '|' delimiter will be used
def getSongs(asMap,artist):
	if artist in asMap.keys():
		song = asMap[artist]
		if type(song) is list:
			temp = ""
			for i in song:
				temp += i + "|"
			return temp[:len(temp)-1]
		else:
			return song
	else:
		return "No songs associated to the given artist"

def tcplink(connectionSocket,addr):
	start = time.time()
	while True:
		#receive data from client
		try:
			artist = connectionSocket.recv(bufferSize).decode().upper()
		except error as msg:
			print("Exception occurred when receiving data: %s" % msg)
			sys.exit(1)

		#close connection socket
		if artist == "QUIT":
			break
		else:
			logging.info('Artist name "%s" received' % artist)

		#send data to client
		try:
			songs = getSongs(asMap,artist)
			connectionSocket.sendall(songs.encode())
		except error as msg:
			print("Exception occurred when sending data: %s" % msg)
			sys.exit(1)
	connectionSocket.close()
	done = time.time()
	period = done - start
	logging.info("Client disconnected - Total connection time: %s s" % period)

#create a log file and name the file server.log
logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

#Define host port and bufferSize
serverName = "127.0.0.1"
serverPort = 8000
bufferSize = 1024

#create server socket
try:
	serverSocket = socket(AF_INET,SOCK_STREAM)
except error as msg:
	print("Strange exception occurred when creating server socket: %s" % msg)
	sys.exit(1)

#bind server
try:
	serverSocket.bind((serverName,serverPort))
	logging.info("Server started at host " + serverName + " port " + str(serverPort))
except gaierror as msg:
	print("Address-related exception occurred when binding server: %s" % msg)
	sys.exit(1)
except error as msg:
	print("Binding exception: %s" % msg)
	sys.exit(1)

#set the maximum number of quened connections
serverSocket.listen(5)
print("The server is ready to connect at host " + serverName + " port " + str(serverPort) + ".")
print("Terminate server socket by pressing Ctrl + Break (Windows) or Ctrl + C (Mac).")

#enlist artists plus their songs which is read in and held in a map
asMap = readFile("100worst.txt")

while True:
	try:
		#accept clients' connections
		try:
			connectionSocket, addr = serverSocket.accept()
			logging.info("Client connection request received and established successfully")
		except error as msg:
			logging.info("Client connection request received but failed to establish")
			print("Connection exception: %s" % msg)
			continue

		#create new thread for each client
		try:
			t = threading.Thread(target = tcplink, args = (connectionSocket,addr))
			t.start()
		except threading.RuntimeError as msg:
			print("Thread runtime error: %s" % msg)
			sys.exit(1)
	except KeyboardInterrupt:
		if threading.activeCount() != 1:
			print("\nServer socket failed to terminate: %s client connections is active" % str(threading.activeCount()-1))
		else:
			serverSocket.close()
			logging.info("Server terminated")
			print("\nServer socket is now closed.")
			break
