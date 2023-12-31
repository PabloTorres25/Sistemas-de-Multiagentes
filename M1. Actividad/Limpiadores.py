from mesa import Agent, Model 
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np
import time
from datetime import datetime

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
        possible_moves = [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
        
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
                    self.model.basura_inicial -= 1
                    print("Basuras restantes =", self.model.basura_inicial)
                    
                    # Mueve al Limpiador a la nueva posición
                    self.model.grid.move_agent(self, (new_x, new_y))


class LimpiadoresModel(Model):
    def __init__(self, width, height, num_agents, por_basura, tiempo):
        self.grid = SingleGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True # Para la visualizacion usando navegador
        self.num_agents = num_agents
        self.num_serie = 0
        self.width = width
        self.height = height
        self.tiempo_maximo_segundos = tiempo
        self.tiempo_inicio = datetime.now()
        self.basura_inicial = int((por_basura / 100) * height * width)
        print("Basura inicial = ", self.basura_inicial)
        

        # Creación de Basura
        coor_basura = celdas_random(width, height, por_basura)
        for x, y in coor_basura:
            basura = Basura((x, y), self)    # Creamos un agente en x,y, su id son sus coordenadas
            self.grid.place_agent(basura, (x, y))        # Ahora lo colocamos
            self.schedule.add(basura) 
        
        primer_limpiador = Limpiador(self.num_serie, self)
        self.grid.place_agent(primer_limpiador, (1, 1))
        self.schedule.add(primer_limpiador)
        self.num_serie += 1

    def step(self):
        tiempo_actual = datetime.now() - self.tiempo_inicio
        print(f"Tiempo transcurrido: {tiempo_actual}")
        if tiempo_actual.total_seconds() >= self.tiempo_maximo_segundos:
            self.running = False  # Detener la simulación
            print("Tiempo Maximo alcanzado")
            porcentaje = (self.basura_inicial / (self.height * self.width)) * 100
            print("Basura restante = ", self.basura_inicial)
            print("Porcentaje de basura restante = ", porcentaje, "%")
            return
        
        if self.basura_inicial <= 0:
            self.running = False  # Detener la simulación
            print("SE ASPIRARON TODAS LAS BASURAS")
            print(f"En un tiempo de: {tiempo_actual}")
            return

        # Hacer avanzar el modelo
        self.schedule.step()

        # Creación de Limpiadores
        if self.grid.is_cell_empty((1, 1)) and self.num_serie < self.num_agents:
            # Crear un nuevo Limpiador
            new_limpiador = Limpiador(self.num_serie, self)
            self.grid.place_agent(new_limpiador, (1, 1))
            self.schedule.add(new_limpiador)
            self.num_serie += 1
        

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

    ancho = 5
    alto = 5
    numero_Agentes = 8
    porcentaje_basura = 30
    tiempo = 30
    grid = CanvasGrid(agent_portrayal, ancho, alto, 500, 500)
    server = ModularServer(LimpiadoresModel,
                        [grid],
                        "Robots Limpiadores Model",
                        {"width":ancho, "height":alto, 
                        "num_agents" : numero_Agentes, "por_basura" : porcentaje_basura, 
                        "tiempo" : tiempo})
    server.port = 8521 # The default
    server.launch()