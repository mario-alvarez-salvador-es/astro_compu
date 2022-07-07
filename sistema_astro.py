# classes
import numpy as np
class astro():
    "Objeto que representa las magnitudes fisicas de un astro"
    def __init__(self, name, m=0., r=np.array([0.,0.]), v=np.array([0.,0.]), movility=True):
        "Iniciamos masa possicion y velocidad y si se puede mover o no"
        self.name = str(name)
        self.m = float(m)
        self.r = r.astype(float)
        self.v = v.astype(float)
        self.movility = bool(movility)
        self.history = {'t': [0], 'r': [self.r], 'v': [self.v]}

    def set_mass(self, m):
        "Cambiamos masa"
        self.m = m

    def set_position(self, r):
        "Cambiamos posicion"
        self.r = np.array(r).astype(float)
        self.history['r'] = [self.r]

    def set_speed(self, v):
        "Cambiamos velocidad"
        self.v = np.array(v).astype(float)
        self.history['v'] = [self.v]

    def update_position(self, r):
        self.r = r
        self.history['r'].append(r)

    def update_speed(self, v):
        self.v = v
        self.history['v'].append(v)

    def update_time(self, t):
        self.history['t'].append(t)

    def __str__(self):
        string = f"Astro: {self.name}\n"
        string += f"Masa = {self.m} masas solares\n"
        string += f"Posicion = {self.r} UA\n"
        string += f"Velocidad = {self.v} UA/año\n"
        string += f"Movil? : {self.movility}\n"
        return string

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
class astro_system():
    "Establece el sistema de particulas y puede simularse"
    def __init__(self, name=''):
        "Iniciamos con un nombre"
        self.name = name
        self.astros = list()
        self.t = 0.
    
    def add_astros(self, *astros):
        "Añadimos los astros que queramos"
        self.astros += astros
        self.mass_astros = list( filter(lambda astro: astro.m > 0, self.astros) )

    def calculate_g(self, r, astro_recieved):
        "Calculamos g (aceleracion de la gravedad en ese punto)"
        total_g = np.zeros(shape = self.astros[0].r.shape)
        for astro in self.mass_astros:
            if astro_recieved.name == astro.name: # no puedes calcular la gravedad que ejerce sobre si mismo
                continue
            r_ij = astro.r-r # vector del punto al astro -urij
            # total_g +=  astro.m*r_ij/np.dot(r_ij, r_ij)**(3/2)
            r = np.sqrt(np.dot(r_ij, r_ij))
            total_g += astro.m * r_ij/r**3
        return 4*np.pi*np.pi*total_g

    def move_astro_rk4(self, astro, dt):
        # k1 = dt * astro.v
        # l1 = dt * self.calculate_g(astro.r, astro)
        # k2 = dt * (astro.v+.5*l1)
        # l2 = dt * self.calculate_g(astro.r+0.5*k1, astro)
        # k3 = dt * dt*(astro.v + 0.5*l2)
        # l3 = dt * self.calculate_g(astro.r+0.5*k2, astro)
        # k4 = dt *(astro.v+l3)
        # l4 = dt * self.calculate_g(astro.r+k3, astro)

        # self.t += dt
        # astro.update_speed(astro.v + 1/6*(l1+2*l2+2*l3+l4))
        # astro.update_position(astro.r + 1/6*(k1+2*k2+2*k3+k4))
        # astro.update_time(self.t)

        k1=dt*astro.v
        l1=dt*self.calculate_g(astro.r, astro)
        k2=dt*(astro.v+l1/2)
        l2=dt*self.calculate_g(astro.r+k1/2, astro)
        k3=dt*(astro.v+l2/2)
        l3=dt*self.calculate_g(astro.r+k2/2, astro)
        k4=dt*(astro.v+l3)
        l4=dt*self.calculate_g(astro.r+k3, astro)
        # x+=(k1+2*k2+2*k3+k4)/6;
        # v+=(l1+2*l2+2*l3+l4)/6;
        self.t += dt
        astro.update_speed(astro.v + (l1+2*l2+2*l3+l4)/6)
        astro.update_position(astro.r + (k1+2*k2+2*k3+k4)/6)
        astro.update_time(self.t)
    
    def move_astros_rk4(self, dt):
        "Mueve los astros un periodo de tiempo dt rk4 mode"
        for astro in self.astros:
            if astro.movility:
                self.move_astro_rk4(astro, dt)

    def move_astro(self, astro, dt):
        "Mover un astro segun gravedad"
        v = astro.v + self.calculate_g(astro.r, astro) * dt
        r = astro.r + astro.v * dt
        self.t = self.t + dt

        astro.update_speed(v)
        astro.update_position(r)
        astro.update_time(self.t)

    def move_astros(self, dt):
        "Mueve los astros un periodo de tiempo dt"
        for astro in self.astros:
            if astro.movility:
                self.move_astro(astro, dt)

    def simulate_system(self, t, dt, mode='euler'):
        "simula el sistema durante un tiempo total t y en tramos separados dt"
        if mode=='euler':
            sim_function = self.move_astros
        elif mode.lower() in ['rk4',"runge kutta 4",'runge_kutta4']:
            sim_function = self.move_astros_rk4
        while t>=self.t:
            sim_function(dt)
        for astro in self.astros:
            astro.history['r'] = np.array(astro.history['r'])
            astro.history['v'] = np.array(astro.history['v'])