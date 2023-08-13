from collections import defaultdict, deque


class Jugador: #nodo del grafo
    def __init__(self, nombre: str, velocidad: int) -> None:
        self.nombre = nombre
        self.velocidad = velocidad
    
    def __repr__(self) -> None:
        return f'Jugador: {self.nombre}, Velocidad: {self.velocidad}'


class Equipo: #grafo
    def __init__(self) -> None:
        self.jugadores = dict()
        self.dict_adyacencia = defaultdict(set)
    
    def agregar_jugador(self, id_jugador: int, jugador: Jugador) -> bool:
        '''Agrega un nuevo jugador al equipo.'''
        # # Completar
        # mineeeeeeeeeeeeeee
        # if id_jugador not in self.jugadores: #tb podría ser jugador
        #     self.jugadores[jugador] = id_jugador
        #     self.dict_adyacencia[id_jugador] = set() #no tiene vecinos inicialmente
        #     return True
        # else:
        #     return False
        if id_jugador in self.jugadores:
            return False
        self.jugadores[id_jugador] = jugador
        return True

    def agregar_vecinos(self, id_jugador: int, vecinos: list[int]) -> int:
        '''Agrega una lista de vecinos a un jugador.'''
        # Completar
        # {Jugador: Alonso, Velocidad: 1: 0}
        # mineeeeeeeeeeeeeeeeeeeee
        # if id_jugador not in self.jugadores:
        #     return -1
        # else:
        #     for i in vecinos:
        #         if i not in self.dict_adyacencia:
        #             self.dict_adyacencia[id_jugador].add(i)
        #             i += 1
        #     return i
        if id_jugador not in self.dict_adyacencia:
            return -1

        nuevos_vecinos = 0
        for vecino in vecinos:
            if vecino not in self.dict_adyacencia[id_jugador]:
                self.dict_adyacencia[id_jugador].add(vecino)
                nuevos_vecinos += 1

        return nuevos_vecinos
        
    def mejor_amigo(self, id_jugador: int) -> Jugador:
        '''Retorna al vecino con la velocidad más similar.'''
        # Completar {Jugador: Alonso, Velocidad: 1: 0} {jugador:nombre, vel: vel: id}
        # mineeeeeeeeeeeeeeeeee
        # id_vecinos = self.dict_adyacencia[id_jugador] 
        # diferencias = []
        # for i in id_vecinos:
        #     self.jugadores[i] #es el jugador en forma{Jugador: Alonso, Velocidad: 1: 0}
        #     velocidad = self.jugadores[i].velocidad
        #     dif = self.jugadores[id_jugador].velocidad - velocidad
        #     diferencias.append(dif)
        # if len(diferencias) > 1:
        #     vel_similar = min(diferencias)
        # for i in id_vecinos:
        #     self.jugadores[i] #es el jugador en forma{Jugador: Alonso, Velocidad: 1: 0}
        #     velocidad = self.jugadores[i].velocidad
        #     if velocidad == vel_similar:
        #         return self.jugadores[i].nombre
        if id_jugador not in self.dict_adyacencia:
            return None

        jugador_actual = self.jugadores[id_jugador]
        mejor_amigo = None
        menor_diferencia = float('inf')

        for vecino in self.dict_adyacencia[id_jugador]:
            diferencia = abs(jugador_actual.velocidad - self.jugadores[vecino].velocidad)
            if diferencia < menor_diferencia:
                mejor_amigo = self.jugadores[vecino]
                menor_diferencia = diferencia

        return mejor_amigo

    def peor_compañero(self, id_jugador: int) -> Jugador:
        '''Retorna al compañero de equipo con la mayor diferencia de velocidad.'''
        # mineeeeeeeeeeeeeee
        # id_vecinos = self.dict_adyacencia[id_jugador] 
        # diferencias = []
        # print(self.jugadores[id_jugador].velocidad)
        # for id in id_vecinos:
        #     velocidad = self.jugadores[id].velocidad
        #     dif = self.jugadores[id_jugador].velocidad - velocidad
        #     diferencias.append(dif)
        # for i in id_vecinos:
        #     self.jugadores[i] #es el jugador en forma{Jugador: Alonso, Velocidad: 1: 0}
        #     velocidad = self.jugadores[i].velocidad
        #     if len(diferencias) > 1:
        #         vel_mayor = max(diferencias)
        #         if velocidad == vel_mayor:
        #             return self.jugadores[i].nombre
        jugador_actual = self.jugadores[id_jugador]
        peor_compañero = None
        mayor_diferencia = 0

        for jugador_id, jugador in self.jugadores.items():
            if jugador_id != id_jugador:
                diferencia = abs(jugador.velocidad - jugador_actual.velocidad)
                if diferencia > mayor_diferencia:
                    peor_compañero = jugador
                    mayor_diferencia = diferencia

        return peor_compañero

    def peor_conocido(self, id_jugador: int) -> Jugador:
        '''Retorna al amigo con la mayor diferencia de velocidad.'''
        # Completar
        #son amigos si id_jugador le tira una arista al otro
        # mineeeeeeeeeeeeeeeeeee
        # id_vecinos = self.dict_adyacencia[id_jugador] 
        # diferencias = []
        # print(self.jugadores[id_jugador].velocidad)
        # for id in id_vecinos:
        #     velocidad = self.jugadores[id].velocidad
        #     dif = self.jugadores[id_jugador].velocidad - velocidad
        #     diferencias.append(dif)
        # for i in id_vecinos:
        #     self.jugadores[i] #es el jugador en forma{Jugador: Alonso, Velocidad: 1: 0}
        #     velocidad = self.jugadores[i].velocidad
        #     if len(diferencias) > 1:
        #         vel_mayor = max(diferencias)
        #         if velocidad == vel_mayor:
        #             return self.jugadores[i].nombre
        jugador_actual = self.jugadores[id_jugador]
        peor_conocido = None
        mayor_diferencia = 0

        visitados = set()
        visitados.add(id_jugador)

        queue = deque()
        queue.append(id_jugador)

        while queue:
            jugador_id = queue.popleft()

            for vecino in self.dict_adyacencia[jugador_id]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    diferencia = abs(self.jugadores[vecino].velocidad - jugador_actual.velocidad)
                    if diferencia > mayor_diferencia:
                        peor_conocido = self.jugadores[vecino]
                        mayor_diferencia = diferencia
                    queue.append(vecino)

        return peor_conocido
    
    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        '''Retorna el tamaño del camino más corto entre los jugadores.'''
        # Completar
        # mineeeeeeeeeeeeeee
        # if id_jugador_1 in self.dict_adyacencia[id_jugador_2]:

        #     return 0
        # else:
        #     return -1
        if id_jugador_1 == id_jugador_2:
            return 0

        visitados = set()
        visitados.add(id_jugador_1)

        queue = deque()
        queue.append((id_jugador_1, 0))

        while queue:
            jugador_id, distancia_actual = queue.popleft()

            for vecino in self.dict_adyacencia[jugador_id]:
                if vecino == id_jugador_2:
                    return distancia_actual + 1

                if vecino not in visitados:
                    visitados.add(vecino)
                    queue.append((vecino, distancia_actual + 1))

        return -1

if __name__ == '__main__':
    equipo = Equipo()
    jugadores = {
        0: Jugador('Alonso', 1),
        1: Jugador('Alba', 3),
        2: Jugador('Alicia', 6),
        3: Jugador('Alex', 10)
    }
    adyacencia = {
        0: [1],
        1: [0, 2],
        2: [1],
    }
    for idj, jugador in jugadores.items():
        equipo.agregar_jugador(id_jugador=idj, jugador=jugador)
    for idj, vecinos in adyacencia.items():
        equipo.agregar_vecinos(id_jugador=idj, vecinos=vecinos)
    
    print(f'El mejor amigo de Alba es {equipo.mejor_amigo(1)}') 
    print(f'El peor compañero de Alonso es {equipo.peor_compañero(0)}')
    print(f'El peor amigo de Alicia es {equipo.peor_compañero(2)}')
    print(f'La distancia entre Alicia y Alonso es {equipo.distancia(2, 0)}')
    print(f'La distancia entre Alba y Alex es {equipo.distancia(1, 3)}')
    