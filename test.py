from __future__ import print_function
from pprint import pprint
import numpy as np
import scipy
import matplotlib.pyplot as plt
import pickle
import librosa
import librosa.display
# 1. Get the file path to the included audio example
filename = "japan.wav"

# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
y, sr = librosa.load(filename)

print(len(y))

tempo = librosa.beat.tempo(y, sr)

print(tempo)

y_harm = librosa.effects.harmonic(y=y, margin=8)
print(len(y_harm))
chroma_os_harm = librosa.feature.chroma_cqt(y=y_harm, sr=sr, bins_per_octave=12*3)

chroma_filter = np.minimum(chroma_os_harm,
                           librosa.decompose.nn_filter(chroma_os_harm,
                                                       aggregate=np.median,
                                                       metric='cosine'))
chords = [[1,0,0,0,1,0,0,1,0,0,0,0], #c
          [1,0,0,1,0,0,0,1,0,0,0,0], #cm
          [0,0,1,0,0,0,1,0,0,1,0,0], #d
          [0,0,1,0,0,1,0,0,0,1,0,0], #dm 
          [0,0,0,0,1,0,0,0,1,0,0,1], #e
          [0,0,0,0,1,0,0,1,0,0,0,1], #em
          [1,0,0,0,0,1,0,0,0,1,0,0], #f
          [1,0,0,0,0,1,0,0,1,0,0,0], #fm
          [0,0,1,0,0,0,0,1,0,0,0,1], #g
          [0,0,1,0,0,0,0,1,0,0,1,0], #gm
          [1,0,0,0,1,0,0,0,1,0,0,0], #a
          [1,0,0,0,1,0,0,0,0,1,0,0], #am
          [0,0,1,0,0,0,1,0,0,0,0,1], #b
          [0,0,0,1,0,0,1,0,0,0,0,1]] #bm
names = ['c', 'cm', 'd', 'dm', 'e', 'em', 'f', 'fm', 'g', 'gm', 'a', 'am', 'b', 'bm']

# And for comparison, we'll show the CQT matrix as well.
C = np.abs(librosa.cqt(y=y, sr=sr, bins_per_octave=12*3, n_bins=7*12*3))

chroma_smooth = scipy.ndimage.median_filter(chroma_filter, size=(1, 9))

l = len(chroma_smooth[0])

print(l)

chordsToAveragise = 100

s = [0]*(l+chordsToAveragise)

for i in range(l):
    m = 0
    chord = 0
    for k in range(len(chords)):
        c = 0
        for n in range(len(chords[0])):
            c += chroma_smooth[n][i]*chords[k][n]
        if c > m :
            m = c
            chord = k
    s[i] = chord

f = open('chords.out', 'wb')
pickle.dump({'chrds' : s, 'samples' : len(y), 'sr' : sr, 'tempo' : tempo}, f)
f.close()

import process
