
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from rcosdesign import rcosdesign
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from RS import encode, decode
import funciones as fn



def modem(Ns, L, Ts, rolloff, ISI, ruido, codificacion, iter,total_errores, ecualizador,modulation):


    
    #se generan las figuras 

    # Activa el modo interactivo de Matplotlib
    plt.ion()

    # Crea las figuras una vez para que se mantengan abiertas
    plt.figure(1)
    plt.figure(2)


    # Inicializa los gráficos con valores vacíos
    plt.figure(1).clear()
    plt.figure(2).clear()
 

    
    
   
    # 1. Generacion de onda del pulso
    pt = rcosdesign(rolloff, 6, L, 'sqrt')
    pt = pt / (np.max(np.abs(pt)))  # rescaling to match rcosine


    data_bit = (np.random.rand(Ns) > 0.5).astype(int)


    #Codifica con o sin RS
    if codificacion:
        encoded_data = np.array(encode(data_bit))
    else        :
        encoded_data = data_bit
    Ns_code = len(encoded_data)

    #Ts = Ts*Ns/Ns_code
    t_step = Ts / L


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


                   

    # Convolucionar la señal con el pulso
    tx_signal_full = ss.convolve(impulse_modulated, pt, mode='full')
    diff_len = len(tx_signal_full) - len(impulse_modulated)
    start = diff_len // 2
    end = start + len(impulse_modulated)
    tx_signal = tx_signal_full[start:end]

    




    

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

    #----------------------------------------------------------#
    #----------------------Receptor----------------------------#
    #----------------------------------------------------------#


    #--------------------Filtro Acoplado---------------#
    #Filtro acoplado tiene la misma forma que pt debido a su simetria
    filtro_acoplado_full = ss.convolve(rx_signal, pt, mode='full')
    diff_len = len(filtro_acoplado_full) - len(rx_signal)
    start = diff_len // 2
    end = start + len(rx_signal)
    filtro_acoplado = filtro_acoplado_full[start:end]

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
      

    #---------------Decodificacion------------------#

    if ecualizador:
        signal_to_decode = equalized_signal_shifted
    else:
        signal_to_decode = filtro_acoplado



    #deteccion de los bits
    match modulation:
        case "nrz_p":
            bits_rx, valores, t_muestreo = fn.detector_umbral(signal_to_decode, 0, L)
        case "rz_p":
            bits_rx, valores, t_muestreo = fn.detector_umbral(signal_to_decode, 0, L)
        case "nrz_u":
            bits_rx, valores, t_muestreo = fn.detector_umbral(signal_to_decode, 0.48, L)


    #-----------------grafico del muestreo------------------#
    # Genera una señal de tiempo que tenga la misma longitud que valores
    t_muestreo = np.arange(len(valores)) + tiempo_actual

    fig2 = plt.figure(2)
    fig2.set_size_inches(12, 7)
    fig2.subplots_adjust(hspace=0.3, wspace=0.3)  # Ajusta el espacio entre los subplots
    plt.subplot(2, 2, 1)
    plt.stem(t_muestreo, valores, use_line_collection=True)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Muestreo de señal recibida')
    plt.ylim(-2, 2)
    plt.grid(True)


    #grafica el diagrama de ojo------------------------------------------
    signal_len = len(filtro_acoplado)
    num_bits = signal_len // (L*2)  # Ajustado para dos símbolos
    eye_width = L*2

    eye_diagram = np.zeros((num_bits, eye_width))

    for i in range(num_bits):
        start = i * eye_width
        end = start + eye_width
        eye_diagram[i] = filtro_acoplado[start:end]

    # Graficar el diagrama de ojo

    plt.subplot(2, 2, 2)
    plt.title('Diagrama de Ojo')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.grid(True)

    for i in range(eye_diagram.shape[0]):
        plt.plot(eye_diagram[i], label=f'Bit {i}')
    #--------------------------------------------------------------
    #--------------------------------------------------------------



    errores_RS = []
    simbolo_error = False
    if codificacion:    
        decoded_data, errores_RS, simbolo_error = np.array(decode(bits_rx, Ns))
    else:
        decoded_data = bits_rx

    pos_errores, bits_con_error = fn.contar_diferencias(data_bit, decoded_data)



    print("Bits originales:", data_bit)
    print("Bits decoficados:", np.array(decoded_data))
    print("Número de errores:", bits_con_error)
    print("Posiciones de los errores:", pos_errores)
    total_errores += bits_con_error
    






    #---------------Potencia de señales----------------#
    
    pot_or=round(np.mean(np.square(encoded_data)),3) #potencia pulsos originales
    pot_cod=round(np.mean(np.square(amp_modulated)),3) #potencia señal codificada
    pot_pulsos=round(np.mean(np.square(impulse_modulated)),3) #potencia pulsos transmitidos
    # Señal modulada continua
    t_continuo = np.linspace(0, Ns_code * Ts, Ns_code * L, endpoint=False)  # Tiempo continuo

    # Calcular la potencia de la señal continua
    potencia_tx_continua = round(np.trapz(tx_signal**2, t_continuo) / (Ns_code * Ts),3) #transmitida
    potencia_rx_continua = round(np.trapz(rx_signal**2, t_continuo) / (Ns_code * Ts),3) #recibida
    potencia_acoplado_continua = round(np.trapz(filtro_acoplado**2, t_continuo) / (Ns_code * Ts),3) #potencia filtro acoplado
    potencia_to_decode = round(np.trapz(signal_to_decode**2, t_continuo) / (Ns_code * Ts),3) #potencia signal to decode

    print("\n--------------Potencia de señales-------------\n")
    print("Potencia pulsos originales: ",pot_or,"Vrms")
    print("Potencia señal codificada: ",pot_cod,"Vrms")
    print("Potencia pulsos transmitidos: ",pot_pulsos,"Vrms")
    print("Potencia de la señal continua transmitida:", potencia_tx_continua,"Vrms")
    print("Potencia de la señal con ISI y ruido:", potencia_rx_continua,"Vrms")
    print("Potencia de la señal filtrada:", potencia_acoplado_continua,"Vrms")

    #Grafica la señal que fue decodificada
    t_rx = np.arange(0, len(signal_to_decode)) * t_step + tiempo_actual
    plt.subplot(2, 2, 3)
    plt.plot(t_rx, signal_to_decode)
    plt.text(0.1, 0.01, f'Potencia señal filtrada: {potencia_to_decode} W', transform=plt.figure(2).transFigure, fontsize=10)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Señal Filtrada')
    plt.grid(True)
    plt.text(0.5, 0.4, f'Bits transmitidos: {Ns+iter*Ns}', transform=plt.figure(2).transFigure, fontsize=12)
    plt.text(0.5, 0.35, f'Total de errores (enviado vs recibido): {total_errores}', transform=plt.figure(2).transFigure, fontsize=12)
    plt.ylim(-2, 2)


#GRAFICAS--------------------------------------------------------------------------------------------------
 # Graficar la señal
    fig = plt.figure(1)
    fig.set_size_inches(12, 6)
    fig.subplots_adjust(hspace=0.37, wspace=0.37)  # Ajusta el espacio entre los subplots
    plt.subplot(2, 2, 1)
    plt.plot(t_p, encoded_data, drawstyle='steps-post', label='Señal original')
    plt.text(0.1, 0.93, f'Potencia señal original: {pot_or} W', transform=plt.figure(1).transFigure, fontsize=10)
    plt.plot(t_p2, amp_modulated, drawstyle='steps-post', label='Señal modulada')
    plt.text(0.58, 0.93, f'Potencia señal codificada: {pot_cod} W', transform=plt.figure(1).transFigure, fontsize=10)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Señal modulada')
    plt.legend()
    plt.grid()

    # Grafica los pulsos
    t_tx = np.arange(0, len(impulse_modulated)) * t_step + tiempo_actual
    #plt.figure(2)
    plt.subplot(2, 2, 2)
    plt.plot(t_tx, impulse_modulated)
    
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Pulsos')
    plt.grid(True)

    # Grafica la señal transmitida

    
    t_tx = np.arange(0, len(tx_signal)) * t_step + tiempo_actual
    #plt.figure(3)
    plt.subplot(2, 2, 3)
    plt.plot(t_tx, tx_signal)
    plt.text(0.1, 0.01, f'Potencia señal transmitida: {potencia_tx_continua} W', transform=plt.figure(1).transFigure, fontsize=10)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Señal Transmitida')
    plt.grid(True)

    # Graficar la señal con ISI y ruido
    t_rx = np.arange(0, len(rx_signal)) * t_step + tiempo_actual
    #plt.figure(4)
    plt.subplot(2, 2, 4)
    plt.plot(t_rx, rx_signal)
    plt.text(0.58, 0.01, f'Potencia señal recibida: {potencia_rx_continua} W', transform=plt.figure(1).transFigure, fontsize=10)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Señal con ISI y ruido')
    plt.grid(True)

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