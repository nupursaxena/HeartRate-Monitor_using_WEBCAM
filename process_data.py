from scipy.signal import find_peaks
from scipy.fftpack import fft, ifft
import time
import numpy as np
import cv2
from scipy import signal

def proc_vid ( bpm_cumulative, forehead, start):

	'''
	This function processes the green channel frames obtained from
	the input facial video and calculates the BPM from the denoised 
	image
	'''

	g_avg = []
	peaks = []
	end = time.time() - start

	#Total time elapsed upto this frame
	buff_time = (time.time()-start)

	#Calculate average of green channel values of each frame
	for i in range( len(forehead)):
		mean_val = cv2.mean( forehead[i] )
		g_avg.append( mean_val[1] )

	#Remove any trends from the signal due to factors like motion
	g_avg = signal.detrend(g_avg)
	g_avg =  (g_avg -np.mean(g_avg))/np.std(g_avg)
	g_avg = np.hamming(len(g_avg)) * g_avg

	#Obtain corresponding signal in frequency domain
	f_trans = fft(g_avg)
	ps = np.abs(f_trans)**2


	#BPM calculation using peak detection
	p_count=0

	peaks, _ = find_peaks(ps)
	for i in range(len(peaks)):
	    if ps[peaks[i]]>45 and  ps[peaks[i]]<180 :
	        p_count=p_count+1


	beats = (p_count/end)*60
	#print("Time= ",end , " HR= %0.2f"%beats)

	bpm_cumulative.append(beats)

	return bpm_cumulative
