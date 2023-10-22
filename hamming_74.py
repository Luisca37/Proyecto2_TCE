def encode(data, num_parity_bits):
    # Asegurarse de que los datos de entrada tengan la longitud correcta
    if len(data) != (2**num_parity_bits - num_parity_bits):
        raise ValueError(f"Se requieren exactamente {2**num_parity_bits - num_parity_bits} bits de entrada para {num_parity_bits} bits de paridad")

    # Calcular los bits de paridad
    encoded_data = [0] * (len(data) + num_parity_bits)
    for i in range(num_parity_bits):
        parity_bit = 2**i  # Calcular la posición del bit de paridad
        for j in range(len(data)):
            if (j + 1) & parity_bit:  # Verificar si el bit en posición j afecta a este bit de paridad
                encoded_data[parity_bit - 1] ^= data[j]

    # Combinar datos y bits de paridad en un arreglo codificado
    encoded_data.extend(data)

    return encoded_data

def decode(encoded_data, num_parity_bits):
    # Asegurarse de que los datos de entrada tengan la longitud correcta
    if len(encoded_data) != (2**num_parity_bits):
        raise ValueError(f"Se requieren exactamente {2**num_parity_bits} bits de entrada para {num_parity_bits} bits de paridad")

    # Calcular los bits de paridad
    error_count = 0
    error_position = 0
    for i in range(num_parity_bits):
        parity_bit = 2**i  # Calcular la posición del bit de paridad
        calculated_parity = 0
        for j in range(len(encoded_data)):
            if (j + 1) & parity_bit:  # Verificar si el bit en posición j afecta a este bit de paridad
                calculated_parity ^= encoded_data[j]

        if calculated_parity != encoded_data[parity_bit - 1]:  # Comparar el bit de paridad calculado con el recibido
            error_count += parity_bit
            error_position += parity_bit

    # Corregir un solo error si se detectan errores
    if error_count > 0:
        encoded_data[error_position - 1] ^= 1

    # Eliminar los bits de paridad y devolver el número de errores y los datos corregidos
    decoded_data = encoded_data[num_parity_bits:]

    return error_count, decoded_data

def encode_frame(data_bit, num_parity_bits):
    simbolo = []
    encoded_data = []
    for i in range(len(data_bit)):
        simbolo.append(data_bit[i])
        if len(simbolo) == (2**num_parity_bits - num_parity_bits):
            simbolo_codificado = encode(simbolo, num_parity_bits)
            encoded_data += simbolo_codificado
            simbolo = []  # Restablecer el símbolo
    return encoded_data

def decode_frame(encoded_data, num_parity_bits):
    simbolo_c = []
    decoded_data = []
    cont_error = 0
    num_error = 0
    for i in range(len(encoded_data)):
        simbolo_c.append(encoded_data[i])
        if len(simbolo_c) == (2**num_parity_bits):
            cont_error, simbolo_decodificado = decode(simbolo_c, num_parity_bits)
            decoded_data += simbolo_decodificado
            num_error += cont_error
            simbolo_c = []  # Restablecer el símbolo codificado
    return num_error, decoded_data
