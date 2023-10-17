import numpy as np

def encode_hamming(data_bits):
    # Determine the number of parity bits required
    m = len(data_bits)
    r = 0
    while 2**r < m + r + 1:
        r += 1

    # Create an array for the encoded data
    encoded_data = [0] * (m + r)
    j = 0

    # Fill in the positions of the parity bits
    for i in range(1, m + r + 1):
        if i == 2**j:
            j += 1
        else:
            encoded_data[i - 1] = data_bits.pop(0)

    j = 0

    # Calculate the parity bits
    for i in range(1, m + r + 1):
        if i == 2**j:
            j += 1
            encoded_data[i - 1] = calculate_parity_bit(encoded_data, i, m, r)

    return encoded_data

def calculate_parity_bit(data, position, data_bits, parity_bits):
    parity_bit = 0
    for i in range(1, data_bits + parity_bits + 1):
        if (i & position) == position:
            parity_bit ^= data[i - 1]
    return parity_bit

def decode_hamming(encoded_data):
    r = 0
    m = len(encoded_data)
    while 2**r < m:
        r += 1

    decoded_data = encoded_data.copy()
    error_position = 1

    for i in range(1, m + 1):
        if i & (i - 1) == 0:
            parity_bit = calculate_parity_bit(decoded_data, i, m - r, r)
            if parity_bit != decoded_data[i - 1]:
                error_position += i

    if error_position > 0:
        print("Error en la posición:", error_position)
        decoded_data[error_position - 1] ^= 1

    data_bits = []
    j = 0
    for i in range(1, m + 1):
        if i != 2**j:
            data_bits.append(decoded_data[i - 1])
        else:
            j += 1

    return data_bits

# Ejemplo de uso
data_bits = [1, 0, 1, 0]  # Datos de entrada

encoded_data = encode_hamming(data_bits)
print("Secuencia codificada:", encoded_data)

received_data = [1, 0, 1, 0, 1, 1, 0]  # Datos recibidos con posible error
decoded_data = decode_hamming(received_data)
print("Secuencia decodificada:", decoded_data)
