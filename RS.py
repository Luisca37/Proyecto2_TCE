from reedsolo import RSCodec, ReedSolomonError
def encode(data):
    # se convierte la lista de bits a una lista de enteros para poder usar la librería
    byte_list = []
    byte = ""
    for i in range(len(data)):
        byte += str(data[i])
        if (i+1) % 8 == 0:
            byte_list.append(int(byte, 2))
            byte = ""
    # se usa la librería para codificar los datos
    rs = RSCodec(12)

    encoded = rs.encode(bytearray(byte_list))
    # se convierte la lista de enteros a una lista de bits
    bit_list = []
    for byte in encoded:
        bits = bin(byte)[2:].zfill(8)
        for bit in bits:
            bit_list.append(int(bit))
    return bit_list

def decode(data, size_data):
    simbolo_error = False
    # se convierte la lista de bits a una lista de enteros para poder usar la librería
    byte_list = []
    byte = ""
    pos_errores = []
    for i in range(len(data)):
        byte += str(data[i])
        if (i+1) % 8 == 0:
            byte_list.append(int(byte, 2))
            byte = ""

    # se usa la librería para decodificar los datos
    rs = RSCodec(12)
    try:
        decoded = rs.decode(bytearray(byte_list))[0]
        pos_errores = list(rs.decode(bytearray(byte_list))[2])
    except ReedSolomonError:
        decoded = bytearray(byte_list[:size_data//8])
        simbolo_error = True

    # se convierte la lista de enteros a una lista de bits

    bit_list = []
    for byte in decoded:
        bits = bin(byte)[2:].zfill(8)
        for bit in bits:
            bit_list.append(int(bit))

    return bit_list, pos_errores, simbolo_error




"""
data = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1]
print(len(data))
encoded  = encode(data)
print(encoded)
encoded[4] = encoded[4] ^ 1
encoded[5] = encoded[5] ^ 1
encoded[6] = encoded[6] ^ 1
encoded[7] = encoded[7] ^ 1

encoded[26] = encoded[26] ^ 1   
encoded[27] = encoded[27] ^ 1
encoded[28] = encoded[28] ^ 1
encoded[29] = encoded[29] ^ 1
decoded = decode(encoded)
print(decoded)

print(contar_diferencias(data, decoded))"""