# Coherent Optical Receiver

### Purpose
The purpose is to develop an algorithm to counterbalance for the chromatic dispersion by means of an FIR filter with an appropriate transfer function to suppress the chromatic dispersion.

### Simulation

##### Step 1: Creating a modulated signal for transmission

* First we generate a random sequence of digits-symbols.
* We generate pulses using 16 samples/symbol and encode the generated sequence with **Unipolar-NRZ**. These pulses correspond to the envelope of the modulated signal, as the signal passes through the photodiode.

	_Unipolar_: for bit '0' we send 0, otherwise for bit '1' we send +A V (we choose A = 1).

	_NRZ_: the pulse lasts the entire symbol period.
* We modulate the pulses to have rise and fall times. (The pulses have expanded, after being modulated by convolution, so they are cut into the eyediagram).


![]()

##### Step 2: Import chromatic dispersion
We calculate the original signal in the frequency domain using the Discrete Fourier Transform (DFT). Let $s_n$ to be the initial sequence of pulses, which has length M. Then in the frequency field can be computed as:

$$ S_k=\sum_{n=0}^{M-1}s_ne^{-j\frac{2π}{M}kn},~~ k=0,1,...,M-1 $$
