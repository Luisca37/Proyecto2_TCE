import matplotlib.pyplot as plt
import numpy as np

Ns=12
Ts = 1
L = 32
t_step = Ts / L

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

data_bit = [0, 0, 1, 0, 0, 1, 1, 1,0,1,1,0]
array_codificado = codificar_pam4(data_bit)
print(array_codificado)


t_tx = np.arange(0, len(array_codificado)) * t_step
plt.figure(1)
plt.step(t_tx, array_codificado, where='post')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Modulación PAM-4')
plt.grid()
plt.show()



Ns_mecago=Ns/2
print(Ns_mecago)
impulse_modulated = np.zeros(int(Ns_mecago * L))
for n in range(int(Ns_mecago)):
    delta_signal = np.concatenate(([array_codificado[n]], np.zeros(L - 1)))
    impulse_modulated[n * L: (n * L) + L] = delta_signal
 

t_tx = np.arange(0, len(impulse_modulated)) * t_step
plt.figure(2)
plt.step(t_tx, impulse_modulated, where='post')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Pulsos')
plt.grid(True)
plt.show()