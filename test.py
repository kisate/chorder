from __future__ import print_function
from pprint import pprint
import numpy as np
import scipy
import matplotlib.pyplot as plt
import pickle
import librosa
import librosa.display
# 1. Get the file path to the included audio example
filename = "tsoi2"
savepath = filename + '.out'
# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
y, sr = librosa.load(filename + '.mp3')

print(len(y))

tempo = librosa.beat.tempo(y, sr)

print(tempo)

y_harm = librosa.effects.harmonic(y=y, margin=12)
chroma_orig = librosa.feature.chroma_cqt(y=y, sr=sr)
#print(len(y_harm))
chroma_os_harm = librosa.feature.chroma_cqt(y=y_harm, sr=sr, bins_per_octave=12*3)

filtered = librosa.decompose.nn_filter(chroma_os_harm)

chroma_filter = np.minimum(chroma_os_harm, filtered)
# And for comparison, we'll show the CQT matrix as well.
#C = np.abs(librosa.cqt(y=y, sr=sr, bins_per_octave=12*3, n_bins=7*12*3))

chroma_smooth = scipy.ndimage.median_filter(chroma_filter, size=(1, 9))

#l = len(chroma_smooth[0])

#print(l)

f = open(savepath, 'wb')
pickle.dump({'data' : chroma_smooth, 'samples' : len(y), 'sr' : sr, 'tempo' : tempo}, f)
f.close()

import process

process.process(savepath)
