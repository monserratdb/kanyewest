from typing import List
import json
from errors import JsonError, SequenceError


def serializar_diccionario(dictionary: dict) -> bytearray:
    # Completar
    # json_string = json.dumps(dictionary)
    # try:
    #     mensaje = bytearray(json_string.encode("UTF-8"))
    #     return mensaje
    # except TypeError:
    #     raise json.JSONDecodeError
    try:
        json_str = json.dumps(dictionary)
        encoded_str = json_str.encode('utf-8')
        return bytearray(encoded_str)
    except TypeError:
        raise JsonError('Error al serializar el diccionario')


def verificar_secuencia(mensaje: bytearray, secuencia: List[int]) -> None:
    # Completar
    # try:
    #     for i in range(len(mensaje)-1):
    #         if mensaje[i] > len(mensaje):
    #             print("error")
    #         else:
    #             if mensaje[i] == mensaje[i-1]:
    #                 print("error")
    #             else:
    #                 #msj y byytes son del tipo bytearray
    #                 mensaje_original = bytearray()
    #                 byytes = bytearray() #bytes indicados en la sec de num
    #                 for j in secuencia:
    #                     if i == j:
    #                         mensaje.pop(i)
    #                         byytes.append(mensaje[i])
    #                     else:
    #                         mensaje_original.append(mensaje[i])
    # except:
    #     raise SequenceError
    if max(secuencia) >= len(mensaje):
        raise SequenceError('El número más grande de la secuencia es mayor o igual al largo del mensaje')
    if len(secuencia) != len(set(secuencia)):
        raise SequenceError('Existen números repetidos en la secuencia')


def codificar_secuencia(secuencia: List[int]) -> bytearray:
    # Completar
#     vacio = bytearray()
#     for i in secuencia:
#         vacio.extend(i.to_bytes(2, byteorder="big"))
#     return vacio
# #'bytes' object cannot be interpreted as an integer
    encoded_seq = bytearray()
    for num in secuencia:
        encoded_seq.extend(num.to_bytes(2, 'big'))
    return encoded_seq


def codificar_largo(largo: int) -> bytearray:
    # Completar
    # num_transformado = bytearray()
    # lol = largo.to_bytes(4, byteorder="big")
    # num_transformado.extend(lol)
    # return num_transformado
    return largo.to_bytes(4, 'big')


def separar_msg(mensaje: bytearray, secuencia: List[int]) -> List[bytearray]:
    # m_bytes_secuencia = bytearray()
    # m_reducido = bytearray()
    # # Completar
    # for i in range(len(mensaje)-1):
    #     for j in secuencia:
    #         if i == j:
    #             mensaje.pop(i)
    #             m_bytes_secuencia.append(mensaje[i])
    #         else:
    #             m_reducido.append(mensaje[i])
    # return [m_bytes_secuencia, m_reducido]
    m_reducido = bytearray([mensaje[i] for i in range(len(mensaje)) if i not in secuencia])
    m_bytes_secuencia = bytearray([mensaje[i] for i in secuencia])
    return [m_reducido, m_bytes_secuencia]


def encriptar(mensaje: dict, secuencia: List[int]) -> bytearray:
    verificar_secuencia(mensaje, secuencia)

    m_bytes_secuencia, m_reducido = separar_msg(mensaje, secuencia)
    secuencia_codificada = codificar_secuencia(secuencia)

    return (
        codificar_largo(len(secuencia))
        + m_bytes_secuencia
        + m_reducido
        + secuencia_codificada
    )


if __name__ == "__main__":
    original = serializar_diccionario({"tama": 1})
    encriptado = encriptar(original, [1, 5, 10, 3])
    print(original)
    print(encriptado)
