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


<img src="/plots/1.png" alt="1st plot" width=400 />

##### Step 2: Import chromatic dispersion
We calculate the original signal in the frequency domain using the Discrete Fourier Transform (DFT). Let <img src="/tex/aabe1517ce1102595512b736cbf264bb.svg?invert_in_darkmode&sanitize=true" align=middle width=15.831502499999988pt height=14.15524440000002pt/> to be the initial sequence of pulses, which has length M.
Then in the frequency field can be computed as:

<p align="center"><img src="/tex/eba9dc79c9c94296fadc253251fbc22c.svg?invert_in_darkmode&sanitize=true" align=middle width=293.078808pt height=47.60747145pt/></p>

<p align="center"><img src="/tex/76ad6000c2f12c4caa67c934042d8ed8.svg?invert_in_darkmode&sanitize=true" align=middle width=90.090957pt height=12.6027363pt/></p>


<p align="center"><img src="/tex/c59dfee61f0f1ef3a1f6b6b1d950e01e.svg?invert_in_darkmode&sanitize=true" align=middle width=330.21949455pt height=48.18280005pt/></p>

<p align="center"><img src="/tex/439dedf761b53fbf339050b711127b25.svg?invert_in_darkmode&sanitize=true" align=middle width=173.7372483pt height=39.452455349999994pt/></p>

<p align="center"><img src="/tex/2d125955cdfaf63674edc7fb8ab2ff8e.svg?invert_in_darkmode&sanitize=true" align=middle width=179.9751657pt height=25.160896199999996pt/></p>

<img src="/plots/2.png" alt="2nd plot" width=400 />


<p align="center"><img src="/tex/8a4bab3cfa6acb8ca4fb438f48e11198.svg?invert_in_darkmode&sanitize=true" align=middle width=64.26127125pt height=35.77743345pt/></p>

<p align="center"><img src="/tex/269dd2ab9cc821bccdfddb647bdf81c0.svg?invert_in_darkmode&sanitize=true" align=middle width=95.1640074pt height=35.77743345pt/></p>

<p align="center"><img src="/tex/9f0660d8266d7d7ceca7b4297f16ad26.svg?invert_in_darkmode&sanitize=true" align=middle width=82.7281917pt height=16.438356pt/></p>

<img src="/plots/3.png" alt="3rd plot" width=400 />

##### Step 3: Apply the filter to counterbalance the chromatic dispersion
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/FIR_Filter.svg/2880px-FIR_Filter.svg.png" alt="FIR filter" width=400 />

<p align="center"><img src="/tex/21ab1a17d541a91f588f10f8fb0b584a.svg?invert_in_darkmode&sanitize=true" align=middle width=154.15735665pt height=39.452455349999994pt/></p>

<p align="center"><img src="/tex/c79ecedf0a558beff094fcfef92d6102.svg?invert_in_darkmode&sanitize=true" align=middle width=103.5867294pt height=39.452455349999994pt/></p>

<p align="center"><img src="/tex/a1a1212d9a60ccd8f22ade6d1b4e0ed1.svg?invert_in_darkmode&sanitize=true" align=middle width=151.03627605pt height=40.11819404999999pt/></p>

<img src="/plots/4.png" alt="4th plot" width=400 />

<p align="center"><img src="/tex/efcc134d78e7b02f6fede57dfb6da689.svg?invert_in_darkmode&sanitize=true" align=middle width=466.18079804999996pt height=47.60747145pt/></p>

<img src="/plots/5.png" alt="5th plot" width=400 />

<img src="/plots/optic_fiber.png" alt="Optic fiber" width=400 />



### References

[1] [Savory, Seb J. "Digital filters for coherent optical receivers." Optics express 16.2 (2008): 804-817](https://www.researchgate.net/publication/5313457_Digital_Filters_for_Coherent_Optical_Receivers)

[2] [Αλεξανδρής Αλέξανδρος. "ΕΠΙΚΟΙΝΩΝΙΑΚΑ ΣΥΣΤΗΜΑΤΑ ΜΕ ΟΠΤΙΚΕΣ ΙΝΕΣ." Εκδόσεις Τζίολα (2010)](https://www.tziola.gr/book/aleks/)

[3] [Συστήματα Μετάδοσης και Δίκτυα Οπτικών Ινών](https://www.photonics.ntua.gr/Diafaneies_Susthmata_metadoshs/Systimata_Metadosis_kai%20_Diktya_Optikwn_Inwn.pdf)