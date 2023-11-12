import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss
from scipy.signal import lfilter
from rcosdesign import rcosdesign


def nrz_encoding(data):
    encoded_signal = []
    for bit in data:
        if bit == 1:
            encoded_signal.extend([1] * 2)  # 1 se representa con una señal constante alta
        else:
            encoded_signal.extend([-1] * 2)  # 0 se representa con una señal constante baja
    return encoded_signal

def plot_nrz_polar(data, encoded_data):
    plt.figure(figsize=(10, 2))
    plt.plot(data, drawstyle='steps-post', label='Señal original')
    plt.plot(encoded_data, drawstyle='steps-post', label='NRZ Polar')
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Codificación NRZ Polar')
    plt.legend()
    plt.grid()
    #plt.show()



Ns=16


def rz_polar_encoding(data):
    encoded_signal = []
    for bit in data:
        pos=0
        if bit == 1:
            encoded_signal.extend([1, 0])  # 1 se representa con +1, seguido de 0
        else:
            encoded_signal.extend([-1, 0])  # 0 se representa con -1, seguido de 0
    return encoded_signal

def plot_rz_polar(data, encoded_data):
    plt.figure(figsize=(10, 2))
    plt.plot(data, drawstyle='steps-post', label='Señal original')
    plt.plot(encoded_data, drawstyle='steps-post', label='RZ Polar')
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Codificación RZ Polar')
    plt.legend()
    plt.grid()
    #plt.show()

# Ejemplo de uso
data = [1, 0, 1, 1, 0, 0, 1]
encoded_data = rz_polar_encoding(data)
plot_rz_polar(data, encoded_data)



def manchester_encoding(data):
    encoded_signal = []
    for bit in data:
        if bit == 1:
            encoded_signal.extend([1, -1])  # 1 se representa con una transición de +1 a -1
        else:
            encoded_signal.extend([-1, 1])  # 0 se representa con una transición de -1 a +1
    return encoded_signal

def plot_manchester(data, encoded_data):
    plt.figure(figsize=(10, 2))
    plt.plot(data, drawstyle='steps-post', label='Señal original')
    plt.plot(encoded_data, drawstyle='steps-post', label='Manchester')
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Codificación Manchester')
    plt.legend()
    plt.grid()
    plt.show()

# Ejemplo de uso
#data = [1, 0, 1, 1, 0, 0, 1]
encoded_data = manchester_encoding(data)
plot_manchester(data, encoded_data)















# Ejemplo de uso
#data = [1, 0, 1, 1, 0, 0, 1]
#data = (np.random.rand(Ns) > 0.5).astype(int)
encoded_data = nrz_encoding(data) # a[k]
plot_nrz_polar(data, encoded_data)


Ts = 1
L = 16
t_step = Ts / L

#Generacion de respuesta del filtro
pt = rcosdesign(0.5, 6,  L, 'sqrt')
pt = pt/ (np.max(np.abs(pt))) 
data = np.array(encoded_data)
#tx_signal = np.convolve(data, pt)
tx_signal = lfilter(pt, 1, data)
#grafica de señal transmitida

t_tx = np.arange(0, len(tx_signal))*t_step
plt.figure(1)
plt.plot(t_tx , tx_signal)
plt.xlabel('Tiempo_[s]')
plt.ylabel('Amplitud')
plt.title('Señal transmitida')
plt.grid(True)
plt.show()


#Implementation of RZ Encoding Scheme
import matplotlib.pyplot as plt
import numpy as np
#Function for drwaing vertical dashed lines and Y-axis
def my_lines(ax, pos, *args, **kwargs):
    if ax == 'x':
        for p in pos:
            if(p!=0):
                plt.axvline(p,linestyle='dashed', *args, **kwargs)
            else:
                plt.arrow(0,0,0,3.9,head_width=0.05, head_length=0.1, fc='k', ec='k')
    else:
        for p in pos:
            plt.axhline(p, *args, **kwargs)
clock = []
bits = [0,1,0,0,1]
j=0
#Encoding of signal bits to RZ scheme signal bits
for i in range(len(bits)):
    if(bits[i]==1):
        clock.insert(j,1)
        clock.insert(j+1,0)
    elif(bits[i]==0):
            clock.insert(j,-1)
            clock.insert(j+1,0)
    j=j+2
clock.insert(j+1,0)
data=np.repeat(clock,1)
t = 0.5 * np.arange(len(data))
my_lines('x', range(len(bits)+1), color='black', linewidth=1)
plt.arrow(0, 2,len(bits)+1-0.1, 0, head_width=0.05, head_length=0.1, fc='k', ec='k')
plt.step(t, data+2, 'r', linewidth = 2.5, where='post')
plt.ylim([0,4])
plt.xlim([-0.1,len(bits)+1])
for tbit, bit in enumerate(bits):
    plt.text(tbit + 0.5, 3.5, str(bit))
plt.text(-0.2,4.1,'Amplitude');
plt.text(len(bits)+0.3,1.8,'Time');
plt.gca().axis('off')
plt.savefig("RZ.png")
plt.show()