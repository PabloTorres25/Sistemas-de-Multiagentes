from mesa import Agent, Model 
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np

class Auto(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None

class Edificio(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None

class Estacionamiento(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None

class Semaforo(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None


class CiudadModel(Model):
    def __init__(self, width, height,num_autos):
        self.grid = SingleGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True # Para la visualizacion usando navegador
        self.num_autos = num_autos

        new_auto = Auto(0, self)
        self.grid.place_agent(new_auto, (1, 1))
        self.schedule.add(new_auto)

    def step(self):
        # Hacer avanzar el modelo
        self.schedule.step()

if __name__ == "__main__":
    
    def agent_portrayal(agent):
        if isinstance(agent, Auto):
            portrayal = {"Shape": "circle",
                        "Filled": "true",
                        "Layer": 0,
                        "Color": "red",
                        "r": 0.5}
        else:
            portrayal = {"Shape": "circle",
                        "Filled": "true",
                        "Layer": 0,
                        "Color": "blue",
                        "r": 0.25}
        return portrayal

    ancho = 20
    alto = 20
    numero_coches = 10
    grid = CanvasGrid(agent_portrayal, ancho, alto, 500, 500)
    server = ModularServer(CiudadModel,
                        [grid],
                        "Ciudad Model",
                        {"width": ancho, "height": alto, "num_autos":numero_coches})
    server.port = 8521 # The default
    server.launch()