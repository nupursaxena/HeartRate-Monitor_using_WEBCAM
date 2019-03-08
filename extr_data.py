import time
import numpy as np
import cv2

def get_data():


	cap = cv2.VideoCapture(0)

	if cap.isOpened()==False :
		print(" WEBCAM Error ")
		exit(0)

	begin_t = time.time()

	# Define the codec and create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('facial_vid.avi',fourcc, 15, (640,480))


	while(cap.isOpened()):
	    ret, frame = cap.read()
	    if ret==True:

	        out.write(frame)

	        cv2.imshow('frame',frame)
	        if cv2.waitKey(1) & 0xFF == ord('e'):
	            break
	    else:
	        break

	# Release everything after job is done
	cap.release()
	out.release()
	cv2.destroyAllWindows()

	#Return total length of video
	return time.time()-begin_t

def extract_green_channel ( v_img ):
	v_img = extract_forehead(v_img)
	v_img[:,:,[0,2]] = 0
	return v_img

def extract_forehead ( v_img ):

	face_coor = []
	face_coor = extract_face(v_img)

	x0 = int(face_coor[0]+ 2*face_coor[2]/5)
	X0 = int(face_coor[0]+ 3*face_coor[2]/5)
	y0 = int(face_coor[1]+0.75* face_coor[3]/5)
	Y0 = int(face_coor[1]+1.25* face_coor[3]/5)

	v_img = v_img[ y0:Y0 , x0:X0]
	return v_img

def extract_face( v_img ):
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
	eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
	gray = cv2.cvtColor(v_img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3,5)

	for (x,y,w,h) in faces:
		return [ x, y, w, h]

'''
get_data()
cap = cv2.VideoCapture('facial_vid.avi')
frames = []
c=0
while(cap.isOpened()):
    ret, frame = cap.read()
    frames.append(frame)

    c=c+1
    if c==3:
        break
cap.release()
cv2.destroyAllWindows()
img = extract_green_channel(frames[0])
cv2.imshow('s.png',img)
cv2.waitKey(0)

print( cv2.mean(img)[1])
	#v_img= cv2.cvtColor(v_img, cv2.COLOR_RGB2HSV)
    #v_img[:,:,2] = cv2.equalizeHist(v_img[:,:,2])
    #v_img = cv2.cvtColor(v_img, cv2.COLOR_HSV2RGB)
'''