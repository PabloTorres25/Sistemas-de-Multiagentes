from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class YourAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class YourModel(Model):
    def __init__(self, width, height):
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Crea tus agentes y colócalos en la grid aquí según sea necesario

def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect",
        "Filled": "true",
        "Layer": 0,
        "Color": "blue",  # Fondo azul para todas las celdas
        "w": 1,
        "h": 1
    }

    x, y = agent.pos
    if x == 2:  # Remarcar la línea media horizontalmente
        portrayal["Color"] = "red"  # Cambiar el borde a negro
        portrayal["stroke_width"] = 2  # Aumentar el ancho del borde

    return portrayal

if __name__ == "__main__":
    width = 4
    height = 4

    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
    server = ModularServer(YourModel,
                           [grid],
                           "Grid con línea remarcada",
                           {"width": width, "height": height})
    server.port = 8521  # El puerto por defecto
    server.launch()
