import api
import re
import requests
import time


class Yolanda:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"
        self.regex_validador_fechas = r'\b(\d{1,2})\s+de\s+([a-zA-Z]+)\s+de\s+((?:19|20)?\d{2})\b'
        self.regex_extractor_signo = r'(?i)(?:Los|Las)\s+([A-Za-z]+)\s+pueden\s+.*\.'

    def saludar(self) -> dict:
        respp = requests.get(f"{self.base}/")
        resp = respp.json()
        status = respp.status_code
        dic = {"status-code": status, "saludo": resp["result"]}
        return dic

    def verificar_horoscopo(self, signo: str) -> bool:
        # TODO: Completar
        respp = requests.get(f"{self.base}/signos")
        resp = respp.json()
        for i in resp["result"]:
            if i == signo:
                return True
            elif i != signo:
                return False

    def dar_horoscopo(self, signo: str) -> dict:
        # TODO: Completar
        params_s = {"signo": signo}
        respp = requests.get(f"{self.base}/horoscopo", params=params_s)
        resp = respp.json()
        # horoscopo asociado a cada signo
        status = respp.status_code
        dic = {"status-code": status, "mensaje": resp["result"]}
        return dic

    def dar_horoscopo_aleatorio(self) -> dict:
        # TODO: Completar
        respp = requests.get(f"{self.base}/aleatorio")
        status = respp.status_code
        resp = respp.json()

        if status != 200:
            mensaje = resp["result"]
            dic = {"status-code": status, "mensaje": mensaje}
            return dic
        else:
            enlace = resp["result"]
            respuessta = requests.get(enlace)
            status_code = respuessta.status_code
            respuesta = respuessta.json()

            mensajee = respuesta["result"]
            dicc = {"status-code": status_code, "mensaje": mensajee}
            return dicc

    def agregar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        m_headers = {
            "Authorization": access_token
        }
        data_m = {"signo": signo, "mensaje": mensaje}
        respp = requests.post(f"{self.base}/update", headers=m_headers, data= data_m)
        status = respp.status_code
        resp = respp.json()
        if status == 401:
            return "Agregar horoscopo no autorizado"
        elif status == 400:
            return resp["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"

    def actualizar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        # TODO: Completar
        m_headers = {
            "Authorization": access_token
        }
        data_m = {"signo": signo, "mensaje": mensaje}
        url = f"{self.base}/update"
        respp = requests.put(url, headers=m_headers, data=data_m)
        status = respp.status_code
        resp = respp.json()
        if status == 401:
            return "Editar horoscopo no autorizado"
        elif status == 400:
            return resp["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"

    def eliminar_signo(self, signo: str, access_token: str) -> str:
        # TODO: Completar
        m_headers = {
            "Authorization": access_token
        }
        data_m = {"signo": signo}
        url = f"{self.base}/remove"
        respp = requests.delete(url, headers=m_headers, data=data_m)
        status = respp.status_code
        resp = respp.json()
        if status == 401:
            return "Eliminar signo no autorizado"
        elif status == 400:
            return resp["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "acuario": "Hoy será un hermoso día",
        "leo": "No salgas de casa.... te lo recomiendo",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    yolanda = Yolanda(HOST, PORT)
    print(yolanda.saludar())
    print(yolanda.dar_horoscopo_aleatorio())
    print(yolanda.verificar_horoscopo("acuario"))
    print(yolanda.verificar_horoscopo("pokemon"))
    print(yolanda.dar_horoscopo("acuario"))
    print(yolanda.dar_horoscopo("pokemon"))
    print(yolanda.agregar_horoscopo("a", "aaaaa", "pepaiic2233"))
    print(yolanda.dar_horoscopo("a"))
