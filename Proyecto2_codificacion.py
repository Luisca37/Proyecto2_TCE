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
    # Inicializar una variable para contar las diferencias
    diferencias = 0

    # Asegurarnos de que ambos arrays tengan la misma longitud
    if len(array1) == len(array2):
        # Comparar los elementos de los arrays uno por uno
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                diferencias += 1

        return diferencias
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


np.random.seed(324)

Ns = 12 #divisible por 4
hamming_code = False
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


#Codifica con o sin Hamming
if hamming_code:
    encoded_data = np.array(hamming.encode_frame(data_bit))
else        :
    encoded_data = data_bit
Ns_code = len(encoded_data)


#Unipolar a Bipolar (modulacion de amplitud)
amp_modulated = 2*encoded_data - 1  # 0=> -1,  1=>1

# 4. Modulacion de pulsos
print(amp_modulated)


plt.figure(1)
plt.plot(encoded_data, drawstyle='steps-post', label='Señal original')
plt.plot(amp_modulated, drawstyle='steps-post', label='NRZ Polar')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Codificación NRZ Polar')
plt.legend()
plt.grid()



impulse_modulated = np.zeros(Ns_code * L)
for n in range(Ns_code):
    delta_signal = np.concatenate(([amp_modulated[n]], np.zeros(L - 1)))
    impulse_modulated[n * L: (n * L) + L] = delta_signal
    #impulse_modulated[n * L: (n + 1) * L] = delta_signal




tx_signal = ss.convolve(impulse_modulated, pt, mode='same')

# Grafica los pulsos
t_tx = np.arange(0, len(impulse_modulated)) * t_step
plt.figure(2)
plt.plot(t_tx, impulse_modulated)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Pulsos')
plt.grid(True)


# Grafica la señal transmitida
t_tx = np.arange(0, len(tx_signal)) * t_step
plt.figure(3)
plt.plot(t_tx, tx_signal)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señal Transmitida')
plt.grid(True)


plt.figure(4)
plt.subplot(2,1,1)
plt.stem(np.arange(t_step,Ns_code*Ts+t_step,t_step),impulse_modulated,markerfmt='.')
plt.axis([0,Ns_code*Ts,-2*np.max(impulse_modulated),2*np.max(impulse_modulated)])
plt.grid(True)
plt.title('Pulsomodulado')

plt.subplot(2,1,2)
plt.plot(np.arange(t_step,t_step*len(tx_signal)+t_step,t_step),tx_signal)
plt.axis([0,Ns_code*Ts,-2*np.max(tx_signal),2*np.max(tx_signal)])
plt.grid(True)
plt.title('Formadepulso')
plt.tight_layout()

#---------------Canal------------------#    


#Generar numeros aleatorios con distribucion normal para simuar el ruido
length_tx_signal=len(tx_signal)
randn_array=factor_ruido*np.random.randn(1,length_tx_signal)


#se agrega isi y ruido a la señal
isi_factor = 1 # Valor mayor para un ISI más pronunciado

rx_signal = isi(tx_signal, L, isi_factor)+randn_array[0]



# Graficar la señal con ISI y ruido
t_rx = np.arange(0, len(rx_signal)) * t_step
plt.figure(7)
plt.plot(t_rx, rx_signal)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señal con ISI y ruido')
plt.grid(True)




#----------------------------Receptor---------------#
#Filtro acoplado tiene la misma forma que pt debido a su simetria
filtro_acoplado = ss.convolve(rx_signal , pt, mode = 'same' )

filtro_acoplado /= np.sum(np.abs(pt)) #normalizacion


#Grafica la señal Recibida
t_rx = np.arange(0, len(filtro_acoplado)) * t_step
plt.figure(6)
plt.plot(t_rx, filtro_acoplado)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señal Filtrada')
plt.grid(True)


#---------------Decodificacion------------------#


bits_rx = detector_umbral(filtro_acoplado, 0, L)
print('Bits detectados con detector de umbral: ', bits_rx, '\n')

#se realiza la decodificacion con hamming code de ser necesario
if hamming_code:    
    decoded_data = np.array(hamming.decode_frame(bits_rx))
else:
    decoded_data = bits_rx


bits_con_error = contar_diferencias(data_bit, decoded_data)

print("Bits originales:", data_bit)
print("Bits detectados:", np.array(decoded_data))
print("Número de errores:", bits_con_error)






#---------------Potencia de señales----------------#


print("\n--------------Potencia de señales-------------\n")
print("Potencia pulsos originales: ",np.mean(np.square(encoded_data)),"Vrms")
print("Potencia señal NRZ: ",np.mean(np.square(amp_modulated)),"Vrms")
print("Potencia pulsos transmitidos: ",np.mean(np.square(impulse_modulated)),"Vrms")
# Señal modulada continua
t_continuo = np.linspace(0, Ns_code * Ts, Ns_code * L, endpoint=False)  # Tiempo continuo

# Calcular la potencia de la señal continua
potencia_tx_continua = np.trapz(tx_signal**2, t_continuo) / (Ns_code * Ts)
print("Potencia de la señal continua transmitida:", potencia_tx_continua,"Vrms")

potencia_rx_continua = np.trapz(rx_signal**2, t_continuo) / (Ns_code * Ts)
print("Potencia de la señal con ISI y ruido:", potencia_rx_continua,"Vrms")

potencia_acoplado_continua = np.trapz(filtro_acoplado**2, t_continuo) / (Ns_code * Ts)
print("Potencia de la señal filtrada:", potencia_acoplado_continua,"Vrms")

plt.show()
sys.exit(0)







