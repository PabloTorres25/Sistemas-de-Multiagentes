from mesa import Agent, Model 
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
import numpy as np

def celdas_random(anchura, altura, porcentaje):
    total_celdas = int((porcentaje / 100) * altura * anchura)
    coordenadas_celdas = []

    for _ in range(total_celdas):
        while True:
            coordenada = (np.random.randint(0, altura), np.random.randint(0, anchura))
            if coordenada not in coordenadas_celdas:
                coordenadas_celdas.append(coordenada)
                break

    return coordenadas_celdas

class Basura(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None

class Limpiador(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None

class LimpiadoresModel(Model):
    def __init__(self, width, height, num_agents, por_basura, tiempo):
        self.grid = SingleGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True #Para la visualizacion usando navegador

        # Creación de Basura
        coor_basura = celdas_random(width, height, por_basura)
        for x, y in coor_basura:
            basura = Basura((x, y), self)    # Creamos un agente en x,y, su id son sus coordenadas
            self.grid.place_agent(basura, (x, y))        # Ahora lo colocamos
            self.schedule.add(basura) 
        
        # # Creación de agentes
        # num_serie = 0
        # for i in range (num_agents):
        #     limpiador = Limpiador(num_serie, self)
        #     self.grid.place_agent(limpiador, (1, 1))
        #     self.schedule.add(limpiador) 
        #     num_serie +=1
    
    def step(self):
        self.schedule.step()
