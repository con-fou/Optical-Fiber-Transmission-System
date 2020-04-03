# Coherent Optical Receiver

### Purpose
The purpose is to develop an algorithm to counterbalance for the chromatic dispersion by means of an FIR filter with an appropriate frequency response to suppress the chromatic dispersion.

### Simulation

##### Step 1: Creating a modulated signal for transmission

* First we generate a random sequence of digits-symbols.
* We generate pulses using 16 samples/symbol and encode the generated sequence with **Unipolar-NRZ**. These pulses correspond to the envelope of the modulated signal, as the signal passes through the photodiode.

	_Unipolar_: for bit '0' we send 0, otherwise for bit '1' we send +A V (we choose A = 1).

	_NRZ_: the pulse lasts the entire symbol period.
* We modulate the pulses to have rise and fall times. (The pulses have expanded, after being modulated by convolution, so they are cut into the eyediagram).

| <img src="/plots/1.png" alt="1st plot" width=600 /> | 
|:--:| 
| *Figure 1: (a) Pulse-width modulated signal with rate of symbol transmission $25*10^9 \text{ symbols/sec}$. (b) The corresponding eye diagram for pulse superposition within two $T_{symb}$ .* |

##### Step 2: Import chromatic dispersion
We calculate the original signal in the frequency domain using the Discrete Fourier Transform (DFT). Let $s_n$ to be the initial sequence of pulses, which has length M.
Then in the frequency domain can be computed as:
$$
S_k=\sum_{n=0}^{M-1}s_ne^{-j\frac{2\pi}{M}kn},~~ k=0,1,...,M-1 
$$

Applying chromatic dispersion, Η, to our signal in the time domain (for a given optical fiber length) we obtain the Hadamard product:
$$ 
SS=H\odot S 
$$

Convert the signal with the chromatic dispersion to time domain, with Inverse DFT:
$$
ss_n = \frac{1}{M}\sum_{k=0}^{M-1}{X_ke^{j2\pi kn/M}},~~n=0,1,...,M-1
$$

The chromatic dispersion is described in the time domain by the impulse response:
$$
h(z,t)=\sqrt{\frac{c}{jD\lambda ^2z}}e^{j\frac{\pi c}{D\lambda ^2z}t^2}
$$

and in the frequency domain by the frequency response:
$$
H(z,\omega)=e^{-j\frac{\beta _2z}{2}\omega ^2} = e^{j\frac{D\lambda ^2z}{4\pi c}\omega ^2}
$$
where:

> $\lambda$: the wavelength of the light <br>
> $c$: the speed of light <br>
> $D$: the dispersion coefficient of the fiber <br>
> $\beta _2$: group velocity dispersion parameter <br>
> $z$: the distance of propagation <br>
> $\omega$: the angular frequency 

Keeping the above parameters constant and only changing the optical fiber length, z, we observe that the longer the optical fiber length increases, the more the original signal changes in time domain.

| <img src="/plots/2.png" alt="2nd plot" width=600 /> | 
|:--:| 
| *Figure 2: (a) The signal we receive from the optical fiber over time, which is affected by the chromatic dispersion effect (b) The corresponding eye diagram.* |

We will calculate the power spectral density (PSD) estimation for the signal before and after transmission, using the periodogram.

$$P=\frac{|S|^2}{M^2} ~ \text{and} ~ P_{CD} = \frac{|SS|^2}{M^2}$$

As shown in Figure 3, the PSD is not affected by the chromatic dispersion, since the chromatic dispersion frequency response has $|H(z,\omega)|=1$, for each values ​​of $z$ and $\omega$.

| <img src="/plots/3.png" alt="3rd plot" width=1200 /> | 
|:--:| 
| *Figure 3: (a) The spectrum of the signal to be transmitted. (b) The spectrum of the signal received through the optical fiber.* |


##### Step 3: Apply the filter to counterbalance the chromatic dispersion
<p align="center">
	<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/FIR_Filter.svg/2880px-FIR_Filter.svg.png" alt="FIR filter" width=400 />
</p>

We implement a FIR filter with an impulse function equal to that of the chromatic dispersion but with the opposite sign of the dispersion parameter D. Specifically, the $b_k$ taps values ​​of the FIR filter are given by:
$$
b_k = \sqrt{\frac{jcT_s^2}{D\lambda ^2z}}e^{-j\frac{\pi cT_s^2}{D\lambda ^2z}k^2}
$$

where we limit the impulse response of the filter at time, according to Nyquist's theorem, to avoid aliasing, giving the criterion that:
$$\left\lfloor -\frac{N}{2} \right\rfloor \leq k \leq \left\lfloor \frac{N}{2} \right\rfloor,~ N=2* \left\lfloor\frac{|D|\lambda ^2z}{2cT_s^2}\right\rfloor+1 $$

| <img src="/plots/4.png" alt="4th plot" width=600 /> | 
|:--:| 
| *Figure 4: (a) The amplitude of the FIR filter. (b) The normalized phase of the FIR filter.* |

We apply the filter, in the time domain, by convolution to the signal we received from the fiber optic transmission. The filtered signal is given by:
$$
filtered_{ss}[n]=(ss *b)[n] = \sum_{m=0}^{N-1}ss[n-m]b[m],~~n = N+M-1 
$$
where from the N + M-1 samples, we only hold M, according to the ` mode='same' ` of the function ` scipy.signal.convolve( ) `

| <img src="/plots/5.png" alt="5th plot" width=600 /> | 
|:--:| 
| *Figure 5: (a) The recovered signal, obtained with the help of the color dispersion filter, in the time domain. (b) The corresponding eye diagram.* |

We observe that the longer the fiber length increases, the more the chromatic dispersion effect affects the signal we send. From the eye-diagram we notice the existence of noise that was not eliminated by the filter, both at level '1' and '0'. We also observe that the eye opening has diminished as the level '1' has less width since the energy has "spread out" after the pulse expanded. In addition, in the eye diagram we notice the shift of the pulse to the right, that is, a delay in the time domain due to the chromatic dispersion importing a phase change. 

<p align="center">
	<img src="/plots/optic_fiber.png" alt="Optic fiber" width=400 />
</p>

Finally, we observe a time fluctuation of the pulses due to the fact that the chromatic dispersion leads the different spectral components to be transmitted at slightly different group velocities.

### References

[1] [Savory, Seb J. "Digital filters for coherent optical receivers." Optics express 16.2 (2008): 804-817](https://www.researchgate.net/publication/5313457_Digital_Filters_for_Coherent_Optical_Receivers)

[2] [Αλεξανδρής Αλέξανδρος. "ΕΠΙΚΟΙΝΩΝΙΑΚΑ ΣΥΣΤΗΜΑΤΑ ΜΕ ΟΠΤΙΚΕΣ ΙΝΕΣ." Εκδόσεις Τζίολα (2010)](https://www.tziola.gr/book/aleks/)

[3] [Συστήματα Μετάδοσης και Δίκτυα Οπτικών Ινών](https://www.photonics.ntua.gr/Diafaneies_Susthmata_metadoshs/Systimata_Metadosis_kai%20_Diktya_Optikwn_Inwn.pdf)