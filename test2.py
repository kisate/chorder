from __future__ import print_function
from __future__ import division
from pprint import pprint
import numpy as np
import pickle
from matplotlib.ticker import FuncFormatter, MaxNLocator, FormatStrFormatter
import librosa
import librosa.display
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

bias = 10

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
names = ['C', 'Cm', 'D', 'Dm', 'E', 'Em', 'F', 'Fm', 'G', 'Gm', 'A', 'Am', 'B', 'Bm']

chordsToAveragise = 100

f = open('chords2.out', 'rb')
inp = pickle.load(f)
f.close()



data = inp['data']
samples = inp['samples']
sr = inp['sr']
tempo = inp['tempo']

s = [0,0,0,0,1,1,1,1,1,5,5,5,6,6,6,6]
fpq = 4

def yformat_fn(tick_val, tick_pos):
    if int(tick_val) in range(len(names)):
        return names[int(tick_val)]
    else:
        return ''
def xformat_fn(tick_val, tick_pos):
    return int(int(tick_val)/(fpq))


num_bins = len(s)

fig, plot = plt.subplots()

plt.ylabel('Chords')
plt.xlabel('Beats')

plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
plot.yaxis.set_major_locator(MaxNLocator(integer=True))

plot.plot(filter6())
plt.xlim(xmin=0.0)
plt.ylim(ymin=0.0)

n, bins, patches = plot.hist(x, len(x))

plt.yticks(range(len(chords)))
start, end = plot.get_xlim()
plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
plot.grid()
