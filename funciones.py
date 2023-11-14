import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from rcosdesign import rcosdesign
import numpy as np

def detector_umbral(señal, umbral, L):
    bits_rx = []
    tiempos = []
    valores = []
    cont = L
    for i, valor in enumerate(señal):
        if cont == L:
            if valor > umbral:
                bits_rx.append(1)
            else:
                bits_rx.append(0)
            tiempos.append(i)
            cont = 0
            valores.append(valor)
        cont += 1
    return bits_rx, valores, tiempos

    return bits_rx
def detector_umbralNRZ(señal, umbral, L):
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
    print("bits_rx:",bits_rx)
    return bits_rx

def detector_umbralRZ(señal, umbral, L):
    bits_rx = []
    cont = L
    for i in señal:
        if cont == 2*L:
            if i > umbral:
                bits_rx.append(1)
            elif i==0:
                continue
            elif i<umbral:
                bits_rx.append(0)           
            cont = 0
        cont += 1
    print ("bits_rx:",bits_rx)
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

#codificacion RZ polar
def rz_polar_encoding(data):
    encoded_signal = []
    for bit in data:
        if bit == 1:
            encoded_signal.extend([1, 0])  # 1 se representa con +1, seguido de 0
        else:
            encoded_signal.extend([-1, 0])  # 0 se representa con -1, seguido de 0
    return encoded_signal

def plot_eye_diagram(signal, samples_per_bit, tiempo_actual):
    signal_len = len(signal)
    num_bits = signal_len // samples_per_bit
    eye_width = samples_per_bit

    eye_diagram = np.zeros((num_bits, eye_width))

    for i in range(num_bits):
        start = i * samples_per_bit
        end = start + eye_width
        eye_diagram[i] = signal[start:end]

    # Graficar el diagrama de ojo
    
    plt.figure(11)
    plt.title('Diagrama de Ojo')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.grid(True)

    for i in range(eye_diagram.shape[0]):
        plt.plot(eye_diagram[i], label=f'Bit {i}')

    plt.show