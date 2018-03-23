from __future__ import print_function
from __future__ import division
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.ticker import FuncFormatter, MaxNLocator, FormatStrFormatter
import librosa
import librosa.display

chords = [[0]*12]*14

notes = [0, 2, 4, 5, 7, 9, 11]

vals = [1, 1, 1]

def generateChords() :
    i = 0
    for n in notes :
        c = [0]*12
        c[n] = vals[0]
        c[(n+4)%12] = vals[1]
        c[(n+7)%12] = vals[2]
        chords[i] = c
        c = [0]*12
        c[n] = vals[0]
        c[(n+3)%12] = vals[1]
        c[(n+7)%12] = vals[2]
        i+=1
        chords[i] = c
        i+=1
    print(chords)

def process(path) : 

    bias = 10

    generateChords()
    
    names = ['C', 'Cm', 'D', 'Dm', 'E', 'Em', 'F', 'Fm', 'G', 'Gm', 'A', 'Am', 'B', 'Bm']

    chordsToAveragise = 100

    f = open(path, 'rb')
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

        s = filter5()
        
        
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


    def filter5() :

        s = [0]*len(data[0])
        
        for i in range(len(data[0])):
            chroma = [0]*12
            for j in range(12):
                chroma[j] = data[j][i]
            deltas = [0]*len(chords)
            for c in range(len(chords)):
                deltas[c] = getDelta(chroma, c)
            s[i] = deltas.index(min(deltas))
            #print(deltas)
        return s
            

    def getDelta(chroma, index):

        s = 0
        
        for i, c in enumerate(chroma) :
            s += (chords[index][i] - c)**2
        
        return (s**0.5)/(9*bias)
        
    tacts = int(samples/sr*tempo/240)
    fpt = int(len(data[0])/tacts)
    fpq = int(fpt*2)        
    def filter6() :
        s = filter5()
        

        i = 0
        while (i < len(s) - fpq) :
            c = [0]*len(chords)
            for j in range(i, i + fpq) :
                c[s[j]]+=1
            m = c.index(max(c))
            print(c)
            for i in range(i, i + fpq) :
                s[i] = m

        f = open('aaa.txt', 'w')
        f.write(str(s))
        f.close()
        
        return s


    print(int(samples/sr*tempo/240)) 
                
    plt.figure(figsize=(14, 8))

    plot = plt.subplot(4,1,1)

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

        i = 0
        while(i*fpq <= tick_val) : i+=1
        i-=1
        
        return i


    plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
    plot.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()


    plot.plot(filter5())
    plt.xlim(xmin=0.0)
    plt.ylim(ymin=0.0)

    plt.yticks(range(len(chords)))
    start, end = plot.get_xlim()
    plot.xaxis.set_ticks(np.arange(start, end, t*2))
    plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
    plot.grid()

    plot = plt.subplot(4,1,2)

    #plt.tight_layout()

    plt.ylabel('Chords')
    plt.xlabel('Beats')

    plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
    plot.yaxis.set_major_locator(MaxNLocator(integer=True))

    plot.plot(filter2())
    plt.xlim(xmin=0.0)
    plt.ylim(ymin=0.0)

    plt.yticks(range(len(chords)))
    start, end = plot.get_xlim()
    plot.xaxis.set_ticks(np.arange(start, end, t*2))
    plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
    plot.grid()

    plot = plt.subplot(4,1,3)

    #plt.tight_layout()

    plt.ylabel('Chords')
    plt.xlabel('Beats')

##    plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
##    plot.yaxis.set_major_locator(MaxNLocator(integer=True))
##
##    plot.plot(filter3())
##    plt.xlim(xmin=0.0)
##    plt.ylim(ymin=0.0)
##
##    plt.yticks(range(len(chords)))
##    start, end = plot.get_xlim()
##    plot.xaxis.set_ticks(np.arange(start, end, t*2))
##    plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
##    plot.grid()

    librosa.display.specshow(data, y_axis='chroma', x_axis='time')

    plot = plt.subplot(4,1,4)


    plt.ylabel('Chords')
    plt.xlabel('Beats')

    plot.yaxis.set_major_formatter(FuncFormatter(yformat_fn))
    plot.yaxis.set_major_locator(MaxNLocator(integer=True))

    x = filter6()

    plot.plot(x)
    plt.xlim(xmin=0.0)
    plt.ylim(ymin=0.0)

    plt.yticks(range(len(chords)))
    start, end = plot.get_xlim()
    print(len(x))
    print(start, end)
    plot.xaxis.set_ticks(np.arange(0, len(x), fpq))
    plot.xaxis.set_major_formatter(FuncFormatter(xformat_fn))
    plot.grid()
    plt.show()

process('tsoi1.out')
