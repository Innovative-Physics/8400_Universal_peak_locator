Universal peak detector
The universal peak detector can locate the peaks in a given spectra, using the scipy.signal.find_peaks() function, within the Universal_peak_locate.py module.  
Parameters for the peak finding function can be altered directly in the module if needed.
Aditional functiionality includes a peak-based isotopic identification, allowing for Am-141, Cs-137 and Co60 to be identified by thier peak characteristics. 
This works by constraining the peak finding functions to specific ranges within either the ADC range (0-8999 ADC) bins or the calibrated energy range (0-2999 keV).