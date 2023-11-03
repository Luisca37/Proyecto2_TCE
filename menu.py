import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from Proyecto2_codificacion import modem


def create_label_entry(parent, label_text, default_value):
    label = tk.Label(parent, text=label_text)
    label.pack()
    entry = tk.Entry(parent)
    entry.pack()
    entry.insert(0, default_value)
    return entry

def create_checkbutton(parent, text, var):
    checkbutton = tk.Checkbutton(parent, text=text, variable=var)
    checkbutton.pack()

def create_slider(parent, label_text, default_value, from_value , to_value):
    slider_value = tk.DoubleVar()
    slider = tk.Scale(parent, from_=from_value, to=to_value, orient='horizontal', variable=slider_value, resolution=0.001)
    entry = tk.Entry(parent, textvariable=slider_value)
    label = tk.Label(parent, text=label_text)

    label.pack()
    slider.pack()
    entry.pack()
    slider.set(default_value)  # Set default value for the slider
    return slider, slider_value

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
    isi = slider_value1.get()
    ruido = slider_value2.get()
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
        total_errores, error_RS, error_simbolo = modem(Ns, L, Ts, roll_off, isi, ruido, code, i, total_errores, ecualizador)
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
# Crear la ventana principal
window = tk.Tk()
window.title("Simulación de Modem")  # Añade un título a la ventana

# Crear los widgets para configurar los parámetros del programa
Ns_entry = create_label_entry(window, "Numero de bits por bloque(multiplo de 8):", "64")
Ts_entry = create_label_entry(window, "Tiempo de bit:", "1")
code_var = tk.BooleanVar()
code_checkbutton = create_checkbutton(window, "Usar Reed Solomon", code_var)
ecualizador_var = tk.BooleanVar()
ecualizador_checkbutton = create_checkbutton(window, "Usar Ecualizador", ecualizador_var)
roll_off_entry = create_label_entry(window, "Roll-off del coseno alzado:", "0.75")
L_entry = create_label_entry(window, "L:", "16")
bloques_entry = create_label_entry(window, "Numero de bloques a transmitir:", "8")

# Crear sliders
slider1, slider_value1 = create_slider(window, "ISI:", 1.8, 1, 5)
slider2, slider_value2 = create_slider(window, "Factor de Ruido:", 0.5, 0.01, 10)

# Ajustar el tamaño de la ventana y definir la fuente
window.geometry('800x800')
font = ('Arial', 12)

# Crear el botón "Ejecutar"
run_button = tk.Button(window, text="Ejecutar simulacion", command=start_execution)
run_button.pack()

# Crear un widget de texto para mostrar la salida de la terminal
output_text = tk.Text(window, wrap='word', height=20, font=font)  # Ajusta la fuente
output_text.pack(fill='both', expand=True)

# Redirigir la salida estándar al widget de texto
sys.stdout = TextRedirector(output_text)

# Ejecutar el bucle principal de la ventana
window.mainloop()