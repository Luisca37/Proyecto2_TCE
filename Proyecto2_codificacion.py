import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from rcosdesign import rcosdesign
import hamming_74 as hamming
import numpy as np
import random
#-----------Funciones-------------------#


def detector_umbral(señal, umbral, L):
    bits_rx = []
    cont = L
    umbral = 0
    bits_con_error = 0
    for i in señal:
        if cont == L:
            if i > umbral:
                bits_rx.append(1)
            else:
                bits_rx.append(0)
            
            # Comparar con los bits originales y contar los errores
            if bits_rx[-1] != data_bit[len(bits_rx) - 1]:
                bits_con_error += 1 #se calcula los bits con error al comparar con dato original
            
            cont = 0
        cont += 1

    return bits_rx, bits_con_error


#funcion que agrega ISI a la señal
def isi(signal, L, isi_factor):
    # Crear un filtro con forma de pulso rectangular y duración de L*isi_factor
    isi_filter = np.ones(int(L * isi_factor))
    # Normalizar el filtro para mantener la amplitud
    isi_filter /= np.sum(isi_filter)

    # Aplicar convolución para introducir ISI
    isi_signal = np.convolve(signal, isi_filter, 'full')[:len(signal)]

    return isi_signal



np.random.seed(324)

Ns = 12 #divisible por 4

Ts = 1
L = 16
t_step = Ts / L
factor_ruido = 0.5


rolloff = 0.75
# 1. Generacion de onda del pulso
pt = rcosdesign(rolloff, 6, L, 'sqrt')
pt = pt / (np.max(np.abs(pt)))  # rescaling to match rcosine


data_bit = (np.random.rand(Ns) > 0.5).astype(int)
print(data_bit)


#Codificacion con Hamming Code
encoded_data = hamming.encode_frame(data_bit)



print("Datos codificados con Hamming Code:", encoded_data)

#Unipolar a Bipolar (modulacion de amplitud)
amp_modulated = 2 * data_bit - 1  # 0=> -1,  1=>1
#amp_modulated = data_bit
#Modulacion de pulsos

encoded_data[2] = encoded_data[2]^1
encoded_data[3] = encoded_data[3]^1

encoded_data[10] = encoded_data[10]^1
print('Datos codificados con error:', encoded_data)
#Decodificacion Hamming Code
decoded_data, num_error = hamming.decode_frame(encoded_data)


print("Datos decodificados con Hamming Code:", decoded_data)