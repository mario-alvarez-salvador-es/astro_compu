# classes
import numpy as np
class astro():
    "Objeto que representa las magnitudes fisicas de un astro"
    def __init__(self, name, m=0, r=np.array([0,0]), v=np.array([0,0]), movility=True):
        "Iniciamos masa possicion y velocidad y si se puede mover o no"
        self.name = name
        self.m = m
        self.r = r
        self.v = v
        self.movility = movility

    def set_mass(self, m):
        "Cambiamos masa"
        self.m = m

    def set_position(self, r):
        "Cambiamos posicion"
        self.r = r

    def set_speed(self, v):
        "Cambiamos velocidad"
        self.v = v

    def __str__(self):
        string = f"Astro: {self.name}\n"
        string += f"Masa = {self.m} masas solares\n"
        string += f"Posicion = {self.r} UA\n"
        string += f"Velocidad = {self.v} UA/año\n"
        string += f"Movil? : {self.movility}\n"
        return string

class astro_system():
    "Establece el sistema de particulas y puede simularse"
    def __init__(self, name=''):
        "Iniciamos con un nombre"
        self.name = name
        self.astros = list()
        self.t = 0
    
    def add_astros(self, *astros):
        "Añadimos los astros que queramos"
        self.astros.append(*astros)
        self.mass_astros = filter(lambda astro: astro.m > 0, self.astros)

    def calculate_g(self, r):
        "Calculamos g (aceleracion de la gravedad en ese punto)"
        return sum 
        (
            np.array
            (
            [astro.m/np.dot(astro.r, r) for astro in self.mass_astros]
            )
        ) *-4*np.pi*np.pi

    def rk4(self, t, r, v, dt):
        "Runge kutta 4"
        pass

    def move_astro(self, astro, dt):
        "Mover un astro segun gravedad"
        pass

    def move_astros(self, dt):
        "Mover todos los astros segun gravedad"
        pass

    def simulate_system(self, t, dt):
        "simula el sistema durante un tiempo total t y en tramos separados dt"
        pass