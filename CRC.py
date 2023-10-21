import random


def calculate_parity_bits(data):
    # Calcular la cantidad de bits de paridad necesarios
    m = len(data)
    r = 0
    while 2 ** r < m + r + 1:
        r += 1

    # Crear una lista con bits de paridad
    parity_bits = [0] * r

    # Calcular los bits de paridad
    for i in range(r):
        parity_position = 2 ** i
        for j in range(1, m + 1):
            if (j >> i) & 1:  # Verificar si el bit j tiene el i-ésimo bit activado
                parity_bits[i] ^= data[j - 1]

    return parity_bits


def encode_with_hamming(data):
    m = len(data)
    r = 0
    while 2 ** r < m + r + 1:
        r += 1

    # Inicializar la secuencia de bits codificada
    encoded_data = [0] * (m + r)
    j = 0

    # Insertar los bits de datos en la secuencia de bits codificada
    for i in range(m + r):
        if i + 1 == 2 ** j:
            j += 1
        else:
            encoded_data[i] = data.pop(0)

    # Calcular los bits de paridad y agregarlos
    parity_bits = calculate_parity_bits(encoded_data)
    for i in range(r):
        encoded_data[2 ** i - 1] = parity_bits[i]

    return encoded_data

def decode_with_hamming(data):
    r = 0
    while 2 ** r < len(data):
        r += 1

    # Calcular los bits de paridad y verificar si hay errores
    parity_bits = calculate_parity_bits(data)
    error_position = sum(2 ** i for i, bit in enumerate(parity_bits) if bit)

    error_count = 0

    if error_position:
        print(f"Error detectado en la posición {error_position}")
        data[error_position - 1] = 1 - data[error_position - 1]
        error_count += 1

    # Eliminar los bits de paridad
    decoded_data = [bit for i, bit in enumerate(data) if i + 1 not in (2 ** j for j in range(r))]

    return decoded_data, error_count