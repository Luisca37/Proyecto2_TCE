def encode(data):
    # Asegurarse de que los datos de entrada tengan 4 bits
    if len(data) != 4:
        raise ValueError("Se requieren exactamente 4 bits de entrada")

    # Calcular los bits de paridad
    p1 = data[0] ^ data[1] ^ data[3]
    p2 = data[0] ^ data[2] ^ data[3]
    p3 = data[1] ^ data[2] ^ data[3]

    # Combinar datos y bits de paridad en un arreglo codificado de 7 bits
    encoded_data = [p1, p2, data[0], p3, data[1], data[2], data[3]]

    return encoded_data

def decode(encoded_data):
    # Asegurarse de que los datos de entrada tengan 7 bits
    if len(encoded_data) != 7:
        raise ValueError("Se requieren exactamente 7 bits de entrada")

    # Calcular los bits de paridad
    p1 = encoded_data[0]
    p2 = encoded_data[1]
    p3 = encoded_data[3]

    # Calcular los bits de paridad esperados
    expected_p1 = encoded_data[2] ^ encoded_data[4] ^ encoded_data[6]
    expected_p2 = encoded_data[2] ^ encoded_data[5] ^ encoded_data[6]
    expected_p3 = encoded_data[4] ^ encoded_data[5] ^ encoded_data[6]

    # Contadores para errores y posición de error
    error_count = 0
    error_position = 0

    # Verificar si los bits de paridad calculados son diferentes de los esperados
    if p1 != expected_p1:
        error_count += 1
        error_position += 1
    if p2 != expected_p2:
        error_count += 2
        error_position += 2
    if p3 != expected_p3:
        error_count += 4
        error_position += 4

    # Corregir un solo error si hay errores detectados
    if error_count > 0:
        encoded_data[error_position - 1] ^= 1
    print("Error count:", error_count)

    # Eliminar los bits de paridad y devolver el número de errores y los datos corregidos
    decoded_data = [encoded_data[2], encoded_data[4], encoded_data[5], encoded_data[6]]

    return error_count, decoded_data



def encode_frame(data_bit):
    simbolo = []
    encoded_data = []
    for i in range(len(data_bit)):
        simbolo.append(data_bit[i])
        if len(simbolo) == 4:
            simbolo_codificado = encode(simbolo)
            encoded_data += simbolo_codificado
            simbolo = []  # Restablecer el símbolo
    return encoded_data


def decode_frame(encoded_data):
    simbolo_c = []
    decoded_data = []
    cont_error = 0
    num_error = 0
    for i in range(len(encoded_data)):
        simbolo_c.append(encoded_data[i])
        
        if len(simbolo_c) == 7:
            
            cont_error, simbolo_decodificado = decode(simbolo_c)
            print("Simbolo codificado:", simbolo_c)
            decoded_data += simbolo_decodificado
            num_error += cont_error
            print("Simbolo decodificado:", simbolo_decodificado)
            simbolo_c = []  # Restablecer el símbolo codificado 

    
    return decoded_data, num_error   

