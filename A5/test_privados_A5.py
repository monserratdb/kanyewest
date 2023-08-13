import unittest
import funciones
import inspect
import re
from typing import Generator
from os import remove
from utilidades import Categoria, Producto
from itertools import groupby


class ComandoProhibidoError(BaseException):
    def __init__(self, comandos: list, prohibido: bool = True, *args: object) -> None:
        if prohibido:
            mensaje = "Se utiliza alguno de estos elementos en la función: "
        else:
            mensaje = "No se utiliza alguno de estos elementos esperado en la función: "
        mensaje += ", ".join(comandos)
        super().__init__(mensaje, *args[2:])


def usa_comando_prohibido(func, comandos):
    codigo_fuente = inspect.getsource(func).replace("\\", " ")
    codigo = codigo_fuente.strip()
    for comando in comandos:
        expresion = rf'{comando}([^\n]\s+)'
        if re.search(expresion, codigo):
            raise ComandoProhibidoError(comandos)


def usa_metodo_prohibido(func, comandos):
    codigo_fuente = inspect.getsource(func).replace("\\", " ")
    codigo = codigo_fuente.strip()
    for comando in comandos:
        expresion = rf'{comando}\s*\('
        if re.search(expresion, codigo):
            raise ComandoProhibidoError(comandos)


def usa_metodo_esperado(func, comandos):
    codigo_fuente = inspect.getsource(func).replace("\\", " ")
    codigo = codigo_fuente.strip()
    for comando in comandos:
        expresion = rf'{comando}\s*\('
        if re.search(expresion, codigo):
            return True
    raise ComandoProhibidoError(comandos, False)


class TestCargarDatos(unittest.TestCase):
    data_productos = [
        'id_producto,nombre,precio,pasillo,medida,unidad_medida\n'
        '15,Aceitunas,2490,Pasillo 5,200,gr',

        'id_producto,nombre,precio,pasillo,medida,unidad_medida\n'
        '6,Cebollas,790,Pasillo 3,500,gr\n'
        '7,Papas,1490,Pasillo 3,1000,gr\n'
        '8,Jamón,2990,Pasillo 4,200,gr\n'
        '9,Pan de molde,1490,Pasillo 4,500,gr\n'
        '10,Salsa de tomate,990,Pasillo 5,500,ml',

        'id_producto,nombre,precio,pasillo,medida,unidad_medida\n'
        '2,Leche,1190,Pasillo 2,1000,ml\n'
        '3,Manzanas,990,Pasillo 3,500,gr\n'
        '14,Huevos,1990,Pasillo 3,12,unidades',

        'id_producto,nombre,precio,pasillo,medida,unidad_medida\n'
        '1,Arroz,1990,Pasillo 1,1000,gr\n'
        '2,Leche,1190,Pasillo 2,1000,ml\n'
        '3,Manzanas,990,Pasillo 3,500,gr\n'
        '4,Pan integral,2490,Pasillo 4,500,gr\n'
        '5,Aceite de oliva,5990,Pasillo 5,500,ml\n'
        '6,Yogur,790,Pasillo 2,200,gr\n'
        '7,Papas,1490,Pasillo 3,1000,gr\n'
        '8,Jamón,2990,Pasillo 4,200,gr\n'
        '9,Pan de molde,1490,Pasillo 4,500,gr\n'
        '10,Salsa de tomate,990,Pasillo 5,500,ml\n'
        '11,Cebollas,790,Pasillo 3,500,gr\n'
        '12,Queso,3490,Pasillo 2,250,gr\n'
        '13,Fideos,590,Pasillo 1,500,gr\n'
        '14,Huevos,1990,Pasillo 3,12,unidades\n'
        '15,Aceitunas,2490,Pasillo 5,200,gr\n'
        '16,Tomates,1490,Pasillo 3,500,gr\n'
        '17,Mantequilla,1490,Pasillo 2,200,gr\n'
        '18,Atun,1990,Pasillo 5,200,gr\n'
        '19,Cafe,2990,Pasillo 1,250,gr\n'
        '20,Azucar,990,Pasillo 4,500,gr'
    ]
    data_categorias = [
        'nombre_categoria,id_producto\nConservas,15',

        'nombre_categoria,id_producto\nVerduras,6\nVerduras,7\nCarnes,8\n'
        'Embutidos,8\nPanaderia,9\nSalsas,10\nConservas,10',

        'nombre_categoria,id_producto\nLacteos,2\nFrutas,3\nLacteos,14',

        'nombre_categoria,id_producto\nCereales,1\nGranos,1\nLacteos,2\n'
        'Frutas,3\nPanaderia,4\nAceites,5\nLacteos,6\nPostres,6\n'
        'Verduras,7\nCarnes,8\nEmbutidos,8\nPanaderia,9\nSalsas,10\n'
        'Conservas,10\nVerduras,11\nLacteos,12\nPastas,13\nLacteos,14\n'
        'Conservas,15\nVerduras,16\nLacteos,17\nConservas,18\nBebidas,19\n'
        'Cafe,19\nEndulzantes,20\nReposteria,20'
    ]

    @classmethod
    def setUpClass(cls):
        for i in range(len(cls.data_productos)):
            with open(f'productos_{i + 1}.csv', 'w') as file:
                file.write(cls.data_productos[i])

            with open(f'categorias_{i + 1}.csv', 'w') as file:
                file.write(cls.data_categorias[i])

    @classmethod
    def tearDownClass(cls):
        for i in range(len(cls.data_productos)):
            remove(f'productos_{i + 1}.csv')
            remove(f'categorias_{i + 1}.csv')

    def test_cargar_productos_1(self):
        datos = funciones.cargar_productos('productos_1.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        producto = Producto(15, "Aceitunas", 2490, "Pasillo 5", 200, "gr")
        self.assertSequenceEqual(lista_datos[0], producto)
        self.assertSequenceEqual(lista_datos[-1], producto)

    def test_cargar_productos_2(self):
        datos = funciones.cargar_productos('productos_2.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        producto_1 = Producto(6, "Cebollas", 790, "Pasillo 3", 500, "gr")
        producto_2 = Producto(7, "Papas", 1490, "Pasillo 3", 1000, "gr")
        producto_3 = Producto(8, "Jamón", 2990, "Pasillo 4", 200, "gr")
        producto_4 = Producto(9, "Pan de molde", 1490, "Pasillo 4", 500, "gr")
        producto_5 = Producto(10, "Salsa de tomate", 990, "Pasillo 5", 500, "ml")
        self.assertSequenceEqual(lista_datos[0], producto_1)
        self.assertSequenceEqual(lista_datos[1], producto_2)
        self.assertSequenceEqual(lista_datos[2], producto_3)
        self.assertSequenceEqual(lista_datos[3], producto_4)
        self.assertSequenceEqual(lista_datos[4], producto_5)

    def test_cargar_productos_3(self):
        datos = funciones.cargar_productos('productos_3.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        producto_1 = Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
        producto_2 = Producto(3, "Manzanas", 990, "Pasillo 3", 500, "gr")
        producto_3 = Producto(14, "Huevos", 1990, "Pasillo 3", 12, "unidades")
        self.assertSequenceEqual(lista_datos[0], producto_1)
        self.assertSequenceEqual(lista_datos[1], producto_2)
        self.assertSequenceEqual(lista_datos[2], producto_3)

    def test_cargar_productos_4(self):
        datos = funciones.cargar_productos('productos_4.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        producto_2 = Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
        producto_20 = Producto(20, "Azucar", 990, "Pasillo 4", 500, "gr")
        self.assertSequenceEqual(lista_datos[1], producto_2)
        self.assertSequenceEqual(lista_datos[-1], producto_20)

    def test_cargar_categorias_1(self):
        datos = funciones.cargar_categorias('categorias_1.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        categoria = Categoria("Conservas", 15)
        self.assertSequenceEqual(lista_datos[0], categoria)
        self.assertSequenceEqual(lista_datos[-1], categoria)

    def test_cargar_categorias_2(self):
        datos = funciones.cargar_categorias('categorias_2.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        categoria_1 = Categoria("Verduras", 6)
        categoria_2 = Categoria("Verduras", 7)
        categoria_7 = Categoria("Conservas", 10)
        self.assertSequenceEqual(lista_datos[0], categoria_1)
        self.assertSequenceEqual(lista_datos[1], categoria_2)
        self.assertSequenceEqual(lista_datos[-1], categoria_7)

    def test_cargar_categorias_3(self):
        datos = funciones.cargar_categorias('categorias_3.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        categoria_1 = Categoria("Lacteos", 2)
        categoria_2 = Categoria("Frutas", 3)
        categoria_3 = Categoria("Lacteos", 14)
        self.assertSequenceEqual(lista_datos[0], categoria_1)
        self.assertSequenceEqual(lista_datos[1], categoria_2)
        self.assertSequenceEqual(lista_datos[2], categoria_3)
        self.assertSequenceEqual(lista_datos[-1], categoria_3)

    def test_cargar_categorias_4(self):
        datos = funciones.cargar_categorias('categorias_4.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        categoria_1 = Categoria("Cereales", 1)
        categoria_n = Categoria("Reposteria", 20)
        self.assertSequenceEqual(lista_datos[0], categoria_1)
        self.assertSequenceEqual(lista_datos[25], categoria_n)
        self.assertSequenceEqual(lista_datos[-1], categoria_n)


class TestConsultas(unittest.TestCase):

    def generador_producto(self, variacion):
        if variacion == 1:
            yield Producto(6, "Cebollas", 790, "Pasillo 3", 500, "gr")
            yield Producto(7, "Papas", 1490, "Pasillo 3", 1000, "gr")
        elif variacion == 2:
            yield Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
            yield Producto(5, "Aceite de oliva", 5990, "Pasillo 5", 500, "ml")
        elif variacion == 3:
            yield Producto(3, "Manzanas", 990, "Pasillo 3", 500, "gr")
            yield Producto(4, "Pan integral", 2490, "Pasillo 4", 500, "gr")
        elif variacion == 4:
            yield Producto(8, "Jamon", 2990, "Pasillo 4", 200, "gr")
            yield Producto(9, "Pan de molde", 1490, "Pasillo 4", 500, "gr")
            yield Producto(14, "Huevos", 1990, "Pasillo 3", 12, "unidades")
            yield Producto(10, "Salsa de tomate", 990, "Pasillo 5", 500, "ml")

    def test_obtener_productos_1(self):
        datos = funciones.obtener_productos(self.generador_producto(1))
        self.assertIsInstance(datos, map)
        lista_datos = list(datos)
        self.assertSequenceEqual(lista_datos, ["Cebollas", "Papas"])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_productos, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_productos, ["list", "dict", "set", "tuple"])

    def test_obtener_productos_2(self):
        datos = funciones.obtener_productos(self.generador_producto(2))
        self.assertIsInstance(datos, map)
        lista_datos = list(datos)
        self.assertSequenceEqual(lista_datos, ["Leche", "Aceite de oliva"])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_productos, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_productos, ["list", "dict", "set", "tuple"])

    def test_obtener_productos_3(self):
        datos = funciones.obtener_productos(self.generador_producto(3))
        self.assertIsInstance(datos, map)
        lista_datos = list(datos)
        self.assertSequenceEqual(lista_datos, ["Manzanas", "Pan integral"])
        
        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_productos, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_productos, ["list", "dict", "set", "tuple"])

    def test_obtener_productos_4(self):
        datos = funciones.obtener_productos(self.generador_producto(4))
        self.assertIsInstance(datos, map)
        lista_datos = list(datos)
        self.assertSequenceEqual(lista_datos, ["Jamon", "Pan de molde", "Huevos", "Salsa de tomate"])
        
        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_productos, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_productos, ["list", "dict", "set", "tuple"])

    def test_obtener_productos_vacio(self):
        datos = funciones.obtener_productos(self.generador_producto(5))
        self.assertIsInstance(datos, map)
        lista_datos = list(datos)
        self.assertSequenceEqual(lista_datos, [])
        
        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_productos, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_productos, ["list", "dict", "set", "tuple"])

    def test_obtener_precio_promedio_1(self):
        promedio = funciones.obtener_precio_promedio(self.generador_producto(1))
        self.assertIsInstance(promedio, int)
        self.assertEqual(promedio, 1140)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_precio_promedio, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_precio_promedio, ["list", "dict", "set", "tuple"])

    def test_obtener_precio_promedio_2(self):
        promedio = funciones.obtener_precio_promedio(self.generador_producto(2))
        self.assertIsInstance(promedio, int)
        self.assertEqual(promedio, 3590)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_precio_promedio, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_precio_promedio, ["list", "dict", "set", "tuple"])

    def test_obtener_precio_promedio_3(self):
        promedio = funciones.obtener_precio_promedio(self.generador_producto(3))
        self.assertIsInstance(promedio, int)
        self.assertEqual(promedio, 1740)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_precio_promedio, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_precio_promedio, ["list", "dict", "set", "tuple"])

    def test_obtener_precio_promedio_extra(self):
        promedio = funciones.obtener_precio_promedio(self.generador_producto(4))
        self.assertIsInstance(promedio, int)
        self.assertEqual(promedio, 1865)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.obtener_precio_promedio, ["for", "while"])
        usa_metodo_prohibido(funciones.obtener_precio_promedio, ["list", "dict", "set", "tuple"])


class TestFiltros(unittest.TestCase):

    def generador_producto(self, variacion):
        if variacion == 1:
            yield Producto(6, "Cebollas", 790, "Pasillo 3", 500, "gr")
            yield Producto(7, "Papas", 1490, "Pasillo 3", 1000, "gr")
        elif variacion == 2:
            yield Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
            yield Producto(5, "Aceite de oliva", 5990, "Pasillo 5", 500, "ml")
        elif variacion == 3:
            yield Producto(3, "Manzanas", 990, "Pasillo 3", 500, "gr")
            yield Producto(4, "Pan integral", 2490, "Pasillo 4", 500, "gr")
        elif variacion == 4:
            yield Producto(8, "Jamon", 2990, "Pasillo 4", 200, "gr")
            yield Producto(9, "Pan de molde", 1490, "Pasillo 4", 500, "gr")
            yield Producto(10, "Salsa de tomate", 990, "Pasillo 5", 500, "ml")
            yield Producto(14, "Huevos", 1990, "Pasillo 3", 12, "unidades")
            yield Producto(15, "Aceitunas", 2490, "Pasillo 5", 200, "gr")

    def generador_categoria(self, variacion):
        if variacion == 1:
            yield Categoria("Verduras", 6)
            yield Categoria("Verduras", 7)
        elif variacion == 2:
            yield Categoria("Lacteos", 2)
            yield Categoria("Aceites", 5)
        elif variacion == 3:
            yield Categoria("Frutas", 3)
            yield Categoria("Panaderia", 4)
        elif variacion == 4:
            yield Categoria("Carnes", 8)
            yield Categoria("Embutidos", 8)
            yield Categoria("Panaderia", 9)
            yield Categoria("Salsas", 10)
            yield Categoria("Conservas", 10)
            yield Categoria("Lacteos", 14)
            yield Categoria("Conservas", 15)
            yield Categoria("Verduras", 15)

    def test_filtrar_por_medida_max(self):
        datos = funciones.filtrar_por_medida(self.generador_producto(1), 0, 500, "gr")
        self.assertIsInstance(datos, filter)
        lista_datos = list(datos)
        producto = Producto(6, "Cebollas", 790, "Pasillo 3", 500, "gr")
        self.assertSequenceEqual(lista_datos, [producto])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_por_medida, ["for", "while"])
        usa_metodo_prohibido(funciones.filtrar_por_medida, ["list", "dict", "set", "tuple"])

    def test_filtrar_por_medida_min(self):
        datos = funciones.filtrar_por_medida(self.generador_producto(2), 1000, 1400, "ml")
        self.assertIsInstance(datos, filter)
        lista_datos = list(datos)
        producto = Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
        self.assertSequenceEqual(lista_datos, [producto])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_por_medida, ["for", "while"])
        usa_metodo_prohibido(funciones.filtrar_por_medida, ["list", "dict", "set", "tuple"])

    def test_filtrar_por_medida_vacio(self):
        datos = funciones.filtrar_por_medida(self.generador_producto(3), 100, 200, "gr")
        self.assertIsInstance(datos, filter)
        lista_datos = list(datos)
        self.assertSequenceEqual(lista_datos, [])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_por_medida, ["for", "while"])
        usa_metodo_prohibido(funciones.filtrar_por_medida, ["list", "dict", "set", "tuple"])

    def test_filtrar_por_unidad(self):
        datos = funciones.filtrar_por_medida(self.generador_producto(4), 0, 1000, "gr")
        self.assertIsInstance(datos, filter)
        lista_datos = list(datos)
        lista_productos = [
            Producto(8, "Jamon", 2990, "Pasillo 4", 200, "gr"),
            Producto(9, "Pan de molde", 1490, "Pasillo 4", 500, "gr"),
            Producto(15, "Aceitunas", 2490, "Pasillo 5", 200, "gr")
        ]
        self.assertSequenceEqual(lista_datos, lista_productos)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_por_medida, ["for", "while"])
        usa_metodo_prohibido(funciones.filtrar_por_medida, ["list", "dict", "set", "tuple"])

    def test_filtrar_por_categoria_1(self):
        productos = self.generador_producto(1)
        categorias = self.generador_categoria(1)
        datos = funciones.filtrar_por_categoria(productos, categorias, "Verduras")

        lista_datos = list(datos)
        resultado_productos = list(self.generador_producto(1))
        self.assertSequenceEqual(lista_datos, resultado_productos)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_por_categoria, ["for", "while"])
        usa_metodo_prohibido(funciones.filtrar_por_categoria, ["list", "dict", "set", "tuple"])

    def test_filtrar_por_categoria_2(self):
        productos = self.generador_producto(2)
        categorias = self.generador_categoria(2)
        datos = funciones.filtrar_por_categoria(productos, categorias, "Aceites")

        lista_datos = list(datos)
        resultado_productos = [Producto(5, "Aceite de oliva", 5990, "Pasillo 5", 500, "ml")]
        self.assertSequenceEqual(lista_datos, resultado_productos)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_por_categoria, ["for", "while"])
        usa_metodo_prohibido(funciones.filtrar_por_categoria, ["list", "dict", "set", "tuple"])

    def test_filtrar_por_categoria_3(self):
        productos = self.generador_producto(4)
        categorias = self.generador_categoria(4)
        datos = funciones.filtrar_por_categoria(productos, categorias, "Conservas")

        lista_datos = list(datos)
        resultado_productos = [
            Producto(10, "Salsa de tomate", 990, "Pasillo 5", 500, "ml"),
            Producto(15, "Aceitunas", 2490, "Pasillo 5", 200, "gr")
        ]
        self.assertSequenceEqual(lista_datos, resultado_productos)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_por_categoria, ["for", "while"])
        usa_metodo_prohibido(funciones.filtrar_por_categoria, ["list", "dict", "set", "tuple"])

    def test_filtrar_por_categoria_vacio(self):
        productos = self.generador_producto(3)
        categorias = self.generador_categoria(3)
        datos = funciones.filtrar_por_categoria(productos, categorias, "No existe")
        self.assertIsInstance(datos, filter)
        
        lista_datos = list(datos)
        self.assertSequenceEqual(lista_datos, [])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_por_categoria, ["for", "while"])
        usa_metodo_prohibido(funciones.filtrar_por_categoria, ["list", "dict", "set", "tuple"])


class TestBonus(unittest.TestCase):

    def generador_producto(self, variacion):
        if variacion == 1:
            yield Producto(6, "Cebollas", 790, "Pasillo 3", 500, "gr")
            yield Producto(7, "Papas", 1490, "Pasillo 3", 1000, "gr")
        elif variacion == 2:
            yield Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
            yield Producto(5, "Aceite de oliva", 5990, "Pasillo 5", 500, "ml")
        elif variacion == 3:
            yield Producto(13, "Fideos", 590, "Pasillo 1", 500, "gr")
            yield Producto(19, "Cafe", 2990, "Pasillo 1", 250, "gr")
            yield Producto(12, "Queso", 3490, "Pasillo 2", 250, "gr")
            yield Producto(3, "Manzanas", 990, "Pasillo 3", 500, "gr")
            yield Producto(4, "Pan integral", 2490, "Pasillo 4", 500, "gr")
        elif variacion == 4:
            yield Producto(14, "Huevos", 1990, "Pasillo 3", 12, "unidades")
            yield Producto(8, "Jamon", 2990, "Pasillo 4", 200, "gr")
            yield Producto(9, "Pan de molde", 1490, "Pasillo 4", 500, "gr")
            yield Producto(10, "Salsa de tomate", 990, "Pasillo 5", 500, "ml")
            yield Producto(15, "Aceitunas", 2490, "Pasillo 5", 200, "gr")
        elif variacion == 5:
            yield Producto(14, "Huevos", 1990, "Pasillo 5", 12, "unidades")
        elif variacion == 6:
            yield Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
            yield Producto(3, "Manzanas", 990, "Pasillo 3", 500, "gr")
            yield Producto(14, "Huevos", 1990, "Pasillo 3", 12, "unidades")
        elif variacion == 7:
            yield Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
            yield Producto(6, "Cebollas", 790, "Pasillo 3", 500, "gr")
            yield Producto(20, "Azucar", 990, "Pasillo 4", 500, "gr")

    def test_agrupar_por_pasillo_1(self):
        productos = self.generador_producto(1)
        datos = funciones.agrupar_por_pasillo(productos)
        self.assertIsInstance(datos, groupby)

        lista_datos = [(x[0], list(x[1])) for x in datos]
        productos = list(self.generador_producto(1))

        self.assertEqual(lista_datos[0][0], "Pasillo 3")
        self.assertSequenceEqual(lista_datos[0][1], productos)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.agrupar_por_pasillo, ["for", "while"])
        usa_metodo_prohibido(funciones.agrupar_por_pasillo, ["list", "dict", "set", "tuple"])
        usa_metodo_esperado(funciones.agrupar_por_pasillo, ["groupby"])

    def test_agrupar_por_pasillo_2(self):
        productos = self.generador_producto(2)
        datos = funciones.agrupar_por_pasillo(productos)
        self.assertIsInstance(datos, groupby)

        lista_datos = [(x[0], list(x[1])) for x in datos]
        productos = list(self.generador_producto(2))

        self.assertEqual(lista_datos[0][0], "Pasillo 2")
        self.assertSequenceEqual(lista_datos[0][1], [productos[0]])
        self.assertEqual(lista_datos[1][0], "Pasillo 5")
        self.assertSequenceEqual(lista_datos[1][1], [productos[1]])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.agrupar_por_pasillo, ["for", "while"])
        usa_metodo_prohibido(funciones.agrupar_por_pasillo, ["list", "dict", "set", "tuple"])
        usa_metodo_esperado(funciones.agrupar_por_pasillo, ["groupby"])

    def test_agrupar_por_pasillo_3(self):
        productos = self.generador_producto(3)
        datos = funciones.agrupar_por_pasillo(productos)
        self.assertIsInstance(datos, groupby)

        lista_datos = [(x[0], list(x[1])) for x in datos]
        productos = list(self.generador_producto(3))

        self.assertEqual(lista_datos[0][0], "Pasillo 1")
        self.assertSequenceEqual(lista_datos[0][1], productos[0:2])
        self.assertEqual(lista_datos[1][0], "Pasillo 2")
        self.assertSequenceEqual(lista_datos[1][1], productos[2:3])
        self.assertEqual(lista_datos[2][0], "Pasillo 3")
        self.assertSequenceEqual(lista_datos[2][1], productos[3:4])
        self.assertEqual(lista_datos[3][0], "Pasillo 4")
        self.assertSequenceEqual(lista_datos[3][1], productos[4:])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.agrupar_por_pasillo, ["for", "while"])
        usa_metodo_prohibido(funciones.agrupar_por_pasillo, ["list", "dict", "set", "tuple"])
        usa_metodo_esperado(funciones.agrupar_por_pasillo, ["groupby"])

    def test_agrupar_por_pasillo_4(self):
        productos = self.generador_producto(4)
        datos = funciones.agrupar_por_pasillo(productos)
        self.assertIsInstance(datos, groupby)

        lista_datos = [(x[0], list(x[1])) for x in datos]
        productos = list(self.generador_producto(4))

        self.assertEqual(lista_datos[0][0], "Pasillo 3")
        self.assertSequenceEqual(lista_datos[0][1], productos[0:1])
        self.assertEqual(lista_datos[1][0], "Pasillo 4")
        self.assertSequenceEqual(lista_datos[1][1], productos[1:3])
        self.assertEqual(lista_datos[2][0], "Pasillo 5")
        self.assertSequenceEqual(lista_datos[2][1], productos[3:])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.agrupar_por_pasillo, ["for", "while"])
        usa_metodo_prohibido(funciones.agrupar_por_pasillo, ["list", "dict", "set", "tuple"])
        usa_metodo_esperado(funciones.agrupar_por_pasillo, ["groupby"])

    def test_agrupar_por_pasillo_5(self):
        productos = self.generador_producto(5)
        datos = funciones.agrupar_por_pasillo(productos)
        self.assertIsInstance(datos, groupby)

        lista_datos = [(x[0], list(x[1])) for x in datos]
        productos = list(self.generador_producto(5))

        self.assertEqual(lista_datos[0][0], "Pasillo 5")
        self.assertSequenceEqual(lista_datos[0][1], productos[0:1])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.agrupar_por_pasillo, ["for", "while"])
        usa_metodo_prohibido(funciones.agrupar_por_pasillo, ["list", "dict", "set", "tuple"])
        usa_metodo_esperado(funciones.agrupar_por_pasillo, ["groupby"])

    def test_agrupar_por_pasillo_6(self):
        productos = self.generador_producto(6)
        datos = funciones.agrupar_por_pasillo(productos)
        self.assertIsInstance(datos, groupby)

        lista_datos = [(x[0], list(x[1])) for x in datos]
        productos = list(self.generador_producto(6))

        self.assertEqual(lista_datos[0][0], "Pasillo 2")
        self.assertSequenceEqual(lista_datos[0][1], productos[0:1])
        self.assertEqual(lista_datos[1][0], "Pasillo 3")
        self.assertSequenceEqual(lista_datos[1][1], productos[1:])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.agrupar_por_pasillo, ["for", "while"])
        usa_metodo_prohibido(funciones.agrupar_por_pasillo, ["list", "dict", "set", "tuple"])
        usa_metodo_esperado(funciones.agrupar_por_pasillo, ["groupby"])

    def test_agrupar_por_pasillo_7(self):
        productos = self.generador_producto(7)
        datos = funciones.agrupar_por_pasillo(productos)
        self.assertIsInstance(datos, groupby)

        lista_datos = [(x[0], list(x[1])) for x in datos]
        productos = list(self.generador_producto(7))

        self.assertEqual(lista_datos[0][0], "Pasillo 2")
        self.assertSequenceEqual(lista_datos[0][1], productos[0:1])
        self.assertEqual(lista_datos[1][0], "Pasillo 3")
        self.assertSequenceEqual(lista_datos[1][1], productos[1:2])
        self.assertEqual(lista_datos[2][0], "Pasillo 4")
        self.assertSequenceEqual(lista_datos[2][1], productos[2:])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.agrupar_por_pasillo, ["for", "while"])
        usa_metodo_prohibido(funciones.agrupar_por_pasillo, ["list", "dict", "set", "tuple"])
        usa_metodo_esperado(funciones.agrupar_por_pasillo, ["groupby"])

    def test_agrupar_por_pasillo_vacio(self):
        productos = self.generador_producto(0)
        datos = funciones.agrupar_por_pasillo(productos)
        self.assertIsInstance(datos, groupby)

        lista_datos = [(x[0], list(x[1])) for x in datos]
        productos = list(self.generador_producto(5))

        self.assertEqual(lista_datos, [])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.agrupar_por_pasillo, ["for", "while"])
        usa_metodo_prohibido(funciones.agrupar_por_pasillo, ["list", "dict", "set", "tuple"])
        usa_metodo_esperado(funciones.agrupar_por_pasillo, ["groupby"])


class TestIterables(unittest.TestCase):

    def generador_producto(self, variacion):
        if variacion == 1:
            yield Producto(14, "Huevos", 1990, "Pasillo 3", 12, "unidades")
        elif variacion == 2:
            yield Producto(6, "Cebollas", 790, "Pasillo 3", 500, "gr")
            yield Producto(7, "Papas", 1490, "Pasillo 3", 1000, "gr")
            yield Producto(5, "Aceite de oliva", 5990, "Pasillo 5", 500, "ml")
            yield Producto(2, "Leche", 1190, "Pasillo 2", 1000, "ml")
        elif variacion == 3:
            yield Producto(14, "Huevos", 1990, "Pasillo 3", 12, "unidades")
            yield Producto(8, "Jamon", 2990, "Pasillo 4", 200, "gr")
            yield Producto(9, "Pan de molde", 1490, "Pasillo 4", 500, "gr")
            yield Producto(10, "Salsa de tomate", 990, "Pasillo 5", 500, "ml")
            yield Producto(15, "Aceitunas", 2490, "Pasillo 5", 200, "gr")
        elif variacion == 4:
            yield Producto(14, "Huevos", 1990, "Pasillo 3", 12, "unidades")
            yield Producto(10, "Salsa de tomate", 990, "Pasillo 5", 500, "ml")
            yield Producto(5, "Aceite de oliva", 5990, "Pasillo 5", 500, "ml")

    def test_Carrito_iter(self):
        productos = list(self.generador_producto(1))
        iterador = iter(funciones.Carrito(productos))
        self.assertIsInstance(iterador, funciones.IteradorCarrito)
        self.assertSequenceEqual(iterador.productos_iterable, productos)

        # No usa for ni while
        usa_comando_prohibido(funciones.Carrito, ["for", "while"])

    def test_IteradorCarrito_iter(self):
        productos = list(self.generador_producto(1))
        iterador = iter(funciones.IteradorCarrito(productos))
        self.assertIsInstance(iterador, funciones.IteradorCarrito)
        self.assertSequenceEqual(iterador.productos_iterable, productos)

        # No usa for ni while
        usa_comando_prohibido(funciones.IteradorCarrito, ["for", "while"])

    def test_IteradorCarrito_StopIteration(self):
        carrito = funciones.IteradorCarrito([])
        self.assertRaises(StopIteration, next, carrito)

        # No usa for ni while
        usa_comando_prohibido(funciones.IteradorCarrito, ["for", "while"])

    def test_IteradorCarrito_next_1(self):
        productos = list(self.generador_producto(1))
        carrito = funciones.IteradorCarrito(productos)
        producto_next = next(carrito)
        self.assertSequenceEqual(producto_next, productos[0])

        # No usa for ni while
        usa_comando_prohibido(funciones.IteradorCarrito, ["for", "while"])

    def test_IteradorCarrito_next_2(self):
        productos = list(self.generador_producto(2))
        productos_ordenados = sorted(productos, key=lambda x: x.precio)
        carrito = funciones.IteradorCarrito(productos)

        for producto_ordenado in productos_ordenados:
            producto_next = next(carrito)
            self.assertSequenceEqual(producto_next, producto_ordenado)

        self.assertRaises(StopIteration, next, carrito)

        # No usa for ni while
        usa_comando_prohibido(funciones.IteradorCarrito, ["for", "while"])

    def test_IteradorCarrito_next_3(self):
        productos = list(self.generador_producto(3))
        productos_ordenados = sorted(productos, key=lambda x: x.precio)
        carrito = funciones.IteradorCarrito(productos)

        for producto_ordenado in productos_ordenados:
            producto_next = next(carrito)
            self.assertSequenceEqual(producto_next, producto_ordenado)

        self.assertRaises(StopIteration, next, carrito)

        # No usa for ni while
        usa_comando_prohibido(funciones.IteradorCarrito, ["for", "while"])

    def test_IteradorCarrito_next_4(self):
        productos = list(self.generador_producto(4))
        productos_ordenados = sorted(productos, key=lambda x: x.precio)
        carrito = funciones.IteradorCarrito(productos)

        for producto_ordenado in productos_ordenados:
            producto_next = next(carrito)
            self.assertSequenceEqual(producto_next, producto_ordenado)

        self.assertRaises(StopIteration, next, carrito)

        # No usa for ni while
        usa_comando_prohibido(funciones.IteradorCarrito, ["for", "while"])


if __name__ == '__main__':
    unittest.main(verbosity=1)
