import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from rcosdesign import rcosdesign
import numpy as np


def detector_umbral(señal, umbral, L):
    bits_rx = []
    cont = L
    umbral = 0
    for i in señal:
        if cont == L:
            if i > umbral:
                bits_rx.append(1)
            else:
                bits_rx.append(0)           
            cont = 0
        cont += 1

    return bits_rx

def contar_diferencias(array1, array2):
    # Inicializar una lista para almacenar las posiciones de las diferencias
    posiciones_errores = []
    num_errores = 0  # Inicializar el contador de errores

    # Asegurarnos de que ambos arrays tengan la misma longitud
    if len(array1) == len(array2):
        # Comparar los elementos de los arrays uno por uno
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                posiciones_errores.append(i)  # Agregar la posición al resultado
                num_errores += 1  # Incrementar el contador de errores

        return posiciones_errores, num_errores
    else:
        return "Los arrays no tienen la misma longitud"


#funcion que agrega ISI a la señal
def isi(signal, L, isi_factor):
    # Crear un filtro con forma de pulso rectangular y duración de L*isi_factor
    isi_filter = np.ones(int(L * isi_factor))
    # Normalizar el filtro para mantener la amplitud
    isi_filter /= np.sum(isi_filter)

    # Aplicar convolución para introducir ISI
    isi_signal = np.convolve(signal, isi_filter, 'full')[:len(signal)]

    return isi_signal


def codificar_pam4(data_bit):
    array_codificado = []

    for i in range(0, len(data_bit) - 1, 2):
        if data_bit[i] == 0 and data_bit[i + 1] == 0:
            array_codificado.append(-3)
        elif data_bit[i] == 0 and data_bit[i + 1] == 1:
            array_codificado.append(-1)
        elif data_bit[i] == 1 and data_bit[i + 1] == 0:
            array_codificado.append(1)
        elif data_bit[i] == 1 and data_bit[i + 1] == 1:
            array_codificado.append(3)

    # Agregar el último valor si la longitud de data_bit es impar
    if len(data_bit) % 2 == 1:
        if data_bit[-1] == 0:
            array_codificado.append(-3)
        else:
            array_codificado.append(3)

    return array_codificado
