def encode(dato):
    """
    Codifica una lista de 1s y 0s utilizando un código de repetición (4, 1).

    Args:
        dato (list): Lista de 1s y 0s a codificar.

    Returns:
        list: Lista de 4s y 0s que representa el dato codificado.
    """
    codificado = []
    for bit in dato:
        if bit == 1:
            codificado.extend([1, 1, 1, 1])
        else:
            codificado.extend([0, 0, 0, 0])
    return codificado


def decode(codificado):
    """
    Decodifica una lista de 4s y 0s utilizando un código de repetición (4, 1).

    Args:
        codificado (list): Lista de 4s y 0s a decodificar.

    Returns:
        list: Lista de 1s y 0s que representa el dato decodificado.
    """
    decodificado = []
    for i in range(0, len(codificado), 4):
        grupo = codificado[i:i+4]
        if grupo.count(1) > grupo.count(0):
            decodificado.append(1)
        else:
            decodificado.append(0)
    return decodificado
