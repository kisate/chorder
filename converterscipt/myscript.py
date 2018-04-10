import pygame
import wave 
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)

# create a sound from NumPy array of file
pygame.mixer.music.load('inp.mid')

# open new wave file
sfile = wave.open('pure_tone.wav', 'w')

# set the parameters
sfile.setframerate(44100)
sfile.setnchannels(1)
sfile.setsampwidth(2)

# write raw PyGame sound buffer to wave file
sfile.writeframesraw(snd.get_buffer().raw)

# close file
sfile.close()