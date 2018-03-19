from __future__ import print_function
from __future__ import division
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.ticker import FuncFormatter, MaxNLocator, FormatStrFormatter
import librosa
import librosa.display

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

l = len(data[0])-chordsToAveragise
t = samples//sr*tempo/240
def filter1() : 
    chordsToAveragise = 100

    s = [0]*(l+chordsToAveragise)

    for i in range(l):
        m = 0
        chord = 0
        for k in range(len(chords)):
            c = 0
            for n in range(len(chords[0])):
                c += data[n][i]*chords[k][n]
            if c > m :
                m = c
                chord = k
        s[i] = chord
        
    return s
    
def filter2() :

    s = filter1()
    
    
    print(tempo)
    o = [0]*len(chords)

    chordsToAveragise = int(len(s)/t/2)
    print(chordsToAveragise)

    l = len(s)-chordsToAveragise

    for j in range(l):
        o = [0]*len(chords)
        for i in range(j, j+chordsToAveragise) :
            o[s[i]]+=1
        s[j] = o.index(max(o))
    return s

def filter3() :

    s = filter1()
    i = 0
    while(i < (l-len(s)//(2*t))) :
        o = [0]*len(chords)
        g = i
        for i in range(g, min(int(g+len(s)//(2*t)), l)) :
            o[s[i]]+=1
        m = o.index(max(o))
        for g in range(g, min(int(g+len(s)//(2*t)), l)) :
            s[g] = m
    return s
    
def filter4() :
    
    i = 0
    
    c = int(len(data[0])//t)
    
    res = [0]*len(data[0])
    
    while(i < len(data[0]) - c):
        s = [0]*len(chords)
        for g in range(len(chords)):
            for j in range(i, i+c):
               s[g] += sum([chords[g][x]*data[x][i] for x in range(len(data))])
        chord = s.index(max(s))
        for i in range(i, i+c):
            res[i] = chord
    
    return res
            
plt.figure(figsize=(12, 9))

plot = plt.subplot(3,1,1)

# librosa.display.specshow(data, y_axis='chroma')
# plt.ylabel('Original')
# plt.colorbar()

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

plt.tight_layout()


plot.plot(filter2())
plt.xlim(xmin=0.0)
plt.ylim(ymin=0.0)

plt.yticks(range(len(chords)))
start, end = plot.get_xlim()
plot.xaxis.set_ticks(np.arange(start, end, t*2))
plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
plot.grid()

plot = plt.subplot(3,1,2)

#plt.tight_layout()

plt.ylabel('Chords')
plt.xlabel('Beats')

plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
plot.yaxis.set_major_locator(MaxNLocator(integer=True))

plot.plot(filter3())
plt.xlim(xmin=0.0)
plt.ylim(ymin=0.0)

plt.yticks(range(len(chords)))
start, end = plot.get_xlim()
plot.xaxis.set_ticks(np.arange(start, end, t*2))
plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
plot.grid()

plot = plt.subplot(3,1,3)

#plt.tight_layout()

plt.ylabel('Chords')
plt.xlabel('Beats')

plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
plot.yaxis.set_major_locator(MaxNLocator(integer=True))

plot.plot(filter4())
plt.xlim(xmin=0.0)
plt.ylim(ymin=0.0)

plt.yticks(range(len(chords)))
start, end = plot.get_xlim()
plot.xaxis.set_ticks(np.arange(start, end, t*2))
plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
plot.grid()



plt.show()
