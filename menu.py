import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from Proyecto2_codificacion import modem

class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)


# Función que se ejecutará en un hilo separado para ejecutar el código

def start_execution():
    output_text.delete('1.0', tk.END)

    np.random.seed(324)
    # Obtener los valores de los widgets de la interfaz gráfica
    Ns = int(Ns_entry.get())
    Ts = float(Ts_entry.get())
    code = code_var.get()
    ecualizador = ecualizador_var.get()
    roll_off = float(roll_off_entry.get())
    L = int(L_entry.get())
    bloques = int(bloques_entry.get())

    # Ejecutar el programa con los parámetros seleccionados
    total_errores = 0
    errores_RS = {}
    errores_simbolo = {}
    for i in range(bloques):
        os.system('cls')
        total_errores, error_RS, error_simbolo = modem(Ns, L, Ts, roll_off, code, i, total_errores, ecualizador)
        plt.pause(0.5)
        print('total errores: ',total_errores)
        errores_RS[i] = error_RS
        errores_simbolo[i] = error_simbolo
    
    #conteo errores detectados y corregidos por RS
    total_errores_RS = 0
    for lista in errores_RS.values():
         total_errores_RS += len(lista)
    #conteo simbolos con errores que no se lograron corregir
    simb_con_error = [key for key, value in errores_simbolo.items() if value is True]

    print('Algoritmo Reed Solomon fue capaz de detectar y corregir :\n',total_errores_RS, 'errores')
    print('lista de paquetes con errores que no lograron ser corregidos:\n',simb_con_error)

    # Mostrar los gráficos
    plt.show()

# Crear la ventana principal
window = tk.Tk()

# Crear los widgets para configurar los parámetros del programa
Ns_label = tk.Label(window, text="Numero de bits por bloque(multiplo de 8):")
Ns_label.pack()
Ns_entry = tk.Entry(window)
Ns_entry.pack()
Ns_entry.insert(0, "64")

Ts_label = tk.Label(window, text="Tiempo de bit:")
Ts_label.pack()
Ts_entry = tk.Entry(window)
Ts_entry.pack()
Ts_entry.insert(0, "1")


code_var = tk.BooleanVar()
code_checkbutton = tk.Checkbutton(window, text="Usar Reed Solomon", variable=code_var)
code_checkbutton.pack()

ecualizador_var = tk.BooleanVar()
ecualizador_checkbutton = tk.Checkbutton(window, text="Usar Ecualizador", variable=ecualizador_var)
ecualizador_checkbutton.pack()

roll_off_label = tk.Label(window, text="Roll-off del coseno alzado:")
roll_off_label.pack()
roll_off_entry = tk.Entry(window)
roll_off_entry.pack()
roll_off_entry.insert(0, "0.75")

L_label = tk.Label(window, text="L:")
L_label.pack()
L_entry = tk.Entry(window)
L_entry.pack()
L_entry.insert(0, "16")

bloques_label = tk.Label(window, text="Numero de bloques a transmitir:")
bloques_label.pack()
bloques_entry = tk.Entry(window)
bloques_entry.pack()
bloques_entry.insert(0, "8")


# Ajustar el tamaño de la ventana
window.geometry('800x600')  # Cambia esto a las dimensiones que desees

# Definir la fuente para los widgets
font = ('Helvetica', 12)  # Cambia esto a la fuente y tamaño que desees

# Crear el botón "Ejecutar"
run_button = tk.Button(window, text="Ejecutar simulacion", command=start_execution)
run_button.pack()


# Crear un widget de texto para mostrar la salida de la terminal
output_text = tk.Text(window, wrap='word', height=20)  # Ajusta la altura según tus necesidades
output_text.pack(fill='both', expand=True)  # Hacer que el widget de texto se expanda para llenar la ventana

# Redirigir la salida estándar al widget de texto
sys.stdout = TextRedirector(output_text)

# Ejecutar el bucle principal de la ventana
window.mainloop()