import pyaudio
import numpy as np
from matplotlib.mlab import find
import math
import serial
import keyboard


CHUNK = 2**11
RATE = 44100
MAX_AMP = 16000.0 # <- Adjust this based on input level
MAX_FREQ = 10000.0
RATE_OF_CHANGE = 500 # amount to adjust max values
PORT = '/dev/cu.usbmodem100'

# arrow key codes
left_arrow  = 37
up_arrow    = 38
right_arrow = 39
down_arrow  = 40

# current vars
current_amp = MAX_AMP;
current_freq = MAX_FREQ;

# amp vs freq will be hard coded for now
# 0 = amp 1 = freq
amp_freq = 0;

# switch between running, whole string, image
# controlled with the Makey Makey controller
# running = 0, whole string = 1, image = 2
mode_type = 0  #always default to amplitude

# controlled with the Makey Makey controller
# if we have n numbers of ramps in a mode, then if mod(n+1) = 0 then we can change modes
# current index inside the current color_ramps[mode_type] array
ramp_index = 0 

color_ramps = [((0, 0, 0), (0, 0, 0), (54, 2, 2), (90, 0, 0), (126, 0, 0), (165, 0, 0), (209, 0, 0), (237, 0, 0), (255, 0, 0), (255, 35, 35), (255, 76, 76), (255, 115, 115), (255, 148, 148), (255, 187, 187), (255, 226, 226)),
((0, 0, 0), (0, 0, 0), (2, 54, 2), (0, 90, 0), (0, 126, 0), (0, 165, 0), (0, 209, 0), (0, 237, 0), (0, 237, 0), (35, 255, 35), (76, 255, 76), (115, 255, 115), (148, 255, 148), (187, 255, 187), (226, 255, 226)), 
((80, 233, 246), (106, 198, 243), (134, 162, 238) , (165, 119, 234), (196, 79, 230), (225, 40, 226) , (248, 10, 223)),
((80, 233, 246), (76, 234, 232), (65, 237, 199) , (52, 240, 159), (39, 244, 118), (24, 248, 75) , (12, 251, 37), (3, 254, 9)),
((255, 0, 28), (255, 0, 253), (141, 0, 255) , (0, 26, 255), (0, 255, 238), (0, 255, 33) , (161, 255, 0), (255, 225, 0), (255, 95, 0)),
((0, 255, 2), (0, 198, 94), (8, 84, 255) , (112, 25, 255), (159, 7, 255), (158, 7, 255) ),
((246, 249, 3), (247, 226, 3), (249, 192, 0) , (250, 152, 1), (252, 114, 1), (253, 75, 1) , (254, 44, 0), (255, 24, 0)),
((1, 251, 255), (53, 255, 189), (198, 255, 21) , (250, 244, 0), (255, 158, 72), (255, 69, 161) , (255, 3, 227))]

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


while True:
    #detect keypress and if we receive the right key we will increment a counter
    if keyboard.is_pressed('space'): 
        ramp_index+=1
        if ramp_index > len(color_ramps):
            #change the mode and reset the counter
            ramp_index = 0;
            if (mode_type < 2):
                mode_type+=1;
            else:
                mode_type = 0;            
        else:
            #increase the counter inside the same mode
            ramp_index+=1;


    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)

    #set the number of color ramps we have
    num_colors = len(color_ramps[ramp_index])


    #determine the mode and act accordingly
    if amp_freq == 0:
        if keyboard.is_pressed(down_arrow): 
            if (current_amp > RATE_OF_CHANGE): # whats the lowest we can go here
                current_amp = current_amp - RATE_OF_CHANGE
        if keyboard.is_pressed(up_arrow): 
            if (current_amp < MAX_AMP):
                current_amp = current_amp + RATE_OF_CHANGE

        #use the amplitude mode
        peak=np.average(np.abs(data))*2
        amp = peak/current_amp
        #print peak
        for j in range(num_colors):
            if amp > j/(float(num_colors)):
                color = color_ramps[ramp_index][j]
    elif amp_freq == 1:
        if keyboard.is_pressed(down_arrow): 
            if (current_freq > RATE_OF_CHANGE): #whats the lowest we can go here?
                current_freq = current_freq - RATE_OF_CHANGE
        if keyboard.is_pressed(up_arrow): 
            if (current_freq < MAX_FREQ):
                current_freq = current_freq + RATE_OF_CHANGE

        #use the frequency mode
        Frequency=Pitch(data)
        print "%f Frequency" %Frequency        
        for j in range(num_colors):
            if Frequency/current_freq > j/(float(num_colors)):
                color = color_ramps[ramp_index][j]

    # Arduino expects mode, R, G, B over Serial
    print("{0},{1},{2},{3}".format(mode_type, color[0], color[1], color[2]))
    ser.write("{0},{1},{2},{3},".format(mode_type, color[0], color[1], color[2]))

    #counter += 1
    #if (counter > 100):
    #    i = (i + 1) % 2
    #    counter = 0


ser.close()
stream.stop_stream()
stream.close()
p.terminate()
