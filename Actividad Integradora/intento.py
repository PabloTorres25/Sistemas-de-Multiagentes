from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa import Agent, Model 
from mesa.space import SingleGrid
from mesa.time import RandomActivation

class YourAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class YourModel(Model):
    def __init__(self, width, height):
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)

def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect",
        "Filled": "true",
        "Layer": 0,
        "Color": "blue",  # Fondo azul para todas las celdas
        "w": 1,
        "h": 1
    }
    return portrayal

if __name__ == "__main__":
    ancho = 10
    alto = 10

    grid = CanvasGrid(agent_portrayal, ancho, alto, 500, 500)
    server = ModularServer(YourModel, [grid], "Grid Azul", {"width": ancho, "height": alto})
    server.port = 8521  # El puerto por defecto
    server.launch()
