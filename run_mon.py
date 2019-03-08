from extr_data import get_data
from extr_data import extract_green_channel
from process_data import proc_vid
import time
import numpy as np
import cv2 
import matplotlib.pyplot as plt

def run_m():


	buff_cumulative = []
	g_forehead = []
	t_count = 1


	cap = cv2.VideoCapture(0)

	start = time.time()
	while( cap.isOpened() ):

		ret, frame = cap.read()

		try :
			g_frame = extract_green_channel( frame )
		except :
			print("Facial image not within camera range.\nRe-adjust camera\nRETRY\n")
			exit(0)

		g_forehead.append(g_frame)

		#Calculate bpm at every second
		if time.time()-start > t_count :
			t_count = t_count+1
			buff_cumulative = proc_vid(buff_cumulative, g_forehead, start)

		cv2.imshow('Facial_Frame', frame)
		cv2.imshow('Green_Frame', g_frame)
		
		#Upper limit for recording 
		if time.time()-start > 75:
			break
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	return buff_cumulative


res_buff = run_m()	
try:
	#Observed buffer time is 20 seconds to stabalize with a regular webcam
	#Discard first 20 fram values
	res_buff = res_buff[20:]		
	bpm = np.mean(res_buff)
except :
	print( "Capture video for a minimum of 40 seconds\nRETRY\n")
	exit(0)

if bpm>45 and bpm<180:
	print( "Average heart rate = %0.2f BPM"%bpm)
	plt.plot(res_buff,'xo')
	plt.show()
else :
	print("Adjust light intensity ( tilt webcam/ change lighting )\nand stay as still as possible\nRETRY\n")





