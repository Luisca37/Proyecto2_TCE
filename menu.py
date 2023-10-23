import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from Proyecto2_codificacion import modem

# Función que se ejecutará en un hilo separado para ejecutar el código

np.random.seed(324)

def start_execution():
    # Obtener los valores de los widgets de la interfaz gráfica
    Ns = int(Ns_entry.get())
    Ts = float(Ts_entry.get())
    hamming_code = hamming_code_var.get()
    roll_off = float(roll_off_entry.get())
    L = int(L_entry.get())
    bloques = int(bloques_entry.get())

    # Ejecutar el programa con los parámetros seleccionados
    total_errores = 0
    for i in range(bloques):
        total_errores = modem(Ns, L, Ts, roll_off, hamming_code, i, total_errores)
        plt.pause(0.5)
        print('total errores: ',total_errores)

    # Mostrar los gráficos
    plt.show()

# Crear la ventana principal
window = tk.Tk()

# Crear los widgets para configurar los parámetros del programa
Ns_label = tk.Label(window, text="Ns:")
Ns_label.pack()
Ns_entry = tk.Entry(window)
Ns_entry.pack()

Ts_label = tk.Label(window, text="Ts:")
Ts_label.pack()
Ts_entry = tk.Entry(window)
Ts_entry.pack()

hamming_code_var = tk.BooleanVar()
hamming_code_checkbutton = tk.Checkbutton(window, text="Usar código de Hamming", variable=hamming_code_var)
hamming_code_checkbutton.pack()

roll_off_label = tk.Label(window, text="Roll-off:")
roll_off_label.pack()
roll_off_entry = tk.Entry(window)
roll_off_entry.pack()

L_label = tk.Label(window, text="L:")
L_label.pack()
L_entry = tk.Entry(window)
L_entry.pack()

bloques_label = tk.Label(window, text="Bloques:")
bloques_label.pack()
bloques_entry = tk.Entry(window)
bloques_entry.pack()

# Crear el botón "Ejecutar"
run_button = tk.Button(window, text="Ejecutar", command=start_execution)
run_button.pack()

# Ejecutar el bucle principal de la ventana
window.mainloop()