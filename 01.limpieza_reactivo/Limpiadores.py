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
        
        # De todas las posibilidades elige una
        new_x, new_y = self.random.choice(possible_moves)
        # Si la elección no se sale del margen
        if 0 <= new_x < self.model.grid.width and 0 <= new_y < self.model.grid.height:
            # Y si la elección es una calda vacia
            if self.model.grid.is_cell_empty((new_x, new_y)):
                # Muevete a la elección, sino no hagas nada
                self.model.grid.move_agent(self, (new_x, new_y))
            # O si es de basura, Aspira
            else: 
                cell_contents = self.model.grid.get_cell_list_contents([(new_x, new_y)])
                basura_agents = [agent for agent in cell_contents if isinstance(agent, Basura)]

                if basura_agents:
                    # Aspira = Elimina la basura
                    basura_agent = basura_agents[0]  # Suponemos que solo hay una basura en la celda
                    self.model.grid.remove_agent(basura_agent)
                    
                    # Mueve al Limpiador a la nueva posición
                    self.model.grid.move_agent(self, (new_x, new_y))


class LimpiadoresModel(Model):
    def __init__(self, width, height, num_agents, por_basura, tiempo):
        self.grid = SingleGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True # Para la visualizacion usando navegador
        self.num_agents = num_agents
        self.num_serie = 0
        

        # Creación de Basura
        coor_basura = celdas_random(width, height, por_basura)
        for x, y in coor_basura:
            basura = Basura((x, y), self)    # Creamos un agente en x,y, su id son sus coordenadas
            self.grid.place_agent(basura, (x, y))        # Ahora lo colocamos
            self.schedule.add(basura) 
        
        

        limpiador = Limpiador(self.num_serie, self)
        self.grid.place_agent(limpiador, (1, 1))
        self.schedule.add(limpiador) 

    def step(self):
        # Creación de Limpiadores
        # if self.model.grid.is_cell_empty((1, 1)) and num_serie < num_agents:
        #         num_serie +=1
        #         nuevo_limpiador = Limpiador(num_serie, self)
        #         self.grid.place_agent(nuevo_limpiador, (1, 1))
        #         self.schedule.add(nuevo_limpiador) 
        if self.num_serie < self.num_agents:
            # Crear un nuevo Limpiador
            self.num_serie +=1
            new_limpiador = Limpiador(self.num_serie, self)
            self.grid.place_agent(new_limpiador, (9, 0))
            self.schedule.add(new_limpiador)

        # Hacer avanzar el modelo
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
    porcentaje_basura = 30
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