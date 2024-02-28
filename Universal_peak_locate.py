import numpy as np
from scipy.signal import find_peaks

def find_closest_peak(reference_peak, peaks):
    if len(peaks) == 0:
        return None
    distances = np.abs(peaks - reference_peak)
    closest_peak_idx = np.argmin(distances)
    return peaks[closest_peak_idx]

def identify_isotope(Am_peak_closest, Cs_peak_closest, Co_peak_closest_1, Co_peak_closest_2):
    known_positions = {
        'Am': 59.7,
        'Cs': 661.9,
        'Co1': 1170.0,
        'Co2': 1330.0
    }
    differences = {}
    for peak, closest_peak in zip(['Am', 'Cs', 'Co1', 'Co2'], [Am_peak_closest, Cs_peak_closest, Co_peak_closest_1, Co_peak_closest_2]):
        if closest_peak is not None:
            differences[peak] = np.abs(closest_peak - known_positions[peak])
    if not differences:
        return None
    closest_isotope = min(differences, key=differences.get)
    isotope_names = {
        'Am': 'Americium',
        'Cs': 'Caesium',
        'Co1': 'Cobalt',
        'Co2': 'Cobalt'
    }
    return isotope_names[closest_isotope]

def sweeper(x, y, calibrated=False):
    x = x.to_numpy()
    y = y.to_numpy()
    if calibrated:
        Am_peak_ref = 59.7
        Cs_peak_ref = 661.9
        Co_peak_ref_1 = 1170.0
        Co_peak_ref_2 = 1330.0

    else:
        Am_peak_ref = 1260.0
        Cs_peak_ref = 4265
        Co_peak_ref_1 = 7000
        Co_peak_ref_2 = 8000

    
    Am_peak_range = np.arange(1100, 1300, 1) if not calibrated else np.arange(45, 70, 1)
    Cs_peak_range = np.arange(3500, 5500, 1) if not calibrated else np.arange(500, 750, 1)
    Co_peak_range_1 = np.arange(5000, 7500, 1) if not calibrated else np.arange(900, 1200, 1)
    Co_peak_range_2 = np.arange(6000, 9000, 1) if not calibrated else np.arange(1200, 1500, 1)
    
    Am_peaks, _ = find_peaks(y[np.where((x >= Am_peak_range[0]) & (x <= Am_peak_range[-1]))], height=(None, None), threshold=None, distance=None, prominence=50, width=None, wlen=None, rel_height=50, plateau_size=None)
    Cs_peaks, _ = find_peaks(y[np.where((x >= Cs_peak_range[0]) & (x <= Cs_peak_range[-1]))], height=(None, None), threshold=None, distance=None, prominence=7, width=None, wlen=None, rel_height=50, plateau_size=None)
    Co_peaks_1, _ = find_peaks(y[np.where((x >= Co_peak_range_1[0]) & (x <= Co_peak_range_1[-1]))], height=(None, None), threshold=None, distance=None, prominence=5, width=None, wlen=None, rel_height=10, plateau_size=None)
    Co_peaks_2, _ = find_peaks(y[np.where((x >= Co_peak_range_2[0]) & (x <= Co_peak_range_2[-1]))], height=(None, None), threshold=None, distance=None, prominence=5, width=None, wlen=None, rel_height=10, plateau_size=None)
    
    Am_peak_positions = x[(x >= Am_peak_range[0]) & (x <= Am_peak_range[-1])][Am_peaks]
    Cs_peak_positions = x[(x >= Cs_peak_range[0]) & (x <= Cs_peak_range[-1])][Cs_peaks]
    Co_peak_positions_1 = x[(x >= Co_peak_range_1[0]) & (x <= Co_peak_range_1[-1])][Co_peaks_1]
    Co_peak_positions_2 = x[(x >= Co_peak_range_2[0]) & (x <= Co_peak_range_2[-1])][Co_peaks_2]
    
    if not (Am_peaks.any() or Cs_peaks.any() or Co_peaks_1.any() or Co_peaks_2.any()):
        print("No peaks found. Adjusting parameters.")
        y *= 60
        Am_peaks, _ = find_peaks(y[np.where((x >= Am_peak_range[0]) & (x <= Am_peak_range[-1]))], height=(None, None), threshold=None, distance=None, prominence=10, width=None, wlen=None, rel_height=0.5, plateau_size=None)
        Cs_peaks, _ = find_peaks(y[np.where((x >= Cs_peak_range[0]) & (x <= Cs_peak_range[-1]))], height=(None, None), threshold=None, distance=None, prominence=2, width=None, wlen=None, rel_height=0.5, plateau_size=None)
        Co_peaks_1, _ = find_peaks(y[np.where((x >= Co_peak_range_1[0]) & (x <= Co_peak_range_1[-1]))], height=(None, None), threshold=None, distance=None, prominence=5, width=None, wlen=None, rel_height=0.5, plateau_size=None)
        Co_peaks_2, _ = find_peaks(y[np.where((x >= Co_peak_range_2[0]) & (x <= Co_peak_range_2[-1]))], height=(None, None), threshold=None, distance=None, prominence=5, width=None, wlen=None, rel_height=0.5, plateau_size=None)
    
    Am_peak_closest = find_closest_peak(Am_peak_ref, x[(x >= Am_peak_range[0]) & (x <= Am_peak_range[-1])][Am_peaks])
    Cs_peak_closest = find_closest_peak(Cs_peak_ref, x[(x >= Cs_peak_range[0]) & (x <= Cs_peak_range[-1])][Cs_peaks])
    Co_peak_closest_1 = find_closest_peak(Co_peak_ref_1, x[(x >= Co_peak_range_1[0]) & (x <= Co_peak_range_1[-1])][Co_peaks_1])
    Co_peak_closest_2 = find_closest_peak(Co_peak_ref_2, x[(x >= Co_peak_range_2[0]) & (x <= Co_peak_range_2[-1])][Co_peaks_2])
    
    identified_isotope = identify_isotope(Am_peak_closest, Cs_peak_closest, Co_peak_closest_1, Co_peak_closest_2)
    print(f'The Isotope identified is: {identified_isotope}')
    return Am_peak_closest, Cs_peak_closest, Co_peak_closest_1, Co_peak_closest_2