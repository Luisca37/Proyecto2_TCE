import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss
from scipy.signal import lfilter
from rcosdesign import rcosdesign


def nrz_polar_encoding(data):
    encoded_signal = []
    for bit in data:
        if bit == 1:
            encoded_signal.extend([1, -1])  # 1 se representa con una transición de +1 a -1
        else:
            encoded_signal.extend([-1, 1])  # 0 se representa con una transición de -1 a +1
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
    plt.show()





# Ejemplo de uso
data = [1, 0, 1, 1, 0, 0, 1]
encoded_data = nrz_polar_encoding(data) # a[k]
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
