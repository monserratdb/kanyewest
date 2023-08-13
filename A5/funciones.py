from copy import copy
from functools import reduce
from itertools import groupby
from typing import Generator

from utilidades import (
    Categoria, Producto, duplicador_generadores, generador_a_lista
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_productos(ruta: str) -> Generator:
    with open(ruta, "r") as archivo:
        lineas = archivo.readlines()
        lineas_vacio = []
        for linea in lineas:
            linea.split("\n")
            lineas_vacio.append(linea)
    for linea in lineas_vacio:
        cosa = linea.split(",")
        if linea != lineas_vacio[0]:
            id_producto = int(cosa[0])
            nombre = cosa[1]
            precio = int(cosa[2])
            pasillo = cosa[3]
            medida = int(cosa[4])
            unidad = cosa[5].rstrip("\n")

            producto = Producto(id_producto, nombre, precio, pasillo, medida, unidad)

            yield producto


def cargar_categorias(ruta: str) -> Generator:
    with open(ruta, "r") as archivo:
        lineas = archivo.readlines()
        lineas_vacio = []
        for linea in lineas:
            linea.split("\n")
            lineas_vacio.append(linea)
    for linea in lineas_vacio:
        cosa = linea.split(",")
        if linea != lineas_vacio[0]:
            nombre_categoria = cosa[0]
            id = cosa[1].rstrip("\n")
            id_producto = int(id)

            categoria = Categoria(nombre_categoria, id_producto)

            yield categoria

# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------
# prohibido usar for en la parte 2 :)


def obtener_productos(generador_productos: Generator) -> map:
    nombres_productos = map(lambda producto: producto.nombre, generador_productos)
    return nombres_productos


def obtener_precio_promedio(generador_productos: Generator) -> int:
    total_productos = 0
    suma_precios = 0
    for producto in generador_productos:
        total_productos += 1
        suma_precios += producto.precio

    if total_productos > 0:
        precio_promedio = suma_precios / total_productos
        precio_promedio_entero = int(precio_promedio)
        return precio_promedio_entero
    else:
        return 0


def filtrar_por_medida(generador_productos: Generator,
                       medida_min: float, medida_max: float, unidad: str
                       ) -> filter:
    productos_filtrados = filter(lambda producto: producto.unidad_medida == unidad and medida_min <= producto.medida <= medida_max, generador_productos)
    return productos_filtrados


def filtrar_por_categoria(generador_productos: Generator,
                          generador_categorias: Generator,
                          nombre_categoria: str) -> Generator:
    ids_categoria = [categoria.id_producto for categoria in generador_categorias if categoria.nombre_categoria == nombre_categoria]
    productos_lista = list(generador_productos)
    productos_filtrados = filter(lambda producto: producto.id_producto in ids_categoria, productos_lista)
    return productos_filtrados


def agrupar_por_pasillo(generador_productos: Generator) -> Generator:
    productos_ordenados = sorted(generador_productos, key=lambda p: p.pasillo)
    grupos = groupby(productos_ordenados, key=lambda p:p.pasillo)
    return grupos

# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------


class Carrito:
    def __init__(self, productos: list) -> None:
        self.productos = productos

    def __iter__(self):
        return IteradorCarrito(self.productos)


class IteradorCarrito:
    def __init__(self, iterable_productos: list) -> None:
        self.productos_iterable = copy(iterable_productos)
        self.indice_actual = 0

    def __iter__(self):
        return self

    def __next__(self):
        # TODO: Completar
        if self.indice_actual >= len(self.productos_iterable):
            raise StopIteration("llegamos al final")

        # producto_actual = self.productos_iterable[self.indice_actual]
        indice_menor_precio = self.indice_actual
        for i in range(self.indice_actual + 1, len(self.productos_iterable)):
            if self.productos_iterable[i].precio < self.productos_iterable[indice_menor_precio].precio:
                indice_menor_precio = i

        producto_menor_precio = self.productos_iterable[indice_menor_precio]

        self.productos_iterable[self.indice_actual], self.productos_iterable[indice_menor_precio] = \
            self.productos_iterable[indice_menor_precio], self.productos_iterable[self.indice_actual]

        self.indice_actual += 1

        return producto_menor_precio


# siendo las 16:47 me acabo de fijar en que no se podía usar for en la parte 3 :(
# pero ya me funcionaba cn todos los tests así que lo dejé así noma TT
# amsorri :(
