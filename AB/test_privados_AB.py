from functools import wraps
import signal
import platform
import unittest
import yolanda
import api_privado
import re
from datetime import date
from io import StringIO
from unittest.mock import patch

"""
Código del TimeoutError extraido y adaptado de
https://github.com/pnpnpn/timeout-decorator/tree/master
"""
N_SECOND = 1


class TimeoutError(AssertionError):

    """Thrown when a timeout occurs in the `timeout` context manager."""

    def __init__(self, value="Timed Out"):
        self.value = value

    def __str__(self):
        return repr(self.value)


def timeout(seconds=None):
    def decorate(function):
        def handler(signum, frame):
            raise TimeoutError("Timeout")

        @wraps(function)
        def new_function(*args, **kwargs):
            new_seconds = kwargs.pop('timeout', seconds)
            if new_seconds:
                old = signal.signal(signal.SIGALRM, handler)
                signal.setitimer(signal.ITIMER_REAL, new_seconds)

            if not seconds:
                return function(*args, **kwargs)

            try:
                return function(*args, **kwargs)
            finally:
                if new_seconds:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, old)

        if platform.system().lower() == 'windows':
            return function
        return new_function

    return decorate


class YolandaWebsService(unittest.TestCase):
    host = "localhost"
    port = 4444
    database = {
        "acuario": "Cuidado por donde caminas, puedes tropezar con una tortuga.",
        "aries": "Sé uno con la naturaleza, te traerá buena suerte",
        "leo": "Hoy es un día ideal para adoptar una tortuga.",
    }
    servidor = api_privado.Server(host, port, database, mode=2)
    yolanda = yolanda.Yolanda(host, port)
    servidor.start()

    def setUp(self) -> None:
        self.servidor.mode = 2
        self.database = {
            "acuario": "Cuidado por donde caminas, puedes tropezar con una tortuga.",
            "aries": "Sé uno con la naturaleza, te traerá buena suerte",
            "leo": "Hoy es un día ideal para adoptar una tortuga.",
        }
        self.servidor.database = {
            "acuario": "Cuidado por donde caminas, puedes tropezar con una tortuga.",
            "aries": "Sé uno con la naturaleza, te traerá buena suerte",
            "leo": "Hoy es un día ideal para adoptar una tortuga.",
        }

    #####################
    #      Saludar      #
    #####################
    def test_saludar_mode_1_verificar_todo(self):
        self.servidor.mode = 1
        respuesta = self.yolanda.saludar()
        today = date.today()
        resultado = f"Hoy es {today} y es un lindo día para recibir un horoscopo"

        self.assertIn("status-code", respuesta)
        self.assertIn("saludo", respuesta)
        self.assertEqual(respuesta["status-code"], 200)
        self.assertEqual(respuesta["saludo"], resultado)

    def test_saludar_mode_2_verificar_todo(self):
        self.servidor.mode = 2
        respuesta = self.yolanda.saludar()
        today = date.today()
        resultado = f"Hoy es {today} y quiero escribir horoscopos"

        self.assertIn("status-code", respuesta)
        self.assertIn("saludo", respuesta)
        self.assertEqual(respuesta["status-code"], 200)
        self.assertEqual(respuesta["saludo"], resultado)

    #####################
    #  Verificar Signo  #
    #####################

    def test_verificar_signo_tipo_respuesta(self):
        respuesta = self.yolanda.verificar_horoscopo("acuario")
        self.assertIsInstance(respuesta, bool)

    def test_verificar_signo_si_existe(self):
        respuesta = self.yolanda.verificar_horoscopo("acuario")
        self.assertEqual(respuesta, True)

    def test_verificar_signo_no_existe(self):
        respuesta = self.yolanda.verificar_horoscopo("Tortuga")
        self.assertEqual(respuesta, False)

    #####################
    #   Dar horoscopo   #
    #####################

    def test_dar_horoscopo_verificar_keys(self):
        respuesta = self.yolanda.dar_horoscopo("acuario")
        self.assertIn("status-code", respuesta)
        self.assertIn("mensaje", respuesta)

    def test_dar_horoscopo_existe_verificar_status_code(self):
        respuesta = self.yolanda.dar_horoscopo("acuario")
        self.assertIsInstance(respuesta, dict)
        self.assertEqual(respuesta['status-code'], 200)

    def test_dar_horoscopo_existe_verificar_mensaje(self):
        respuesta = self.yolanda.dar_horoscopo("acuario")
        self.assertIsInstance(respuesta, dict)
        self.assertEqual(respuesta["mensaje"], self.database["acuario"])

    def test_dar_horoscopo_no_existe_verificar_todo(self):
        respuesta = self.yolanda.dar_horoscopo("Tortuga")
        self.assertIsInstance(respuesta, dict)
        self.assertEqual(respuesta['status-code'], 400)
        self.assertEqual(respuesta["mensaje"], 'El signo no existe.')

    ###########################
    # Dar horoscopo aleatorio #
    ###########################

    def test_dar_horoscopo_aleatorio_mode_1(self):
        self.servidor.mode = 1
        respuesta = self.yolanda.dar_horoscopo_aleatorio()
        signo = list(self.database.keys())[0]
        self.assertIsInstance(respuesta, dict)
        self.assertEqual(respuesta["mensaje"], self.database[signo])

    def test_dar_horoscopo_aleatorio_mode_2(self):
        self.servidor.mode = 2
        respuesta = self.yolanda.dar_horoscopo_aleatorio()
        signo = list(self.database.keys())[-1]
        self.assertIsInstance(respuesta, dict)
        self.assertEqual(respuesta["mensaje"], self.database[signo])

    def test_dar_horoscopo_aleatorio_mode_3(self):
        self.servidor.mode = 3
        respuesta = self.yolanda.dar_horoscopo_aleatorio()
        self.assertIsInstance(respuesta, dict)
        self.assertEqual(respuesta['status-code'], 500)
        self.assertEqual(respuesta["mensaje"], "ups, no pude.")

    #####################
    # Agregar horoscopo #
    #####################

    @timeout(N_SECOND)
    def test_agregar_horoscopo_no_autorizado(self):
        respuesta = self.yolanda.agregar_horoscopo("leo", "grande messi", "TORTUGA")
        self.assertEqual(respuesta, "Agregar horoscopo no autorizado")

    @timeout(N_SECOND)
    def test_agregar_horoscopo_signo_ya_existe(self):
        respuesta = self.yolanda.agregar_horoscopo("leo", "grande messi", "morenoiic2233")
        self.assertEqual(respuesta, "El signo ya existe, no puedes modificarlo")

    @timeout(N_SECOND)
    def test_agregar_horoscopo_signo_mensaje_muy_corto(self):
        respuesta = self.yolanda.agregar_horoscopo("leo", "a", "morenoiic2233")
        self.assertEqual(respuesta, "El mensaje debe tener más de 4 caracteres")

    @timeout(N_SECOND)
    def test_agregar_horoscopo_ok_verificar_respuesta(self):
        mensaje = "grande messi"
        respuesta = self.yolanda.agregar_horoscopo("piscis", mensaje, "morenoiic2233")
        self.assertEqual(respuesta, "La base de YolandaAPI ha sido actualizada")

    @timeout(N_SECOND)
    def test_agregar_horoscopo_ok_verificar_base_datos(self):
        mensaje = "grande messi"
        self.yolanda.agregar_horoscopo("piscis", mensaje, "morenoiic2233")
        self.assertIn("piscis", self.servidor.database)
        self.assertEqual(mensaje, self.servidor.database["piscis"])

    ########################
    # Actualizar horoscopo #
    ########################

    @timeout(N_SECOND)
    def test_actualizar_horoscopo_no_autorizado(self):
        respuesta = self.yolanda.actualizar_horoscopo("leo", "grande messi", "TORTUGA")
        self.assertEqual(respuesta, "Editar horoscopo no autorizado")

    @timeout(N_SECOND)
    def test_actualizar_horoscopo_signo_no_existe(self):
        respuesta = self.yolanda.actualizar_horoscopo("messi", "grande messi", "morenoiic2233")
        self.assertEqual(respuesta, "El signo no existe.")

    @timeout(N_SECOND)
    def test_actualizar_horoscopo_signo_mensaje_muy_corto(self):
        respuesta = self.yolanda.actualizar_horoscopo("acuario", "a", "morenoiic2233")
        self.assertEqual(respuesta, "El mensaje debe tener más de 4 caracteres")

    @timeout(N_SECOND)
    def test_actualizar_horoscopo_ok_verificar_respuesta(self):
        mensaje = "grande messi"
        respuesta = self.yolanda.actualizar_horoscopo("acuario", mensaje, "morenoiic2233")
        self.assertEqual(respuesta, "La base de YolandaAPI ha sido actualizada")

    @timeout(N_SECOND)
    def test_actualizar_horoscopo_ok_verificar_base_datos(self):
        mensaje = "grande messi"
        self.yolanda.actualizar_horoscopo("acuario", mensaje, "morenoiic2233")
        self.assertEqual(mensaje, self.servidor.database["acuario"])

    ##################
    # Eliminar signo #
    ##################

    @timeout(N_SECOND)
    def test_eliminar_signo_no_autorizado(self):
        respuesta = self.yolanda.eliminar_signo("leo", "TORTUGA")
        self.assertEqual(respuesta, "Eliminar signo no autorizado")

    @timeout(N_SECOND)
    def test_eliminar_signo_signo_no_existe(self):
        respuesta = self.yolanda.eliminar_signo("messi", "morenoiic2233")
        self.assertEqual(respuesta, "El signo no existe.")

    @timeout(N_SECOND)
    def testeliminar_signo_ok_verificar_respuesta(self):
        respuesta = self.yolanda.eliminar_signo("acuario", "morenoiic2233")
        self.assertEqual(respuesta, "La base de YolandaAPI ha sido actualizada")

    @timeout(N_SECOND)
    def test_eliminar_signo_ok_verificar_base_datos(self):
        self.yolanda.eliminar_signo("acuario", "morenoiic2233")
        self.assertNotIn("acuario", self.servidor.database)


class RegexTests(unittest.TestCase):
    yolanda = yolanda.Yolanda('', '')

    ##############################
    #      Validador fechas      #
    ##############################

    def test_validar_fechas_validas_1(self):
        texto = "02\tde AgosTo de 95"
        respuesta = re.match(self.yolanda.regex_validador_fechas, texto)
        self.assertIsInstance(respuesta, re.Match)
        self.assertEqual(respuesta.group(0), texto)

    def test_validar_fechas_validas_2(self):
        texto = "19 de abrilll de\n2018"
        respuesta = re.match(self.yolanda.regex_validador_fechas, texto)
        self.assertIsInstance(respuesta, re.Match)
        self.assertEqual(respuesta.group(0), texto)

    def test_validar_fechas_validas_3(self):
        texto = "31 de JUNIOO\tde 2023"
        respuesta = re.match(self.yolanda.regex_validador_fechas, texto)
        self.assertIsInstance(respuesta, re.Match)
        self.assertEqual(respuesta.group(0), texto)

    def test_validar_fechas_validas_4(self):
        texto = "4 de ctbrP de 01"
        respuesta = re.match(self.yolanda.regex_validador_fechas, texto)
        self.assertIsInstance(respuesta, re.Match)
        self.assertEqual(respuesta.group(0), texto)

    def test_validar_fechas_validas_5(self):
        texto = "17 de calzo de 2010"
        respuesta = re.match(self.yolanda.regex_validador_fechas, texto)
        self.assertIsInstance(respuesta, re.Match)
        self.assertEqual(respuesta.group(0), texto)

    def test_validar_fechas_validas_6(self):
        texto = "12 de\tnoviembreee de 22"
        respuesta = re.match(self.yolanda.regex_validador_fechas, texto)
        self.assertIsInstance(respuesta, re.Match)
        self.assertEqual(respuesta.group(0), texto)

    def test_validar_fechas_validas_7(self):
        texto = "44 de ABRILL de 1999"
        respuesta = re.match(self.yolanda.regex_validador_fechas, texto)
        self.assertIsInstance(respuesta, re.Match)
        self.assertEqual(respuesta.group(0), texto)

    def test_validar_fechas_invalidas_1(self):
        texto = "007 de agosto de 1997"
        respuesta = re.search(self.yolanda.regex_validador_fechas, texto)
        self.assertEqual(respuesta, None)

    def test_validar_fechas_invalidas_2(self):
        texto = "11 de noviembre de 023"
        respuesta = re.search(self.yolanda.regex_validador_fechas, texto)
        self.assertEqual(respuesta, None)

    def test_validar_fechas_invalidas_3(self):
        texto = "0 de sept de 20221"
        respuesta = re.search(self.yolanda.regex_validador_fechas, texto)
        self.assertEqual(respuesta, None)

    def test_validar_fechas_invalidas_4(self):
        texto = "18 de abril de 2128"
        respuesta = re.search(self.yolanda.regex_validador_fechas, texto)
        self.assertEqual(respuesta, None)

    def test_validar_fechas_invalidas_5(self):
        texto = "30 de juNIO de 1823"
        respuesta = re.search(self.yolanda.regex_validador_fechas, texto)
        self.assertEqual(respuesta, None)

    def test_validar_fechas_invalidas_6(self):
        texto = "8, octubre de 2001"
        respuesta = re.search(self.yolanda.regex_validador_fechas, texto)
        self.assertEqual(respuesta, None)

    def test_validar_fechas_invalidas_7(self):
        texto = "14/marzo/2011"
        respuesta = re.search(self.yolanda.regex_validador_fechas, texto)
        self.assertEqual(respuesta, None)

    def test_validar_fechas_invalidas_8(self):
        texto = "9 de 07 de 1999"
        respuesta = re.search(self.yolanda.regex_validador_fechas, texto)
        self.assertEqual(respuesta, None)

    #######################################
    #      Verificar extractor signo      #
    #######################################

    def test_extraer_signo_valido_1(self):
        texto = "Las   capricornianas pueden   dormir la mejor siesta del semestre."
        signo_espeado = "capricornianas"
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertIsInstance(respuesta, re.Match)
        signo = respuesta.group(1)
        self.assertEqual(signo, signo_espeado)

    def test_extraer_signo_valido_2(self):
        texto = "Los\tSAGITARIANOS\t\n\tpueden vivir el mejor día de su vida."
        signo_espeado = "SAGITARIANOS"
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertIsInstance(respuesta, re.Match)
        signo = respuesta.group(1)
        self.assertEqual(signo, signo_espeado)

    def test_extraer_signo_valido_3(self):
        texto = "Los\nacuarianos pueden volver a escuchar la mejor canción de su vida."
        signo_espeado = "acuarianos"
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertIsInstance(respuesta, re.Match)
        signo = respuesta.group(1)
        self.assertEqual(signo, signo_espeado)

    def test_extraer_signo_valido_4(self):
        texto = "Los    otakus pueden ver anime todo el día."
        signo_espeado = "otakus"
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertIsInstance(respuesta, re.Match)
        signo = respuesta.group(1)
        self.assertEqual(signo, signo_espeado)

    def test_extraer_signo_valido_5(self):
        texto = "Las liBRianas pueden ser libres por 1 semana."
        signo_espeado = "liBRianas"
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertIsInstance(respuesta, re.Match)
        signo = respuesta.group(1)
        self.assertEqual(signo, signo_espeado)

    def test_extraer_signo_valido_6(self):
        texto = "Los reptilianos    pueden ver su serie favorita en la noche."
        signo_espeado = "reptilianos"
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertIsInstance(respuesta, re.Match)
        signo = respuesta.group(1)
        self.assertEqual(signo, signo_espeado)

    def test_extraer_signo_valido_7(self):
        texto = "Las pisqianas pueden    comer su almuerzo favorito mañana."
        signo_espeado = "pisqianas"
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertIsInstance(respuesta, re.Match)
        signo = respuesta.group(1)
        self.assertEqual(signo, signo_espeado)

    def test_extraer_signo_invalido_1(self):
        texto = "Los_arianos pueden   dormir la mejor siesta de su vida."  # No hay espacio entre Los y signo
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertEqual(respuesta, None)

    def test_extraer_signo_invalido_2(self):
        texto = "Las pisqianas+pueden    comer su postre favorito hoy."  # No hay espacio entre signo y pueden
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertEqual(respuesta, None)

    def test_extraer_signo_invalido_3(self):
        texto = "Lus   tuurunus  pueden   vivir su mejor día de su vida."  # Lis no es Las o Los
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertEqual(respuesta, None)

    def test_extraer_signo_invalido_4(self):
        texto = "las\tacuarianas\npueden volver a escuchar la mejor canción de su vida."  # Las no parte con mayúscula
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertEqual(respuesta, None)

    def test_extraer_signo_invalido_5(self):
        texto = "Los escorpio pueden escuchar Mozart con las aquarianas."  # Signo no está en plural
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertEqual(respuesta, None)

    def test_extraer_signo_invalido_6(self):
        texto = "Las liBRianas serán libres por 11 día."  # Falta pueden después del signo
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertEqual(respuesta, None)

    def test_extraer_signo_invalido_7(self):
        texto = "Los reptilianos    pueden ver su serie favorita en la noche"  # Falta el punto al final
        respuesta = re.search(self.yolanda.regex_extractor_signo, texto)
        self.assertEqual(respuesta, None)


if __name__ == '__main__':
    with patch('sys.stdout', new=StringIO()):
        unittest.main(verbosity=1)
