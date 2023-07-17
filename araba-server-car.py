import cv2, imutils, socket
import numpy as np
import time
import base64
import socket, time
import pyfirmata, cv2 ,imutils,base64
board = pyfirmata.Arduino('/dev/ttyUSB0')
iter8= pyfirmata.util.Iterator(board)
iter8.start()
BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '10.11.6.44'
print(host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)
vid = cv2.VideoCapture(0) 
fps,st,frames_to_count,cnt = (0,0,20,0)
while True:
	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	WIDTH=400
	while(vid.isOpened()):
		_,frame = vid.read()
		frame = imutils.resize(frame,width=WIDTH)
		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
		message = base64.b64encode(buffer)
		server_socket.sendto(message,client_addr)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('p'):
			server_socket.close()
			break
		if cnt == frames_to_count:
			try:
				fps = round(frames_to_count/(time.time()-st))
				st=time.time()
				cnt=0
			except:
				pass
		cnt+=1
		gelen = server_socket.recv(2048).decode().strip("b''")
		if gelen == "w":
			board.digital[4].write(0)
			board.digital[6].write(0)
			board.digital[3].write(1)
			board.digital[5].write(1)
			board.digital[2].write(1)
			board.digital[7].write(1)
		elif gelen == "s":
			board.digital[4].write(1)
			board.digital[6].write(1)
			board.digital[3].write(1)
			board.digital[5].write(1)
			board.digital[2].write(0)
			board.digital[7].write(0)
		elif gelen == "d":
			board.digital[4].write(0)
			board.digital[6].write(0)
			board.digital[3].write(1)
			board.digital[5].write(1)
			board.digital[2].write(1)
			board.digital[7].write(0)
		elif gelen == "a":
			board.digital[4].write(0)
			board.digital[6].write(0)
			board.digital[3].write(1)
			board.digital[5].write(1)
			board.digital[2].write(0)
			board.digital[7].write(1)
		else:
			board.digital[4].write(0)
			board.digital[6].write(0)
			board.digital[3].write(0)
			board.digital[5].write(0)
			board.digital[2].write(0)
			board.digital[7].write(0)