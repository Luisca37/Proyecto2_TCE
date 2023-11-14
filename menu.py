import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from Proyecto2_codificacion import modem
from PIL import Image, ImageTk

def create_label_entry(parent, text, default_value, label_width, entry_width):
    # Crear el Label con texto en negrita, ancho fijo y alineado a la izquierda
    label = tk.Label(parent, text=text, font=("Helvetica", 10, "bold"), width=label_width, anchor='w')
    label.pack(side=tk.LEFT)

    # Crear la Entry con ancho fijo
    entry_value = tk.StringVar(value=default_value)
    entry = tk.Entry(parent, textvariable=entry_value, width=entry_width)
    entry.pack(side=tk.LEFT)

    return entry, entry_value

def create_checkbutton(parent, text, variable):
    checkbutton = tk.Checkbutton(parent, text=text, variable=variable)
    return checkbutton  # Devolver el Checkbutton sin organizarlo


def create_slider_entry(parent, text, initial_value, from_, to):
    # Crear el Label y el Slider
    label = tk.Label(parent, text=text)
    slider_value = tk.DoubleVar(value=initial_value)
    slider = tk.Scale(parent, from_=from_, to=to, orient=tk.HORIZONTAL, variable=slider_value, resolution=0.01)

    # Crear la Entry vinculada al mismo DoubleVar que el Slider
    entry = tk.Entry(parent, textvariable=slider_value, width=10)

    return slider, label, slider_value, entry  # Devolver el Slider, el Label, el DoubleVar y la Entry

def create_slider(parent, text, initial_value, from_, to):
    # Crear el Label y el Slider
    label = tk.Label(parent, text=text)
    slider_value = tk.DoubleVar(value=initial_value)
    slider = tk.Scale(parent, from_=from_, to=to, orient=tk.HORIZONTAL, variable=slider_value, resolution=0.01)

    return slider, label, slider_value  # Devolver el Slider, el Label y el DoubleVar

class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)


# Función que se ejecutará en un hilo separado para ejecutar el código

def start_execution():
    global slider_value1, slider_value2
    output_text.delete('1.0', tk.END)

    

    np.random.seed(324)
    # Obtener los valores de los widgets de la interfaz gráfica
    Ns = int(Ns_entry.get())
    if Ns % 8 != 0:
        error_msg = "Error: Número de bits por bloque debe ser un múltiplo de 8.\n"
        output_text.insert(tk.END, error_msg, "error")  # Agrega el tag "error" al mensaje de error
        return
    
    Ts = float(Ts_entry.get())
    isi = slider_value1.get()
    ruido = slider_value2.get()
    code = code_var.get()
    ecualizador = ecualizador_var.get()
    roll_off = float(roll_off_entry.get())
    L = int(L_entry.get())
    bloques = int(bloques_entry.get())
    modulation = modulation_var.get()

    # Ejecutar el programa con los parámetros seleccionados
    total_errores = 0
    errores_RS = {}
    errores_simbolo = {}

    print('Iniciando simulacion...')
    for i in range(bloques):
        print('#------------------------------------------------#\n')
        print('Bloque: ',i)
        os.system('cls')
        total_errores, error_RS, error_simbolo = modem(Ns, L, Ts, roll_off, isi, ruido, code, i, total_errores, ecualizador, modulation)
        plt.pause(0.5)
        print('total errores: ',total_errores)
        errores_RS[i] = error_RS
        errores_simbolo[i] = error_simbolo
    
    print('Simulacion terminada')
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

# Cargar la imagen de fondo
'''
background_image = Image.open("fondo.jpg")
background_image = background_image.resize((800, 800), Image.ANTIALIAS)  # Ajusta el tamaño de la imagen al tamaño de la ventana
background_photo = ImageTk.PhotoImage(background_image)

# Crear un Label para mostrar la imagen de fondo
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Asegura que la imagen de fondo cubra toda la ventana
'''

code_var = tk.BooleanVar()
ecualizador_var = tk.BooleanVar()
modulation_var = tk.StringVar()
modulation_var.set("nrz_p")

# Crear un Frame y un widget de entrada para cada parámetro
Ns_frame = tk.Frame(window)
Ns_frame.pack(pady=5)
Ns_entry, Ns_value = create_label_entry(Ns_frame, "Numero de bits por bloque(multiplo de 8):", "64", 33, 10)

bloques_frame = tk.Frame(window)
bloques_frame.pack(pady=5)
bloques_entry, bloques_value = create_label_entry(bloques_frame, "Numero de bloques a transmitir:", "8", 33, 10)

Ts_frame = tk.Frame(window)
Ts_frame.pack(pady=5)
Ts_entry, Ts_value = create_label_entry(Ts_frame, "Tiempo de bit:", "1", 33, 10)

roll_off_frame = tk.Frame(window)
roll_off_frame.pack(pady=5)
roll_off_entry, roll_off_value = create_label_entry(roll_off_frame, "Roll-off del coseno alzado:", "0.75", 33, 10)

L_frame = tk.Frame(window)
L_frame.pack(pady=5)
L_entry, L_value = create_label_entry(L_frame, "Numero de muestras por simbolo:", "16", 33, 10)



#----botones de seleccion de modulacion-----------------
# Crear un Frame para contener los Radiobuttons
modulation_frame = tk.Frame(window)
modulation_frame.pack(pady=5)

# Crear un Label para el título
title_label = tk.Label(modulation_frame, text="Selecciona la modulación:", font=("Helvetica", 10, "bold"))
title_label.grid(row=0, column=0, columnspan=3)  # Colocar el Label en la parte superior del Frame

# Crear los Radiobuttons
nrz_polar_radiobutton = tk.Radiobutton(modulation_frame, text="NRZ Polar", variable=modulation_var, value="nrz_p")
nrz_unipolar_radiobutton = tk.Radiobutton(modulation_frame, text="NRZ Unipolar", variable=modulation_var, value="nrz_u")
rz_polar_radiobutton = tk.Radiobutton(modulation_frame, text="RZ Polar", variable=modulation_var, value="rz_p")

# Organizar los Radiobuttons en el Frame
nrz_polar_radiobutton.grid(row=1, column=0)  # Cambiar row a 1
nrz_unipolar_radiobutton.grid(row=1, column=1)  # Cambiar row a 1
rz_polar_radiobutton.grid(row=1, column=2)  # Cambiar row a 1

#----------RS y Ecualizador----------------
# Crear un Frame para contener los Checkbuttons
options_frame = tk.Frame(window)
options_frame.pack(pady=5)

# Crear un Label para el título
options_title_label = tk.Label(options_frame, text="Selecciona las opciones:", font=("Helvetica", 10, "bold"))
options_title_label.grid(row=0, column=0, columnspan=2)  # Colocar el Label en la parte superior del Frame

# Crear los Checkbuttons
code_checkbutton = create_checkbutton(options_frame, "Usar Reed Solomon", code_var)
ecualizador_checkbutton = create_checkbutton(options_frame, "Usar ecualizador adaptativo", ecualizador_var)

# Organizar los Checkbuttons en el Frame
code_checkbutton.grid(row=1, column=0)  # Cambiar row a 1
ecualizador_checkbutton.grid(row=1, column=1)  # Cambiar row a 1


#--------Crear sliders--------------------------
# Crear un Frame para contener los Sliders
sliders_frame = tk.Frame(window)
sliders_frame.pack(pady=5)  # Agregar un relleno vertical de 10 píxeles

# Crear un Label para el título
sliders_title_label = tk.Label(sliders_frame, text="Propiedades del canal:", font=("Helvetica", 10, "bold"))
sliders_title_label.grid(row=0, column=0, columnspan=2)  # Colocar el Label en la parte superior del Frame

# Crear los Sliders y las Entries
slider1, label1, slider_value1, entry1 = create_slider_entry(sliders_frame, "ISI:", 1.8, 0.1, 5)
slider2, label2, slider_value2, entry2 = create_slider_entry(sliders_frame, "Factor de Ruido:", 0.5, 0.01, 2)

# Organizar los Labels, los Sliders y las Entries en el Frame
label1.grid(row=1, column=0)  # Cambiar row a 1
slider1.grid(row=2, column=0)  # Cambiar row a 2
entry1.grid(row=3, column=0)  # Añadir la Entry debajo del Slider
label2.grid(row=1, column=1)  # Cambiar row a 1
slider2.grid(row=2, column=1)  # Cambiar row a 2
entry2.grid(row=3, column=1)  # Añadir la Entry debajo del Slider
#---------------------------------------------
# Ajustar el tamaño de la ventana y definir la fuente
window.geometry('800x800')
font = ('Arial', 12)

# Crear el botón "Ejecutar"
run_button = tk.Button(window, text="Ejecutar simulacion", command=start_execution, font=("Helvetica", 10, "bold"))
run_button.pack()

# Crear un widget de texto para mostrar la salida de la terminal
output_text = scrolledtext.ScrolledText(window, wrap='word', height=20, font=font)
output_text.pack(fill='both', expand=True)

# Agregar un tag "error" con formato rojo
output_text.tag_configure("error", foreground="red")
output_text.tag_configure("normal", foreground="black")

# Redirigir la salida estándar al widget de texto
sys.stdout = TextRedirector(output_text)

# Ejecutar el bucle principal de la ventana
window.mainloop()