from mesa import Agent, Model 
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def celdas_random(anchura, altura, porcentaje):
    total_celdas = int((porcentaje / 100) * altura * anchura)
    coordenadas_celdas = []

    for _ in range(total_celdas):
        while True:
            coordenada = (np.random.randint(0, altura), np.random.randint(0, anchura))
            if coordenada not in coordenadas_celdas and coordenada != (1, 1):
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
    
    def step(self):
        x, y = self.pos
        possible_moves = [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
        # Elige un nuevo paso
        new_x, new_y = self.random.choice(possible_moves)
        
        # Revisa si no se sale de la cuadricula y si está vacía
        if 0 <= new_x < self.model.grid.width and 0 <= new_y < self.model.grid.height and not self.model.grid.is_cell_occupied((new_x, new_y)):
            self.model.grid.move_agent(self, (new_x, new_y))

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
        
        # Creación de agentes
        # num_serie = 0
        # for i in range (num_agents):
        #     limpiador = Limpiador(num_serie, self)
        #     self.grid.place_agent(limpiador, (1, 1))
        #     self.schedule.add(limpiador) 
        #     num_serie +=1
        limpiador = Limpiador(0, self)
        self.grid.place_agent(limpiador, (1, 1))
        self.schedule.add(limpiador) 


    def step(self):
        self.schedule.step()

if __name__ == "__main__":
    
    def agent_portrayal(agent):
        if isinstance(agent, Limpiador):
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

    ancho = 10
    alto = 10
    numero_Agentes = 3
    porcentaje_basura = 20
    tiempo = 100
    grid = CanvasGrid(agent_portrayal, ancho, alto, 500, 500)
    server = ModularServer(LimpiadoresModel,
                        [grid],
                        "Robots Limpiadores Model",
                        {"width":ancho, "height":alto, 
                        "num_agents" : numero_Agentes, "por_basura" : porcentaje_basura, 
                        "tiempo" : tiempo})
    server.port = 8521 # The default
    server.launch()