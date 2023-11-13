
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from rcosdesign import rcosdesign
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from RS import encode, decode
import funciones as fn





def modem(Ns, L, Ts, rolloff, ISI, ruido, codificacion, iter,total_errores, ecualizador,modulation):


    pam4 = False
    
    #se generan las figuras 

    # Activa el modo interactivo de Matplotlib
    plt.ion()

    # Crea las figuras una vez para que se mantengan abiertas
    plt.figure(1)
    plt.figure(2)
    plt.figure(3)
    plt.figure(4)
    plt.figure(5)
    plt.figure(6)
    plt.figure(7)

    # Inicializa los gráficos con valores vacíos
    plt.figure(1).clear()
    plt.figure(2).clear()
    plt.figure(3).clear()
    plt.figure(4).clear()
    plt.figure(5).clear()
    plt.figure(6).clear()
    plt.figure(7).clear()

    

    t_step = Ts / L
    
   
    # 1. Generacion de onda del pulso
    print("Rolloff:", rolloff)
    pt = rcosdesign(rolloff, 6, L, 'sqrt')
    pt = pt / (np.max(np.abs(pt)))  # rescaling to match rcosine


    data_bit = (np.random.rand(Ns) > 0.5).astype(int)


    #Codifica con o sin RS
    if codificacion:
        encoded_data = np.array(encode(data_bit))
    else        :
        encoded_data = data_bit
    Ns_code = len(encoded_data)

    


    match modulation:
        case "nrz_p":
            amp_modulated = 2*encoded_data - 1 # 0=> -1,  1=>1
            Ns_code = len(amp_modulated)
        case "rz_p":
            amp_modulated = fn.rz_polar_encoding(encoded_data)
            Ns_code = int(len(amp_modulated)/2)
        case "nrz_u":
            amp_modulated = encoded_data
            Ns_code = len(amp_modulated)





    #se calcula el tiempo actual de simulacion
    tiempo_actual = Ts*Ns_code*iter


    if modulation == "rz_p":
        t_p = np.arange(0, len(encoded_data)) + tiempo_actual
        t_p2=(np.arange(0,len(amp_modulated))/2)+tiempo_actual
    else:
        t_p = np.arange(0, len(encoded_data)) + tiempo_actual
        t_p2=t_p

    # Graficar la señal
    plt.figure(1)
    plt.plot(t_p, encoded_data, drawstyle='steps-post', label='Señal original')
    plt.plot(t_p2, amp_modulated, drawstyle='steps-post', label='NRZ Polar')
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Codificación NRZ Polar')
    plt.legend()
    plt.grid()
    



    # 4. Modulacion de pulsos
    impulse_modulated = np.zeros(Ns_code * L)



    if modulation == "rz_p":
         i = 0
         for n in range(Ns_code):
 
            delta_signal = np.concatenate(([amp_modulated[i]], np.zeros(L - 1)))
            impulse_modulated[n * L: (n * L) + L] = delta_signal
            #impulse_modulated[n * L: (n + 1) * L] = delta_signal
            i += 2      
    else: 
        for n in range(Ns_code):
            delta_signal = np.concatenate(([amp_modulated[n]], np.zeros(L - 1)))
            impulse_modulated[n * L: (n * L) + L] = delta_signal
            #impulse_modulated[n * L: (n + 1) * L] = delta_signal


                   


    tx_signal = ss.convolve(impulse_modulated, pt, mode='same')

    # Grafica los pulsos
    t_tx = np.arange(0, len(impulse_modulated)) * t_step + tiempo_actual
    plt.figure(2)
    plt.plot(t_tx, impulse_modulated)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Pulsos')
    plt.grid(True)




    # Grafica la señal transmitida
    t_tx = np.arange(0, len(tx_signal)) * t_step + tiempo_actual
    plt.figure(3)
    plt.plot(t_tx, tx_signal)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Señal Transmitida')
    plt.grid(True)


    #----------------------------------------------------------#
    #-----------------------Canal------------------------------#
    #----------------------------------------------------------#


    #Generar numeros aleatorios con distribucion normal para simuar el ruido
    factor_ruido = ruido
    length_tx_signal=len(tx_signal)
    randn_array=factor_ruido*np.random.randn(1,length_tx_signal)


    #se agrega isi y ruido a la señal
    isi_factor = ISI # Valor mayor para un ISI más pronunciado
    isi_length = int(L * isi_factor)
    isi_filter = np.ones(isi_length) / isi_length

    rx_signal = ss.convolve(tx_signal, isi_filter, mode='same')+randn_array[0]



    # Graficar la señal con ISI y ruido
    t_rx = np.arange(0, len(rx_signal)) * t_step + tiempo_actual
    plt.figure(4)
    plt.plot(t_rx, rx_signal)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Señal con ISI y ruido')
    plt.grid(True)

    #----------------------------------------------------------#
    #----------------------Receptor----------------------------#
    #----------------------------------------------------------#


    #--------------------Filtro Acoplado---------------#
    #Filtro acoplado tiene la misma forma que pt debido a su simetria
    filtro_acoplado = ss.convolve(rx_signal , pt, mode = 'same' )

    if modulation == "nrz_u":
        filtro_acoplado /= np.sum(np.abs(pt))*0.8
    else:
        filtro_acoplado /= np.sum(np.abs(pt)) #normalizacion


    


    #---------------Ecualizador----------------------------#
    mu = 0.225 # Tasa de aprendizaje del filtro LMS
    n_taps = 16  # Número de coeficientes del filtro LMS
    eq = np.zeros(n_taps)
    input_signal = np.copy(filtro_acoplado)
    equalized_signal = []

    for i in range(len(filtro_acoplado)):
        if i >= n_taps:
            # Tomar una porción de la señal de entrada para calcular el error
            input_segment = input_signal[i:i-n_taps:-1]
            error = tx_signal[i] - np.dot(eq, input_segment)
            eq += mu * error * input_segment
            equalized_signal.append(np.dot(eq, input_segment))

    # Convertir la lista a un array NumPy
    equalized_signal = np.array(equalized_signal)
    time_shift = 10  # Número de muestras para adelantar (valor positivo) o retrasar (valor negativo)

    # Crear una nueva señal ecualizada desplazada en el tiempo
    equalized_signal_shifted = np.roll(equalized_signal, time_shift)
    #el plot de esta señal se imprime despues de calcualr el total de errores

    for i in range(len(equalized_signal), len(filtro_acoplado)):
        equalized_signal_shifted = np.append(equalized_signal_shifted, 0)
    
    '''
    t_rx = np.arange(0, len(equalized_signal_shifted)) * t_step + tiempo_actual
    plt.figure(10)
    plt.plot(t_rx, equalized_signal_shifted)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Señal Ecualizada')
    plt.grid(True)'''    

    #---------------Decodificacion------------------#

    if ecualizador:
        signal_to_decode = equalized_signal_shifted
    else:
        signal_to_decode = filtro_acoplado



    t_rx = np.arange(0, len(signal_to_decode)) * t_step + tiempo_actual
    plt.figure(5)
    plt.plot(t_rx, signal_to_decode)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Señal Filtrada')
    plt.grid(True)
        #Grafica la señal que fue decodificada

    #deteccion de los bits
    match modulation:
        case "nrz_p":
            bits_rx, valores, t_muestreo = fn.detector_umbral(signal_to_decode, 0, L)
        case "rz_p":
            bits_rx, valores, t_muestre = fn.detector_umbral(signal_to_decode, 0, L)
        case "nrz_u":
            bits_rx, valores, t_muestreo = fn.detector_umbral(signal_to_decode, 0.48, L)

    print(t_muestreo)
    #-----------------grafico del muestreo------------------#
    plt.figure(6)
    plt.stem(t_muestreo, valores, use_line_collection=True)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')


    #grafica el diagrama de ojo------------------------------------------
    signal_len = len(signal_to_decode)
    num_bits = signal_len // L
    eye_width = L

    eye_diagram = np.zeros((num_bits, eye_width))

    for i in range(num_bits):
        start = i * L
        end = start + eye_width
        eye_diagram[i] = signal_to_decode[start:end]

    # Graficar el diagrama de ojo
    
    plt.figure(7)
    plt.title('Diagrama de Ojo')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.grid(True)

    for i in range(eye_diagram.shape[0]):
        plt.plot(eye_diagram[i], label=f'Bit {i}')
    #--------------------------------------------------------------




    #se realiza la decodificacion con RS de ser necesario
    print("Bits transmitidos:", encoded_data)
    print("Bits detectados:", np.array(bits_rx))
    print("Número de errores en dato codificado:", fn.contar_diferencias(encoded_data, bits_rx)[1])
    print("Posiciones de los en dato codificado:", fn.contar_diferencias(encoded_data, bits_rx)[0])

    errores_RS = []
    simbolo_error = False
    if codificacion:    
        decoded_data, errores_RS, simbolo_error = np.array(decode(bits_rx, Ns))
    else:
        decoded_data = bits_rx
    print(errores_RS)

    pos_errores, bits_con_error = fn.contar_diferencias(data_bit, decoded_data)



    print("Bits originales:", data_bit)
    print("Bits decoficados:", np.array(decoded_data))
    print("Número de errores:", bits_con_error)
    print("Posiciones de los errores:", pos_errores)
    total_errores += bits_con_error
    


    #Grafica la señal que fue decodificada
    print('iteracion: ',iter)
    print('tiempo actual: ',tiempo_actual)
    t_rx = np.arange(0, len(signal_to_decode)) * t_step + tiempo_actual
    plt.figure(5)
    plt.plot(t_rx, signal_to_decode)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Señal Filtrada')
    plt.grid(True)
    plt.text(0.1, 0.9, f'Total Errores: {total_errores}', transform=plt.figure(5).transFigure, fontsize=12)
    plt.text(0.6, 0.005, f'Bits transmitidos: {Ns+iter*Ns}', transform=plt.figure(5).transFigure, fontsize=12)
    plt.ylim(-2, 2)




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

    return total_errores, errores_RS, simbolo_error

"""
#-----------Menu-------------------#
np.random.seed(324)

tiempo_actual = 0
Ns = 64
Ts = 1
codificacion = True
bloques = 16
roll_off = 0.75
ecualizador = True

L=16
total_errores = 0
errores_bloque = 0

iter = 0

for i in range(bloques):
    #se ejecuta la modulacion demodulacion para un bloque de Ns bits y se acumulan los errores
    total_errores = modem(Ns, L, Ts, roll_off, codificacion, iter, total_errores, ecualizador) 
    display.display(plt.gcf())  # Muestra la figura actual
    plt.pause(0.5)  # Pausa durante 1 segundo para permitir la actualización
    print('total errores: ',total_errores)
    iter += 1
plt.show()
input("Presiona Enter para finalizar")
"""