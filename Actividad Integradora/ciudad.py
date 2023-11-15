from mesa import Agent, Model 
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from typing import Tuple
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

class Glorieta(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None

class Semaforo(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None


class CiudadModel(Model):
    def __init__(self, width, height,num_autos, list_edif, list_esta):
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True # Para la visualizacion usando navegador
        self.num_autos = num_autos

        # Construccion del Mapa

        ## Edificios
        id_edificio = 0
        for edificio in list_edif:
            rango_x = edificio[1][0] - edificio[0][0] + 1
            rango_y = edificio[1][1] - edificio[0][1] + 1
            for i in range(rango_x):
                for j in range(rango_y):
                    new_edificio = Edificio(id_edificio, self)
                    X = (edificio[0][0] + i) - 1
                    Y = height - (edificio[0][1] + j)
                    self.grid.place_agent(new_edificio, (X,Y))
                    self.schedule.add(new_edificio)
                    id_edificio += 1

        # new_auto = Auto(0, self)
        # self.grid.place_agent(new_auto, (5, 5))  # Agente en la posición (5, 5)
        # self.schedule.add(new_auto)
        

        


    def step(self):
        # Hacer avanzar el modelo
        self.schedule.step()

def agent_portrayal(agent):
    if isinstance(agent, Auto):
            portrayal = {"Shape": "circle",
                        "Filled": "true",
                        "Layer": 1,
                        "Color": "red",
                        "r": 0.5}
    else:
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "blue",
                    "w": 1,
                    "h": 1}
    return portrayal

if __name__ == "__main__":
    # Medidas
    ancho = 24
    alto = 24

    # Mapa
    lista_edificios: Tuple[Tuple[Tuple[int,int], Tuple[int,int]]] = (
        ((3,3),(12,6)),
        ((17,3),(18,6)),
        ((21,3),(22,6)), 
        
        ((3,9),(5,12)),
        ((8,9),(12,12)),
        ((17,9),(18,12)),
        ((21,9),(22,12)),

        ((3,17),(6,22)),
        ((9,17),(12,22)),
        ((17,17),(22,18)),
        ((17,21),(22,22))
    )
    lista_estacionamientos = ( (10,3), (3,4) )

    # Autos
    numero_autos = 1

    grid = CanvasGrid(agent_portrayal, ancho, alto, 720, 720)
    server = ModularServer(CiudadModel,
                        [grid],
                        "Ciudad Model",
                        {"width": ancho, "height": alto, 
                        "num_autos": numero_autos,
                        "list_edif": lista_edificios,
                        "list_esta": lista_estacionamientos})
    server.port = 8521 # The default
    server.launch()