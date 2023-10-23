import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from rcosdesign import rcosdesign
import numpy as np
import hamming_74 as hamming
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

Ns = 64

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



# 3. Unipolar a Bipolar (modulacion de amplitud)
amp_modulated = 2 * data_bit - 1  # 0=> -1,  1=>1
#amp_modulated = data_bit
# 4. Modulacion de pulsos
print(amp_modulated)


plt.figure(1)
plt.plot(data_bit, drawstyle='steps-post', label='Señal original')
plt.plot(amp_modulated, drawstyle='steps-post', label='NRZ Polar')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Codificación NRZ Polar')
plt.legend()
plt.grid()



impulse_modulated = np.zeros(Ns * L)
for n in range(Ns):
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
plt.stem(np.arange(t_step,Ns*Ts+t_step,t_step),impulse_modulated,markerfmt='.')
plt.axis([0,Ns*Ts,-2*np.max(impulse_modulated),2*np.max(impulse_modulated)])
plt.grid(True)
plt.title('Pulsomodulado')

plt.subplot(2,1,2)
plt.plot(np.arange(t_step,t_step*len(tx_signal)+t_step,t_step),tx_signal)
plt.axis([0,Ns*Ts,-2*np.max(tx_signal),2*np.max(tx_signal)])
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
print(filtro_acoplado)
print(len(filtro_acoplado))

#Grafica la señal Recibida
t_rx = np.arange(0, len(filtro_acoplado)) * t_step
plt.figure(6)
plt.plot(t_rx, filtro_acoplado)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señal Filtrada')
plt.grid(True)


#---------------Decodificacion------------------#


bits_rx, bits_con_error = detector_umbral(filtro_acoplado, 0, L)

print("Bits originales:", data_bit)
print("Bits detectados:", bits_rx)
print("Número de errores:", bits_con_error)






#---------------Potencia de señales----------------#


print("\n--------------Potencia de señales-------------\n")
print("Potencia pulsos originales: ",np.mean(np.square(data_bit)),"Vrms")
print("Potencia señal NRZ: ",np.mean(np.square(amp_modulated)),"Vrms")
print("Potencia pulsos transmitidos: ",np.mean(np.square(impulse_modulated)),"Vrms")
# Señal modulada continua
t_continuo = np.linspace(0, Ns * Ts, Ns * L, endpoint=False)  # Tiempo continuo

# Calcular la potencia de la señal continua
potencia_tx_continua = np.trapz(tx_signal**2, t_continuo) / (Ns * Ts)
print("Potencia de la señal continua transmitida:", potencia_tx_continua,"Vrms")

potencia_rx_continua = np.trapz(rx_signal**2, t_continuo) / (Ns * Ts)
print("Potencia de la señal con ISI y ruido:", potencia_rx_continua,"Vrms")

potencia_acoplado_continua = np.trapz(filtro_acoplado**2, t_continuo) / (Ns * Ts)
print("Potencia de la señal filtrada:", potencia_acoplado_continua,"Vrms")

plt.show()
sys.exit(0)