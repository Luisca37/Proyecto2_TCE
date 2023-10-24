import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from Proyecto2_codificacion import modem

# Función que se ejecutará en un hilo separado para ejecutar el código



def start_execution():
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
    for i in range(bloques):
        total_errores = modem(Ns, L, Ts, roll_off, code, i, total_errores, ecualizador)
        plt.pause(0.5)
        print('total errores: ',total_errores)

    # Mostrar los gráficos
    plt.show()

# Crear la ventana principal
window = tk.Tk()

# Crear los widgets para configurar los parámetros del programa
Ns_label = tk.Label(window, text="Numero de bits por bloque(multiplo de 4):")
Ns_label.pack()
Ns_entry = tk.Entry(window)
Ns_entry.pack()
Ns_entry.insert(0, "8")

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

# Crear el botón "Ejecutar"
run_button = tk.Button(window, text="Ejecutar simulacion", command=start_execution)
run_button.pack()

# Ejecutar el bucle principal de la ventana
window.mainloop()