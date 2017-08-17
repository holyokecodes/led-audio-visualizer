import pyaudio
import numpy as np
from matplotlib.mlab import find
import math
import serial

CHUNK = 2**11
RATE = 44100
MAX_AMP = 16000.0 # <- Adjust this based on input level
MAX_FREQ = 10000.0
PORT = '/dev/cu.usbmodem27'

# Not used currently, may be used to tell Arduino to update whole string
# rather than moving each pixel to the next LED.
mode = 0

# switch between amplitude and frequency modes
amp_mode = 1

color_ramp = [((0, 0, 0), (0, 0, 0), (54, 2, 2), (90, 0, 0), (126, 0, 0), (165, 0, 0), (209, 0, 0), (237, 0, 0), (255, 0, 0), (255, 35, 35), (255, 76, 76), (255, 115, 115), (255, 148, 148), (255, 187, 187), (255, 226, 226)),
((0, 0, 0), (0, 0, 0), (2, 54, 2), (0, 90, 0), (0, 126, 0), (0, 165, 0), (0, 209, 0), (0, 237, 0), (0, 237, 0), (35, 255, 35), (76, 255, 76), (115, 255, 115), (148, 255, 148), (187, 255, 187), (226, 255, 226))]

# More colors needed here...
freq_colors = [(255,0,0),(0,255,0),(0,0,255)]

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

ser = serial.Serial(port=PORT, baudrate=9600)

def Pitch(signal):
    signal = np.fromstring(signal, 'Int16');
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0;

# used to switch between color ramps
# how often to switch - maybe this should be done with the Makey Makey controller?
counter = 0
i = 0 # index of the color_ramp array

while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    if amp_mode:
        peak=np.average(np.abs(data))*2
        amp = peak/MAX_AMP
        print peak
        num_colors = len(color_ramp[i])
        for j in range(num_colors):
            if amp > j/(float(num_colors)):
                color = color_ramp[i][j]
    else:
        Frequency=Pitch(data)
        print "%f Frequency" %Frequency
        num_colors = len(freq_colors)
        for j in range(num_colors):
            if Frequency/MAX_FREQ > j/(float(num_colors)):
                color = freq_colors[j]

    # Arduino expects mode, R, G, B over Serial
    print("{0},{1},{2},{3}".format(mode, color[0], color[1], color[2]))
    ser.write("{0},{1},{2},{3},".format(mode, color[0], color[1], color[2]))

    counter += 1
    if (counter > 100):
        i = (i + 1) % 2
        counter = 0


ser.close()
stream.stop_stream()
stream.close()
p.terminate()
