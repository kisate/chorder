from __future__ import print_function
from __future__ import division
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.ticker import FuncFormatter, MaxNLocator, FormatStrFormatter

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

f = open('chords.out', 'rb')
inp = pickle.load(f)
f.close()

s = inp['chrds']
samples = inp['samples']
sr = inp['sr']
tempo = inp['tempo']
s2 = list(s)

t = samples//sr*tempo/240
print(tempo)
o = [0]*len(chords)

chordsToAveragise = int(len(s)//t)
print(chordsToAveragise)

l = len(s)-chordsToAveragise

for j in range(l):
    o = [0]*len(chords)
    for i in range(j, j+chordsToAveragise) :
        o[s[i]]+=1
    #s[j] = o.index(max(o))

i = 0
while(i < (l-t*2)) :
    o = [0]*len(chords)
    g = i
    for i in range(g, min(int(g+t*2), l)) :
        o[s2[i]]+=1
    m = o.index(max(o))
    for g in range(g, min(int(g+t*2), l)) :
        s2[g] = m

            
plt.figure(figsize=(16, 12))

plot = plt.subplot(2,1,1)

plt.ylabel('Chords')
plt.xlabel('Beats')

def yformat_fn(tick_val, tick_pos):
    if int(tick_val) in range(len(names)):
        return names[int(tick_val)]
    else:
        return ''
def xformat_fn(tick_val, tick_pos):
    return int(tick_val/(t*2))


plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
plot.yaxis.set_major_locator(MaxNLocator(integer=True))

#plt.tight_layout()


plot.plot(s)
plt.xlim(xmin=0.0)
plt.ylim(ymin=0.0)

plt.yticks(range(12))
start, end = plot.get_xlim()
plot.xaxis.set_ticks(np.arange(start, end, t*2))
plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
plot.grid()

plot = plt.subplot(2,1,2)

#plt.tight_layout()

plt.ylabel('Chords')
plt.xlabel('Beats')

plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
plot.yaxis.set_major_locator(MaxNLocator(integer=True))

plot.plot(s2)
plt.xlim(xmin=0.0)
plt.ylim(ymin=0.0)

plt.yticks(range(12))
start, end = plot.get_xlim()
plot.xaxis.set_ticks(np.arange(start, end, t*2))
plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
plot.grid()

plt.show()
