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
    def __init__(self, unique_id, model, orientacion):
        super().__init__(unique_id, model)
        self.next_state = None
        self.orientacion = orientacion
        self.steps = 0
    
    def step(self):
        self.steps += 1

        if self.steps % 5 == 0:
            if self.color == "00B050":
                self.color = "FF0200"
            else:
                self.color = "00B050"


class CiudadModel(Model):
    def __init__(self, width, height,num_autos, list_edif, list_esta, list_glor, list_sem):
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True # Para la visualizacion usando navegador
        self.num_autos = num_autos
        id_agente = 0

        # Construccion del Mapa

        ## Edificios
        for edificio in list_edif:
            rango_x = edificio[1][0] - edificio[0][0] + 1
            rango_y = edificio[1][1] - edificio[0][1] + 1
            for i in range(rango_x):
                for j in range(rango_y):
                    new_edificio = Edificio(id_agente, self)
                    X = (edificio[0][0] + i) - 1
                    Y = height - (edificio[0][1] + j)
                    self.grid.place_agent(new_edificio, (X,Y))
                    self.schedule.add(new_edificio)
                    id_agente += 1
        
        ## Glorietas
        for glorieta in list_glor:
            new_glorieta = Glorieta(id_agente, self)
            X = glorieta[0] - 1
            Y = height - glorieta[1]
            self.grid.place_agent(new_glorieta, (X,Y))
            self.schedule.add(new_glorieta)
            id_agente += 1
        
        ## Semaforos
        for semaforos in list_sem:
            if (semaforos[1] == 'V'):
                X = semaforos[0][0] - 1
                Y = height - semaforos[0][1] - 1
            else:
                X = semaforos[0][0]
                Y = height - semaforos[0][1]
            new_semaforo = Semaforo(id_agente, self, semaforos[1])
            self.grid.place_agent(new_semaforo, (X,Y))
            self.schedule.add(new_semaforo)
            id_agente += 1
        
        ## Estacionamientos
        for estacionamiento in list_esta:
            new_estacionamiento = Estacionamiento(id_agente, self)
            X = estacionamiento[0] - 1
            Y = height - estacionamiento[1]
            self.grid.place_agent(new_estacionamiento, (X,Y))
            self.schedule.add(new_estacionamiento)
            id_agente += 1

        # new_auto = Auto(0, self)
        # self.grid.place_agent(new_auto, (5, 5))  # Agente en la posición (5, 5)
        # self.schedule.add(new_auto)


    def step(self):
        # Hacer avanzar el modelo
        self.schedule.step()

def agent_portrayal(agent):
    if isinstance(agent, Auto):
        portrayal = {"Shape": "arrowHead",
                    "Filled": "true",
                    "Layer": 1,
                    "Color": "black",
                    "scale": 0.5,
                    "heading_x": 1,
                    "heading_y": 0
                    }
    elif isinstance(agent, Edificio):
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "#5B9BD5",
                    "w": 1,
                    "h": 1
                    }
    elif isinstance(agent, Estacionamiento):
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "#FFFF00",
                    "w": 1,
                    "h": 1
                    }
    elif isinstance(agent, Glorieta):
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "#833C0B",
                    "w": 1,
                    "h": 1
                    }
    elif isinstance(agent, Semaforo):
        if agent.orientacion == 'H':
            portrayal = {"Shape": "rect",
                        "Filled": "true",
                        "Layer": 0,
                        "Color": "#FF0200",
                        "w": 2,
                        "h": 1
                        }
        elif agent.orientacion == 'V':
            portrayal = {"Shape": "rect",
                        "Filled": "true",
                        "Layer": 0,
                        "Color": "#00B050",
                        "w": 1,
                        "h": 2
                        }
    else:
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "black",
                    "w": 1,
                    "h": 1}
    return portrayal

if __name__ == "__main__":
    # Medidas
    ancho = 24
    alto = 24

    # Mapa
    lista_edificios: Tuple[Tuple[Tuple[int, int], Tuple[int, int]]] = (
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

    lista_estacionamientos: Tuple[Tuple[int, int]] = ( 
        (10,3), (3,4), (18,4), (12,5), (21,5), (7,6),
        (9,9), (22,10), (5,11), (12,11), (17,11),
        (3,18), (18,18), (20,18), (6,21), (9,21), (20,21)
    )

    lista_glorietas: Tuple[Tuple[Tuple[int, int], Tuple[int, int]]] = (
        ((14,14),(15,14),(14,15),(15,15))
    )

    lista_semaforos: Tuple[Tuple[Tuple[int, int], str]] = (
        ((17,1), "V"), ((15,3), "H"), ((8,7), "V"),
        ((6,9), "H"), ((1,12), "H"), ((3,13), "V"),
        ((22,15), "V"), ((23,17), "H"), 
        ((15,21), "H"), ((13,22), "H"), ((12,23), "V")
    )

    # Autos
    numero_autos = 1

    grid = CanvasGrid(agent_portrayal, ancho, alto, 720, 720)
    server = ModularServer(CiudadModel,
                        [grid],
                        "Ciudad Model",
                        {"width": ancho, "height": alto, 
                        "num_autos": numero_autos,
                        "list_edif": lista_edificios,
                        "list_esta": lista_estacionamientos,
                        "list_glor": lista_glorietas,
                        "list_sem": lista_semaforos})
    server.port = 8521 # The default
    server.launch()