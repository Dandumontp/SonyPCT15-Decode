import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps 

# Les trucs importants

fs, data = wav.read('test.wav') #On importe le WAV
datacalib=data[35280:44470] # On sauve la zone de calibration
data=data[35280:] # On crop les 800 ms (44100 * 0,8 ms) de signal d'ouverture
data=data[9190:] # crop de la zone de test (franchement à l'arrache)

# On récupère l'enveloppe du signal de calibration

def hilbert(datacalib):
    analytical_signal = signal.hilbert(datacalib)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope
datacalib_am = hilbert(datacalib)

# Calcul de l'amplitude Max

max=0
for q in range(datacalib_am.shape[0] - 1):
    val=datacalib_am[q] 
    if val > max:
        max=val
newmax=max//255 # Division par 255 (valeur max d'un pixel)

# Les données utiles

def hilbert(data):
    analytical_signal = signal.hilbert(data)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope
data_am = hilbert(data)

#La longueur d'une frame est la fréquence d'échantillonnage (44100) divisée par la fréquence de la porteuse (3579545/2^11) multiplié par 96 (96 pixels par ligne) 1748 est une approximation

#frame_width = ((fs//1748)*96) 
# Utiliser la bonne valeur : 3579545/2^11*96
frame_width = 2422
w, h = frame_width, data_am.shape[0]//frame_width

# Création d'une image monochrome

image = Image.new('L', (w, h))
px, py = 0, 0

for p in range(data_am.shape[0] - 1):
    lum = int(data_am[p]//newmax) # le // est une division entière
    if lum < 0: lum = 0 # probablement inutile, mais on essaye de rester entre 0 et 255
    if lum > 255: lum = 255 
    image.putpixel((px, py), (lum)) # On met le pixel
    px += 1  
    if px >= w:
        px = 0 
        py += 1
        if py >= h:
            break
           
image = ImageOps.invert(image) # Inversion de l'image pour les couleurs
image = image.resize((w//(fs//1748), h)) # Ici, l'approximation 1748 suffit
 
image.save(r'test.png') # On sauve l'image