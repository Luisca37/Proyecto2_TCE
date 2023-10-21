import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from rcosdesign import rcosdesign
import CRC
import numpy as np

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

Ns = 16 #divisible por 4

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


# 2. Codificacion con Hamming Code
simbolo = 0
cont_simbolo = 0
encoded_data = []
for i in data_bit:
    if cont_simbolo == 4:
        simbolo = data_bit[i-4:i]
        cont_simbolo = 0
        simbolo_codificado = CRC.encode_with_hamming(simbolo)
        encoded_data.append(simbolo_codificado)

print("Datos codificados con Hamming Code:", encoded_data)

# 3. Unipolar a Bipolar (modulacion de amplitud)
amp_modulated = 2 * data_bit - 1  # 0=> -1,  1=>1
#amp_modulated = data_bit
# 4. Modulacion de pulsos
print(amp_modulated)