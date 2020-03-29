import os
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal 

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PLOTS_PATH = os.path.join(BASE_PATH, "plots")

#-----------------------
#      Parameters 
#-----------------------

noOfSamples = 2048					#total number of samples
noSymb = math.ceil(noOfSamples/16) 	#total number of symbols (16 samples per symbol)
z = np.array([50000,100000,400000]) # distance of propagation
N = np.zeros((len(z)))			    # total number of taps for each case of fiber length.
D = 17./1e6							# dispersion coefficient of the fiber
lamda = 1550./1e9					# wavelength of the light
symbolRate = 25. * 1e9		
samplingRate = 16 * symbolRate  	# 16 samples per symbol
T = 1/samplingRate					# sampling period
c = 299792458						# speed of light(m/s)
F, I = np.modf(abs(D)*lamda*lamda*z/(2*c*T*T))
N = 2*I+1
N = N.astype(int)

#-----------------------
#   Usefull functions
#-----------------------

def NRZgenerator (bitsInput, length, samplesPerSymbol):
	"""
		Parameters
		------------
		bitsInput: a sequence of '0' and '1' 
	  	length: signal's length
		samplesPerSymbol

		Returns
		------------
		outNRZ: NRZ train pulses. 
	"""
	outNRZ = [bitsInput[i] for i in range(0,len(bitsInput)) for j in range(0,samplesPerSymbol)]
	outNRZ = np.array(outNRZ)
	
	return outNRZ

def eyediagram (signal, samplesPerSymbol, totalSamples, Tsymb, ax):	
	t = np.linspace(-1,1,2*samplesPerSymbol)
	for i in range(0,totalSamples-2*samplesPerSymbol+1,2*samplesPerSymbol):
		plt.plot(t,signal[i:i+2*samplesPerSymbol],'b')
	ax.set_title("eyediagram",fontsize=7)
	ax.set_xlabel("Time [sec]",fontsize=7)
	ax.set_ylabel("Amplitude",fontsize=7)
	ax.grid()


if __name__ == '__main__':
	squareNRZ = np.zeros((noOfSamples))
	inputNRZ = np.zeros((noOfSamples))
	S = np.zeros((noOfSamples), dtype=complex)
	t = np.zeros((noOfSamples))
	f = np.zeros((noOfSamples))
	k = np.zeros((len(z),np.amax(N)))
	b = np.zeros((len(z),np.amax(N)), dtype=complex)
	H = np.zeros((len(z),noOfSamples), dtype=complex)
	ss = np.zeros((len(z),noOfSamples), dtype=complex)
	SS = np.zeros((len(z),noOfSamples), dtype=complex)
	filtered_ss = np.zeros((len(z),noOfSamples), dtype=complex)

	bitsSeq = np.random.randint(2, size = noSymb)		#generates a random sequence of bits
	t = np.linspace(0,noOfSamples*T,num=noOfSamples)
	f = np.linspace(-samplingRate/2, samplingRate/2, num = noOfSamples)
	#Computation of input NRZ train pulses	
	squareNRZ = NRZgenerator(bitsSeq, noOfSamples, int(samplingRate/symbolRate))
	win = [0,0,1,1,1,1,1,0,0]
	inputNRZ = scipy.signal.convolve(np.pad(squareNRZ,(4,4),'edge'), win, mode='valid')/sum(win)
	#Fourier Transform of the input NRZ signal
	S = np.fft.fft(inputNRZ)

	for i in range (0,len(z)):
		#Computation of the FIR coefficients.
		F, I = math.modf(N[i]/2)
		k[i,:N[i]] = np.arange(-I, I+1)
		b[i,:N[i]] = cmath.sqrt(1j*c*T*T/(D*lamda*lamda*z[i])) * \
					 np.exp((-1j*math.pi*c*T*T*k[i,:N[i]]*k[i,:N[i]]/(D*lamda*lamda*z[i])))

		#Computation of the chromatic dispersion
		H[i,:] = np.fft.ifftshift(np.exp(-1j*D*lamda*lamda*z[i]*((2*math.pi*f)**2)/(4*math.pi*c)))
		#Computation of the NRZ pulses with chromatic dispersion
		SS[i,:] = H[i,:]*S
		ss[i,:] =  np.fft.ifft(SS[i,:])
		#Counterbalance the chromatic dispersion with FIR filter.
		filtered_ss[i,:] = scipy.signal.convolve(ss[i,:], b[i,:N[i]], mode='same')

	#----------------------------------------------------------------------------------
	plt.figure(1)
	plt.subplot(1,2,1)
	plt.plot(t, inputNRZ)	
	plt.xlabel('Time [sec]', fontsize=7)
	plt.ylabel('Amplitude', fontsize=7)
	plt.xlim(0, noOfSamples*T)
	plt.title('Input NRZ train pulses')
	plt.grid()

	ax = plt.subplot(1,2,2)
	eyediagram(inputNRZ, 16, noOfSamples, T*16, ax)
	plt.tight_layout()
	fileName = os.path.join(PLOTS_PATH, "1.png")
	plt.savefig(fileName, format='png')
	plt.show()

	plt.figure(2)
	for i in range(0,len(z)):
		plt.subplot(3, 2, 2*i+1)
		plt.plot(t, abs(ss[i,:]), '-b')	
		plt.xlabel('Time [sec]', fontsize=7)
		plt.ylabel('Amplitude', fontsize=7)
		plt.xlim(0, noOfSamples*T)
		plt.title('NRZ pulses with chromatic dispersion, fiber_length = '+str(z[i])+'m', fontsize=7)			
		plt.grid()
		ax = plt.subplot(3,2,2*i+2)
		eyediagram(abs(ss[i,:]),16,noOfSamples,T*16,ax)
	plt.tight_layout()
	fileName = os.path.join(PLOTS_PATH, "2.png")
	plt.savefig(fileName, format='png')
	plt.show()
		
	plt.figure(3)
	plt.subplot(2,3,1)
	Sxx = S[:noOfSamples//2]*np.conj(S[:noOfSamples//2])/(noOfSamples*noOfSamples) 		#power spectral density estimate
	plt.plot(np.linspace(0, samplingRate//2, num = noOfSamples//2),10*np.log10(Sxx+1e-12))
	plt.xlabel("Frequency [Hz]",fontsize=7)
	plt.ylabel("Magnitude(dB)",fontsize=7)
	plt.xlim(0,samplingRate//2)
	plt.title('Onesided Spectrum of the NRZ pulses',fontsize=7)		
	plt.grid()
	for i in range(0,len(z)):	
		plt.subplot(2,3,4+i)
		SSxx = SS[i,:noOfSamples//2]*np.conj(SS[i,:noOfSamples//2])/(noOfSamples*noOfSamples) #power spectral density estimate
		plt.plot(np.linspace(0, samplingRate//2, num = noOfSamples//2),10*np.log10(SSxx+1e-12))
		plt.xlabel("Frequency [Hz]",fontsize=7)
		plt.ylabel("Magnitude(dB)",fontsize=7)
		plt.xlim(0,samplingRate//2)
		plt.title('Onesided Spectrum of the NRZ pulses with chromatic dispersion \n fiber_length = '+str(z[i])+'m',fontsize=7)			
		plt.grid()
	fileName = os.path.join(PLOTS_PATH, "3.png")
	plt.savefig(fileName, format='png')
	plt.show()	

	plt.figure(4)
	for i in range(0,len(z)):
		r = abs(b[i,:N[i]])
		phi = np.angle(b[i,:N[i]])

		plt.subplot(3,2,2*i+1)
		plt.plot(k[i,:N[i]],r)
		plt.ylim(0,0.04)
		plt.xlim(k[i,0],k[i,N[i]-1])
		plt.xlabel("Number of taps",fontsize=7)
		plt.ylabel("Amplitude",fontsize=7)
		plt.grid()
		plt.subplot(3,2,2*i+2)
		plt.plot(k[i,:N[i]],phi/math.pi,'.-')
		plt.xlim(k[i,0],k[i,N[i]-1])
		plt.xlabel("Number of taps",fontsize=7)
		plt.ylabel("Normalized phase [1/pi]",fontsize=7)
		plt.grid()
	plt.suptitle("The FIR filter which counterbalances the chromatic dispersion.")
	plt.tight_layout()
	fileName = os.path.join(PLOTS_PATH, "4.png")
	plt.savefig(fileName, format='png')
	plt.show()	

	plt.figure(5)
	for i in range(0,len(z)):
		amplMax = np.amax(abs(filtered_ss[i,:])) #normalizes the filtered signal
		plt.subplot(3,2,2*i+1)
		plt.plot(t,abs(filtered_ss[i,:])/amplMax,'-b')	
		plt.xlabel("Time [sec]",fontsize=7)
		plt.ylabel("Amplitude",fontsize=7)
		plt.xlim(0,noOfSamples*T)
		plt.title('After CD compensation, fiber_length = '+str(z[i])+'m',fontsize=7)
		plt.grid()
		ax = plt.subplot(3,2,2*i+2)
		eyediagram(abs(filtered_ss[i,:])/amplMax,16,noOfSamples,T*16,ax)
	plt.tight_layout()
	fileName = os.path.join(PLOTS_PATH, "5.png")
	plt.savefig(fileName, format='png')
	plt.show()