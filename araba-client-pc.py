import socket, base64,cv2
import numpy as np
import time
import keyboard
import mediapipe as mp
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '10.11.6.44'
print(host_ip)
port = 9999
message = b'Hello'
client_socket.sendto(message,(host_ip,port))
fps,st,frames_to_count,cnt = (0,0,20,0)
a = 0
veri =0
while True:
    packet,_ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet,' /')
    npdata = np.fromstring(data,dtype=np.uint8)
    frame = cv2.imdecode(npdata,1)
    results = pose.process(frame)
    kisi = "Kimse yok."
    if results.pose_landmarks: # if image has a poselandmarks
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = frame.shape
            hl = lm.x,lm.y,lm.z
            cx, cy = int(lm.x * w), int(lm.y * h) 
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        kisi = "Kisi tespiti yapildi."
    frame = cv2.putText(frame,str(kisi),(10,280),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    h, w , l = frame.shape
    new_h = h*2
    new_w = w*2
    frame = cv2.resize(frame , (new_w,new_h))

    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('p'):
        client_socket.close()
        break
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count/(time.time()-st))
            st=time.time()
            cnt=0
        except:
            pass
        cnt+=1
    if keyboard.is_pressed('w'):
        client_socket.sendto(str.encode("w"),(host_ip,port)) 
    elif keyboard.is_pressed('s'):
        client_socket.sendto(str.encode("s"),(host_ip,port))
    elif keyboard.is_pressed('d'):
        client_socket.sendto(str.encode("d"),(host_ip,port))
    elif keyboard.is_pressed('a'):
        client_socket.sendto(str.encode("a"),(host_ip,port))
    else:
        client_socket.sendto(str.encode("o"),(host_ip,port))




