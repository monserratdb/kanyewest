from random import random, randint
from threading import Event, Lock, Thread
from time import sleep

# Completar
class Corredor(Thread): 

    TIEMPO_ESPERA = 0.5  # Tiempo entre avances del corredor
    PORCENTAJE_MIN = 70  # Mínimo avance del corredor
    PORCENTAJE_MAX = 100  # Máximo avance del corredor
    PROBABILIDAD_ROBAR = 0.3  # Probabilidad de robar la tortuga

    def __init__(self, nombre: str, tortuga: Lock, 
                 senal_inicio: Event, senal_fin: Event,
                 lock_verificar_tortuga: Lock) -> None:
        super().__init__()
        self.name = nombre
        # Referencias al lock de la tortuga y las señales propias de la carrera
        self.lock_tortuga = tortuga
        self.senal_inicio = senal_inicio
        self.senal_fin = senal_fin
        self.lock_carrera = lock_verificar_tortuga
        self.lock_verificar_tortuga = lock_verificar_tortuga

        self.tiene_tortuga = False  # Booleano que indica si el corredor lleva la tortuga
        self.__posicion = 0
        self.__velocidad = 10
        self.__correr = True

        # Completar
        self.daemon = True #pq daemon es q termine cndo todos hayan terminado
        #carrera termina cndo el último ken terminar, temrina la carrera

    @property
    def posicion(self) -> float:
        return self.__posicion

    @posicion.setter
    def posicion(self, nueva_posicion: float) -> None:
        # La posicion no puede aumentar más allá de la meta
        self.__posicion = min(nueva_posicion, 100)

    @property
    def velocidad(self) -> float:
        # El corredor reduce su velocidad si lleva la tortuga
        return self.__velocidad if not self.tiene_tortuga else self.__velocidad * 0.5

    def asignar_rival(self, funcion_notificacion) -> None:
        self.notificar_robo = funcion_notificacion

    def ser_notificado_por_robo(self) -> None:
        self.perder_tortuga()

    def avanzar(self) -> None:
        # Completar
        porcentaje = random.randint(self.PORCENTAJE_MIN, self.PORCENTAJE_MAX)
        aumento = porcentaje/100
        self.posicion += aumento*self.velocidad 
        # Luego de avanzar impime su posición y duerme
        print(f'{self.name}: Avancé a {self.posicion:.2f}')
        sleep(self.TIEMPO_ESPERA)

    def intentar_capturar_tortuga(self) -> None:
        # Completar
        #False le dice q debe intentar una vez y dsp seguir su ejecución
        if self.lock_tortuga.acquire(False):
            self.tiene_tortuga = True
            print(f'{self.name}: ¡Capturé la tortuga!')
        # Si logra la captura, imprime un mensaje
            

    def perder_tortuga(self) -> None:
        # Completar
        self.tiene_tortuga = False
        self.lock_tortuga.release()
        print(f'{self.name}: Perdí la tortuga :(')
    
    def robar_tortuga(self) -> bool:
        # PROBABILIDAD_ROBAR de robar la tortuga
        if random() < self.PROBABILIDAD_ROBAR:
            # Completar
            self.lock_tortuga.acquire()
            self.tiene_tortuga = True
            print(f'{self.name}: ¡Robé la tortuga!') 
            self.ser_notificado_por_robo() #notifico al rival ¿¿
            return True
        else:
            return False
            
    def correr_primera_mitad(self):
        while self.posicion < 50:
            # Completar
            self.__correr = True #ya es True x defecto so idk if its necessary to put
            #this line but anyways
            #mientras el corredor este a menos de 50mt, se dedica  avanzar
            pass

    def correr_segunda_mitad(self) -> bool:
        while self.__correr:
            # Completar
            #acquire(True) pq debe esperar si es que el lock está tomado
            while self.lock_carrera.acquire(True): #no toi 100% segura d esa pt
                if self.senal_fin == True:
                    return False
                elif self.posicion >= 100 and self.tiene_tortuga == True:
                    print("La carrera terminó")
                    #self.senal_fin = True
                    self.lock_tortuga.release()
                    return True
                elif self.tiene_tortuga == False:
                    self.robar_tortuga()
        #dsp de verificar todo, sigo corriendo
        self.__correr = True #sigo avanzando

# 2. Luego, debe correr la primera mitad de la carrera.
    def run(self) -> None:
        # Completar
        self.start()
        senal = self.senal_inicio.set()
        self.wait(senal)
        self.correr_primera_mitad
        self.intentar_capturar_tortuga
        self.correr_segunda_mitad

# Completar
class Carrera(Thread):
    def __init__(self, corredor_1: Corredor, corredor_2: Corredor, 
                 senal_inicio: Event, senal_fin: Event) -> None:
        super().__init__()
        # Referencias a las señales propias de la carrera
        self.senal_inicio = senal_inicio
        self.senal_fin = senal_fin

        # Guarda los corredores y los asigna como rivales
        self.corredor_1 = corredor_1
        self.corredor_2 = corredor_2
        corredor_1.asignar_rival(corredor_2.ser_notificado_por_robo)
        corredor_2.asignar_rival(corredor_1.ser_notificado_por_robo)

        # Completar
        self.daemon = False #¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿
    
    # Completar
    def empezar(self) -> str:
        #encargado de inciar el hilo de ejecución de la carrera
        while self.run.start():
            self.start()
        return self.name #nombre del jugador que tga la tortuga

    # Completar
    def run(self) -> None:
        #inicia threads de ambos corredores
        self.corredor_1.start()
        self.corredor_2.start()
        self.senal_inicio.set()
        print("La carrera ha iniciado")
        finsignal = self.senal_fin.set()
        self.wait(finsignal)
        #espera hasta q algún jugador llegue al fin


if __name__ == '__main__':
    # Instancia una tortuga y las señales
    tortuga = Lock()
    lock_verificar_tortuga = Lock()
    senal_inicio = Event()
    senal_fin = Event()

    # Instancia los corredores y la carrera
    j1 = Corredor('Juan', tortuga, senal_inicio, senal_fin, lock_verificar_tortuga)
    j2 = Corredor('Pepe', tortuga, senal_inicio, senal_fin, lock_verificar_tortuga)
    carrera = Carrera(j1, j2, senal_inicio, senal_fin)

    # Inicia la carrera y pausa el main thread hasta que termine
    ganador = carrera.empezar()
    
    print(f'{ganador} ha ganado la carrera!!')

# usamos super().__init__()
# hay q definir un run tb
# run(self):
#     self.trabajar

# al final 
# t1= Minero("John)
# tw = Minero("lol)

# t1.start()
# t2.start()