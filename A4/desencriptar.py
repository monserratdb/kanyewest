from typing import List
import json
from errors import JsonError, SequenceError


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    # Completar
    # mensaje = mensaje_codificado.decode("utf-8")
    # diccionario = dict(substring.split("=") for substring in mensaje.split(";"))
    # return diccionario
    try:
        decoded_str = mensaje_codificado.decode('utf-8')
        dictionary = json.loads(decoded_str)
        return dictionary
    except json.JSONDecodeError:
        raise JsonError('Error al deserializar el diccionario')
    

def decodificar_largo(mensaje: bytearray) -> int:
    # Completar
    # for i in range(0, len(mensaje), 4):
    #     numero = int.from_bytes(i, byteorder="big")
    # return numero
    largo_bytes = mensaje[:4]
    largo = int.from_bytes(largo_bytes, 'big')
    return largo


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    # m_bytes_secuencia = bytearray()
    # m_reducido = bytearray()
    # secuencia_codificada = bytearray()
    # # Completar
    # largo = decodificar_largo(mensaje)
    # return [m_bytes_secuencia, m_reducido, secuencia_codificada]
    largo_secuencia = decodificar_largo(mensaje)
    secuencia_codificada = mensaje[-8:]
    m_bytes_secuencia = mensaje[4:4 + largo_secuencia]
    m_reducido = mensaje[4 + largo_secuencia:-8]
    return [m_bytes_secuencia, m_reducido, secuencia_codificada]

def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    # Completar
    # transformados = []
    # for i in secuencia_codificada:
    #     numero = int.from_bytes(i, byteorder="big")
    #     transformados.append(numero)
    # return transformados
    secuencia = []
    for i in range(0, len(secuencia_codificada), 2):
        num = int.from_bytes(secuencia_codificada[i:i+2], 'big')
        secuencia.append(num)
    return secuencia

def desencriptar(mensaje: bytearray) -> bytearray:
    # Completar
    # original = bytearray()
    # largo = decodificar_largo(mensaje)
    # msj = separar_msg_encriptado(mensaje)
    # sec = decodificar_secuencia(mensaje)
    # original.extend(largo, msj, sec)
    # return original
    m_bytes_secuencia, m_reducido, secuencia_codificada = separar_msg_encriptado(mensaje)
    secuencia = decodificar_secuencia(secuencia_codificada)
    mensaje_original = bytearray(m_reducido)
    for i, byte in enumerate(m_bytes_secuencia):
        pos = secuencia[i]
        mensaje_original.insert(pos, byte)
    return mensaje_original


if __name__ == "__main__":
    mensaje = bytearray(b'\x00\x00\x00\x04"a}a{tm": 1\x00\x01\x00\x05\x00\n\x00\x03')
    desencriptado = desencriptar(mensaje)
    diccionario = deserializar_diccionario(desencriptado)
    print(diccionario)
