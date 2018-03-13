from __future__ import print_function
from pprint import pprint
import numpy as np
import scipy
import matplotlib.pyplot as plt

import librosa
import librosa.display
# 1. Get the file path to the included audio example
filename = "track2.mp3"

# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
y, sr = librosa.load(filename)

chroma_orig = librosa.feature.chroma_cqt(y=y, sr=sr)
chroma_os = librosa.feature.chroma_cqt(y=y, sr=sr, bins_per_octave=12*3)
y_harm = librosa.effects.harmonic(y=y, margin=8)
chroma_os_harm = librosa.feature.chroma_cqt(y=y_harm, sr=sr, bins_per_octave=12*3)
chroma_filter = np.minimum(chroma_os_harm,
                           librosa.decompose.nn_filter(chroma_os_harm,
                                                       aggregate=np.median,
                                                       metric='cosine'))
chords = {'c' : [1,0,0,0,1,0,0,1,0,0,0,0],
          'cm' : [1,0,0,1,0,0,0,1,0,0,0,0],
          'd' : [0,0,1,0,0,0,1,0,0,1,0,0],
          'dm' : [0,0,1,0,0,1,0,0,0,1,0,0],
          'e' : [0,0,0,0,1,0,0,0,1,0,0,1],
          'em' : [0,0,0,0,1,0,0,1,0,0,0,1],
          'f' : [1,0,0,0,0,1,0,0,0,1,0,0],
          'fm' : [1,0,0,0,0,1,0,0,1,0,0,0],
          'g' : [0,0,1,0,0,0,0,1,0,0,0,1],
          'gm' : [0,0,1,0,0,0,0,1,0,0,1,0],
          'a' : [1,0,0,0,1,0,0,0,1,0,0,0],
          'am' : [1,0,0,0,1,0,0,0,0,1,0,0],
          'b' : [0,0,1,0,0,0,1,0,0,0,0,1],
          'bm' : [0,0,0,1,0,0,1,0,0,0,0,1]}
# For display purposes, let's zoom in on a 15-second chunk from the middle of the song
idx = [slice(None), slice(*list(librosa.time_to_frames([0, 300])))]

# And for comparison, we'll show the CQT matrix as well.
C = np.abs(librosa.cqt(y=y, sr=sr, bins_per_octave=12*3, n_bins=7*12*3))

chroma_smooth = scipy.ndimage.median_filter(chroma_filter, size=(1, 9))

l = len(chroma_smooth[0])

print(l)
s = ['']*l

for i in range(l):
    m = 0
    chord = 0
    d=0
    for k in chords.keys():
        c = 0
        for n in range(len(chords['c'])):
            c += chroma_smooth[n][i]*chords[k][n]
        if c > m :
            m = c
            chord = d
        d+=1
    s[i] = chord

print(s)
        
            

plt.figure(figsize=(12, 4))

plt.subplot(2, 1, 1)
librosa.display.specshow(chroma_smooth[idx], y_axis='chroma')
plt.colorbar()
plt.ylabel('Non-local')

plt.subplot(2, 1, 2)
plt.plot(s)
plt.colorbar()
plt.ylabel('Median-filtered')
plt.tight_layout()
plt.show()
