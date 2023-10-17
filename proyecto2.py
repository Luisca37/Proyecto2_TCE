import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from rcosdesign import rcosdesign
import numpy as np



np.random.seed(324)

Ns = 8

Ts = 1
L = 16
t_step = Ts / L
factor_ruido = 1


rolloff = 0.1
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

#---------------Recepcion------------------#    


#Generarnumerosaleatoriosdebajamagnitudcomoruido
length_tx_signal=len(tx_signal)
randn_array=factor_ruido*np.random.randn(1,length_tx_signal)

#Se agrega ruido a la señal transmitida
rx_signal=tx_signal+randn_array[0]


#Grafica la señal ruidosa
t_rx = np.arange(0, len(rx_signal)) * t_step
plt.figure(5)
plt.plot(t_rx, rx_signal)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señal con ruido antes de filtrar')
plt.grid(True)


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

#Detector de Umbral
bits_rx = []
cont = L
umbral = 0

for i in filtro_acoplado:


    if cont == L:
        if i > umbral:
            bits_rx.append(1)
        else:
            bits_rx.append(0)
        cont = 0
    cont+=1

print(bits_rx)


plt.show()
sys.exit(0)