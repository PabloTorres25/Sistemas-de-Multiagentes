from mesa import Agent, Model 
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from typing import Tuple, Any
import numpy as np

def traduccion(val1, val2):
    return val1 - 1, alto - val2 

class Auto(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None
        self.unique_id = unique_id
        self.destino_or = [3,4]
        self.destino = traduccion(self.destino_or[0], self.destino_or[1])   # Traducción de las coordenadas de destino_or
        self.destino_bool = False
        self.primer_paso = False
        self.estado = ""

        self.movimientos_estado = {
            "Ar": (0, 1),   # Arriba
            "Ab": (0, -1),  # Abajo
            "Iz": (-1, 0),  # Izquierda
            "De": (1, 0)    # Derecha
        }

    def girar_sin_opcion(self, pos_list, lista_celdas):
        for coor, direccion in lista_celdas:
            print("Posición2 = ", pos_list)
            print("Coordenada = ", coor)
            pos_list = tuple(pos_list)
            if pos_list == coor:
                print("Son iguales!!!!")
                return direccion # Se queda quieto un segundo, para simular que gira (Aunque no se vea)
        return None # O retorna un valor predeterminado si no encuentra una coincidencia
    
    def step(self):
        print("Posición = ", self.pos)
        x, y = self.pos
        pos_list = [x,y]

        if pos_list == self.destino:
            if (self.destino_bool == False):
                print("LLEGUE A MI DESTINO!!!, Auto ID = ", self.unique_id)
                self.destino_bool = True
        else:
            # Primero, vemos si esta en un estacionamiento que no sea el de destino
            cell_contents = self.model.grid.get_cell_list_contents([(x, y)])    # Revisa que hay en su celda
            estacionamiento_agents = [agent for agent in cell_contents if isinstance(agent, Estacionamiento)]  # Revisa si hay un estacionamiento en su celda
            
            # Si esta en un estacionamiento
            if estacionamiento_agents:
                for move in self.movimientos_estado.values():
                    new_pos = (x + move[0], y + move[1])
                    if self.model.grid.is_cell_empty(new_pos):
                        self.model.grid.move_agent(self, new_pos)
                        break

            # Si ya salio del estacionamiento
            elif self.primer_paso == False:
                print("Ya di mi primer paso, ahora ire al lado...")
                self.estado = self.girar_sin_opcion(pos_list, lista_primeros_traducida)
                print(self.estado)
                self.primer_paso = True

            # Si esta en una celda de giro            
            elif pos_list in lista_giros_traducida:
                        for coor, direccion in lista_celdas:
            print("Posición2 = ", pos_list)
            print("Coordenada = ", coor)
            pos_list = tuple(pos_list)
            if pos_list == coor:
                print("Son iguales!!!!")
                return direccion
                print("Oh miren una celda de giro, creo que ahora ire a...")
                self.estado = self.girar_sin_opcion(pos_list, lista_giros_traducida)
                print(self.estado)

            # # Si esta en una celda de descición 
            # elif pos_list in lista_celdas_eleccion:
            #     for coor, estado in lista_celdas_eleccion:
            #         coor_traducida = [coor[0] - 1, self.model.grid.height - coor[1]]
            #         if pos_list == coor_traducida:
            #             self.estado = estado
            #             break
            else:
                # Muevete segun tu estado
                 if self.estado in self.movimientos_estado:
                    movimiento = self.movimientos_estado[self.estado]
                    self.model.grid.move_agent(self, (x + movimiento[0], y + movimiento[1]))

        # if 0 <= new_x < self.model.grid.width and 0 <= new_y < self.model.grid.height:
        #     if self.model.grid.is_cell_empty((new_x, new_y)):
        #         self.model.grid.move_agent(self, (new_x, new_y))
        #     self.model.grid.move_agent(self, (new_x, new_y))

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
        if self.orientacion == 'V':
            self.color = "#00B050"
        else:
            self.color = "#FF0200"

    def step(self):
        self.steps += 1
        if self.steps % 10 == 0:
            if self.color == "#00B050":
                self.color = "#FF0200"
            else:
                self.color = "#00B050"

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
        
        # Auto
        new_auto = Auto(id_agente, self)
        self.grid.place_agent(new_auto, (10-1, height - 3))
        self.schedule.add(new_auto)
        id_agente += 1

    def step(self):
        # Hacer avanzar el modelo
        self.schedule.step()

def agent_portrayal(agent):
    if isinstance(agent, Auto):
        portrayal = {"Shape": "circle",
                        "Filled": "true",
                        "Layer": 1,
                        "Color": "black",
                        "r": 0.8
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
                        "Color": agent.color,
                        "w": 2,
                        "h": 1
                        }
        elif agent.orientacion == 'V':
            portrayal = {"Shape": "rect",
                        "Filled": "true",
                        "Layer": 0,
                        "Color": agent.color,
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

    # Coordenadas especiales
    lista_primeros_pasos: Tuple[Tuple[int, int], str] = (
        ((10,2),"Iz"), ((2,4),"Ab"), ((19,4),"Ab"), ((13,5),"Ab"),
        ((20,5),"Ab"),((7,7),"Iz"),
        ((9,8),"Iz")    # Aun faltan
    )
    lista_primeros_traducida = tuple((traduccion(tupla[0][0], tupla[0][1]), tupla[1]) for tupla in lista_primeros_pasos)

    lista_celdas_giro: Tuple[Tuple[int, int], str] = (
        ((1,1),"Ab"), ((2,2),"Ab") 
    )
    lista_giros_traducida = tuple((traduccion(tupla[0][0], tupla[0][1]), tupla[1]) for tupla in lista_celdas_giro)
    print("lista_giros_traducida = ", lista_giros_traducida)

    Eleccion = Tuple[Tuple[int, int], Tuple[str, ...]]  # Cambiarlo si vemos que solo se utilizan maximo 2 str
    lista_celdas_eleccion: Eleccion = (
        ((1,16),"Ab","De"), ((2,15),"Ab", "De")
    )

    # Autos
    numero_autos = 1    # TODO: Hay que hacer que los Autos aparezcan solo en estacionamientos

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