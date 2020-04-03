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
| *Figure 1: (a) Pulse-width modulated signal with rate of symbol transmission <img src="/tex/b1772b42f6da3257592fd2558a7a9f4e.svg?invert_in_darkmode&sanitize=true" align=middle width=147.83132924999998pt height=26.76175259999998pt/>. (b) The corresponding eye diagram for pulse superposition within two <img src="/tex/66c85af06abda9c9b8c5720b781bccf4.svg?invert_in_darkmode&sanitize=true" align=middle width=40.33584884999999pt height=22.465723500000017pt/> .* |

##### Step 2: Import chromatic dispersion
We calculate the original signal in the frequency domain using the Discrete Fourier Transform (DFT). Let <img src="/tex/aabe1517ce1102595512b736cbf264bb.svg?invert_in_darkmode&sanitize=true" align=middle width=15.831502499999988pt height=14.15524440000002pt/> to be the initial sequence of pulses, which has length M.
Then in the frequency domain can be computed as:
<p align="center"><img src="/tex/bc1a41d37e1747c64ae9532d38c4e068.svg?invert_in_darkmode&sanitize=true" align=middle width=294.34885755pt height=47.60747145pt/></p>

Applying chromatic dispersion, Η, to our signal in the time domain (for a given optical fiber length) we obtain the Hadamard product:
<p align="center"><img src="/tex/76ad6000c2f12c4caa67c934042d8ed8.svg?invert_in_darkmode&sanitize=true" align=middle width=90.090957pt height=12.6027363pt/></p>

Convert the signal with the chromatic dispersion to time domain, with Inverse DFT:
<p align="center"><img src="/tex/f631623e3bdd4d6bf41c75dfa79ce2bb.svg?invert_in_darkmode&sanitize=true" align=middle width=338.31945344999997pt height=48.18280005pt/></p>

The chromatic dispersion is described in the time domain by the impulse response:
<p align="center"><img src="/tex/5544de40c9b6f9663b909c56e713cb98.svg?invert_in_darkmode&sanitize=true" align=middle width=190.23279495pt height=39.452455349999994pt/></p>

and in the frequency domain by the frequency response:
<p align="center"><img src="/tex/3732d4b623f0bb8640fcd81a80f45324.svg?invert_in_darkmode&sanitize=true" align=middle width=221.59014569999997pt height=23.92804425pt/></p>
where:

> <img src="/tex/fd8be73b54f5436a5cd2e73ba9b6bfa9.svg?invert_in_darkmode&sanitize=true" align=middle width=9.58908224999999pt height=22.831056599999986pt/>: the wavelength of the light <br>
> <img src="/tex/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode&sanitize=true" align=middle width=7.11380504999999pt height=14.15524440000002pt/>: the speed of light <br>
> <img src="/tex/78ec2b7008296ce0561cf83393cb746d.svg?invert_in_darkmode&sanitize=true" align=middle width=14.06623184999999pt height=22.465723500000017pt/>: the dispersion coefficient of the fiber <br>
> <img src="/tex/9d82505b5b0a81353227ecad1baf6cfb.svg?invert_in_darkmode&sanitize=true" align=middle width=15.85051049999999pt height=22.831056599999986pt/>: group velocity dispersion parameter <br>
> <img src="/tex/f93ce33e511096ed626b4719d50f17d2.svg?invert_in_darkmode&sanitize=true" align=middle width=8.367621899999993pt height=14.15524440000002pt/>: the distance of propagation <br>
> <img src="/tex/ae4fb5973f393577570881fc24fc2054.svg?invert_in_darkmode&sanitize=true" align=middle width=10.82192594999999pt height=14.15524440000002pt/>: the angular frequency 

Keeping the above parameters constant and only changing the optical fiber length, z, we observe that the longer the optical fiber length increases, the more the original signal changes in time domain.

| <img src="/plots/2.png" alt="2nd plot" width=600 /> | 
|:--:| 
| *Figure 2: (a) The signal we receive from the optical fiber over time, which is affected by the chromatic dispersion effect (b) The corresponding eye diagram.* |

We will calculate the power spectral density (PSD) estimation for the signal before and after transmission, using the periodogram.

<img src="/tex/59ff8f5aaa807ec49bf6ed232d59f411.svg?invert_in_darkmode&sanitize=true" align=middle width=59.65178009999999pt height=36.460254599999985pt/> and <img src="/tex/f55bcc578fc87f8507a7433ac132b31b.svg?invert_in_darkmode&sanitize=true" align=middle width=88.22809709999999pt height=36.460254599999985pt/>

As shown in Figure 3, the PSD is not affected by the chromatic dispersion, since the chromatic dispersion frequency response has <img src="/tex/9521b392d0ce699df15edaf14a5e6fa0.svg?invert_in_darkmode&sanitize=true" align=middle width=93.55009784999999pt height=24.65753399999998pt/>, for each values ​​of <img src="/tex/f93ce33e511096ed626b4719d50f17d2.svg?invert_in_darkmode&sanitize=true" align=middle width=8.367621899999993pt height=14.15524440000002pt/> and <img src="/tex/ae4fb5973f393577570881fc24fc2054.svg?invert_in_darkmode&sanitize=true" align=middle width=10.82192594999999pt height=14.15524440000002pt/>.

| <img src="/plots/3.png" alt="3rd plot" width=800 /> | 
|:--:| 
| *Figure 3: (a) The spectrum of the signal to be transmitted. (b) The spectrum of the signal received through the optical fiber.* |


##### Step 3: Apply the filter to counterbalance the chromatic dispersion
<p align="center">
	<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/FIR_Filter.svg/2880px-FIR_Filter.svg.png" alt="FIR filter" width=400 />
</p>

We implement a FIR filter with an impulse function equal to that of the chromatic dispersion but with the opposite sign of the dispersion parameter D. Specifically, the <img src="/tex/c1a30f400620a0b6da57046c4b40e16b.svg?invert_in_darkmode&sanitize=true" align=middle width=14.320826849999992pt height=22.831056599999986pt/> taps values ​​of the FIR filter are given by:
<p align="center"><img src="/tex/1ecb8a4b1130af8a04fd5d49a182a0d4.svg?invert_in_darkmode&sanitize=true" align=middle width=166.37325045pt height=39.452455349999994pt/></p>

where we limit the impulse response of the filter at time, according to Nyquist's theorem, to avoid aliasing, giving the criterion that:
<p align="center"><img src="/tex/50ce4c71a0517786b2c948eb53bd5488.svg?invert_in_darkmode&sanitize=true" align=middle width=318.09301755pt height=40.11819404999999pt/></p>

| <img src="/plots/4.png" alt="4th plot" width=600 /> | 
|:--:| 
| *Figure 4: (a) The amplitude of the FIR filter. (b) The normalized phase of the FIR filter.* |

We apply the filter, in the time domain, by convolution to the signal we received from the fiber optic transmission. The filtered signal is given by:
<p align="center"><img src="/tex/efcc134d78e7b02f6fede57dfb6da689.svg?invert_in_darkmode&sanitize=true" align=middle width=466.18079804999996pt height=47.60747145pt/></p>
where from the N + M-1 samples, we only hold M, according to the `mode='same'` of the function `scipy.signal.convolve( )`.

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