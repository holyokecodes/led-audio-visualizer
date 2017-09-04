import pyaudio
import numpy as np
from matplotlib.mlab import find
import math
import serial


CHUNK = 2**11
RATE = 44100
MAX_AMP = 16000.0 # <- Adjust this based on input level
MAX_FREQ = 10000.0
PORT = '/dev/cu.usbmodem1411'

# Within each mode type, we can define many color ramps
# We will reference these by the index of the ramp
ramp_index = 0

# switch between amplitude, frequency, and random modes
# amplitude = 0 frequency = 1 random = 2
mode_type = 0

pins = [0]

amp_color_ramps = [((0, 0, 0), (0, 0, 0), (54, 2, 2), (90, 0, 0), (126, 0, 0), (165, 0, 0), (209, 0, 0), (237, 0, 0), (255, 0, 0), (255, 35, 35), (255, 76, 76), (255, 115, 115), (255, 148, 148), (255, 187, 187), (255, 226, 226)),
((0, 0, 0), (0, 0, 0), (2, 54, 2), (0, 90, 0), (0, 126, 0), (0, 165, 0), (0, 209, 0), (0, 237, 0), (0, 237, 0), (35, 255, 35), (76, 255, 76), (115, 255, 115), (148, 255, 148), (187, 255, 187), (226, 255, 226)), 
((80, 233, 246), (106, 198, 243), (134, 162, 238) , (165, 119, 234), (196, 79, 230), (225, 40, 226) , (248, 10, 223)),
((80, 233, 246), (76, 234, 232), (65, 237, 199) , (52, 240, 159), (39, 244, 118), (24, 248, 75) , (12, 251, 37), (3, 254, 9)),
((255, 0, 28), (255, 0, 253), (141, 0, 255) , (0, 26, 255), (0, 255, 238), (0, 255, 33) , (161, 255, 0), (255, 225, 0), (255, 95, 0)),
((0, 255, 2), (0, 198, 94), (8, 84, 255) , (112, 25, 255), (159, 7, 255), (158, 7, 255) ),
((246, 249, 3), (247, 226, 3), (249, 192, 0) , (250, 152, 1), (252, 114, 1), (253, 75, 1) , (254, 44, 0), (255, 24, 0)),
((1, 251, 255), (53, 255, 189), (198, 255, 21) , (250, 244, 0), (255, 158, 72), (255, 69, 161) , (255, 3, 227))]
freq_color_ramps = []

random_color_ramps = []

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
i = 5 # index of the color_ramp array

while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    #if amp_mode:
    peak=np.average(np.abs(data))*2
    amp = peak/MAX_AMP
    #print peak
    num_colors = len(amp_color_ramps[i])
    for j in range(num_colors):
        if amp > j/(float(num_colors)):
            color = amp_color_ramps[i][j]
    #else:
    #    Frequency=Pitch(data)
    #    print "%f Frequency" %Frequency
    #    num_colors = len(freq_colors)
    #    for j in range(num_colors):
    #        if Frequency/MAX_FREQ > j/(float(num_colors)):
    #            color = freq_colors[j]

    # Arduino expects mode, R, G, B over Serial
    print("{0},{1},{2},{3},{4}".format(pins[0], mode_type, color[0], color[1], color[2]))
    ser.write("{0},{1},{2},{3},{4},".format(pins[0], mode_type, color[0], color[1], color[2]))

    #counter += 1
    #if (counter > 100):
    #    i = (i + 1) % 2
    #    counter = 0


ser.close()
stream.stop_stream()
stream.close()
p.terminate()
