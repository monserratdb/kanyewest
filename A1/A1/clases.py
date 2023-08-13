from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, peso, nombre, *arg, **kwargs) -> None:
        self.peso = int(peso)
        self.nombre = str(nombre)
        self.__energia = 100 #es privado
        self.identificador = 0 #parte en 0
        #rut del animal. para setearlo se fija cmo el valor actual de la variable
        #de clase Animal.identificador, luego se le suma 1 a la misma variable 

    @abstractmethod
    def desplazarse(self) -> None:
        #metodo abstracto

     @property #no se por qué cuando lo tenía en el mismo espacio de identación que "@abstractmethod" me tiraba error
     def energia(self) -> int:
        return self.__energia
    #getter retorna el valor del atributo privado self.energia
    
     @energia.setter
     def energia(self, valor):
        if valor < 0:
            self.__energia = 0
        #setter se encarga de q self.energia no sea menor a 0

class Terrestre(Animal):
    #hereda de Animal
    #clase abstracta ????
    def __init__(self, cantidad_patas, *args, **kwargs) -> None:
        #además de llamar al método de la clase padre (Animal)
        super().__init__(**kwargs) #llama al metodo de la clase padre ¿¿
        self.cantidad_patas = int(cantidad_patas)
    
    def identificador(self):
        super().identificador

    def energia(self):
        super().__energia

    def energia_gastada_por_desplazamiento(self) -> int:
        energia_requerida = self.peso * 5
        return energia_requerida
    
    def desplazarse(self) -> str:
        energia_gastada = self.energia_gastada_por_desplazamiento()
        energia_actual = self.energia  #privado de Animal
        energia_final = energia_actual - energia_gastada
        #energia_actual es un metodo, no se admite metodo - int
        return "caminando..."

class Acuatico(Animal):
    #hereda de Animal
    #clase abstracta
    def energia_gastada_por_desplazamiento(self) -> int:
        energia_requerida = self.peso * 2
        return energia_requerida
    
    def desplazarse(self) -> str:
        energia_actual = self.energia #privado de Animal
        energia_gastada = self.energia_gastada_por_desplazamiento() 
        energia_final = energia_actual - energia_gastada
        #energia_actual es un metodo, no se admite metodo - int
        return "nadando..."

class Perro(Terrestre):
    #hereda de terrestre
    def __init__(self, raza, *args, **kwargs) -> None:
        self.raza = raza #esto es setear la raza?
        self.cantidad_patas = 4
        super().__init__(self.cantidad_patas,**kwargs) #llama al metodo de la clase padre

    def ladrar(self) -> str:
        return "guau guau"

class Pez(Acuatico):
    #hereda de acuatico
    def __init__(self, color, *args, **kwargs) -> None: 
        super().__init__(**kwargs)  
        self.color = color #setea color?
    
    def nadar(self) -> str:
        return "moviendo aleta"

class Ornitorrinco(Terrestre, Acuatico):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def desplazarse(self) -> str:
        #no supe cómo hacerlo en verdad 
        #energia_actuatico = blabla
        #energia_terrestre = blabla
        #gasto_energia = (energia_actuatico + energia_terrestre)//2 
        #return energia_acuatico + energia_terrestre
        pass

if __name__ == '__main__':
    perro = Perro(nombre='Pongo', raza='Dalmata', peso=3)
    pez = Pez(nombre='Nemo', color='rojo', peso=1)
    ornitorrinco = Ornitorrinco(nombre='Perry', peso=2, cantidad_patas=6)

    perro.desplazarse()
    pez.desplazarse()
    ornitorrinco.desplazarse()