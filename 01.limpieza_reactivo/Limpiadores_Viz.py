from Limpiadores import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}
    
    return portrayal

ancho = 5
alto = 5
numero_Agentes = 3
porcentaje_basura = 20
tiempo = 100
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(LimpiadoresModel,
                       [grid],
                       "Robots Limpiadores Model",
                       {"width":ancho, "height":alto, 
                       "num_agents" : numero_Agentes, "por_basura" : porcentaje_basura, 
                       "tiempo" : tiempo})
server.port = 8521 # The default
server.launch()