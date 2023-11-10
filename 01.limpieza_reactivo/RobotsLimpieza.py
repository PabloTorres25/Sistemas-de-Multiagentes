from mesa import Agent, Model 
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
import numpy as np

class Basura(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None

class Modelo(Model):
    def __init__(self, width, height, num_agents, ):
        self.grid = SingleGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True #Para la visualizacion usando navegador

        for content, (x, y) in self.grid.coord_iter():
            a = Basura((x, y), self)    # Creamos un agente en x,y, su id son sus coordenadas
            self.grid.place_agent(a, (x, y))        # Ahora lo colocamos