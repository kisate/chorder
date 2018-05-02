from __future__ import print_function
from pprint import pprint
import numpy as np
import scipy
import matplotlib.pyplot as plt
import pickle
import librosa
import librosa.display
import glob


for filename in glob.iglob('chordchromas/mp3s/c/*.mp3'):

    savepath = 'chordchromas/chromas/c/' + filename[20:-4] + '.out'

    y, sr = librosa.load(filename)

    print(len(y))

    tempo = librosa.beat.tempo(y, sr)

    print(tempo)

    y_harm = librosa.effects.harmonic(y=y, margin=12)
    chroma_orig = librosa.feature.chroma_cqt(y=y, sr=sr)
    #print(len(y_harm))
    chroma_os_harm = librosa.feature.chroma_cqt(y=y_harm, sr=sr, n_chroma=12, bins_per_octave=12*5, hop_length=256)

    filtered = librosa.decompose.nn_filter(chroma_orig)

    chroma_filter = np.minimum(chroma_orig, filtered)
    # And for comparison, we'll show the CQT matrix as well.
    #C = np.abs(librosa.cqt(y=y, sr=sr, bins_per_octave=12*3, n_bins=7*12*3))

    chroma_smooth = scipy.ndimage.median_filter(chroma_filter, size=(1, 9))

    #l = len(chroma_smooth[0])

    #print(l)

    f = open(savepath, 'wb')
    pickle.dump({'data' : chroma_orig, 'samples' : len(y), 'sr' : sr, 'tempo' : tempo}, f)
    f.close()

    import process

    process.process(savepath)
