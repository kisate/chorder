""" from midi2audio import FluidSynth 
import glob
path = 'chordchromas/midis/c/*'
fs = FluidSynth()
print(glob.glob(path))
fs.midi_to_audio('inp.mid', 'output.wav')
for i, filename in enumerate(glob.glob(path)):
    fs.midi_to_audio(r'chordchromas/midis/c/c-str.mid', 'output.mp3')
 """
 