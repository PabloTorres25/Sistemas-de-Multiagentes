from mesa import Agent, Model
from mesa.visualization.modules import TextElement
from mesa.visualization.ModularVisualization import ModularServer

class SimpleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class MyModel(Model):
    def __init__(self):
        self.schedule = []
        for i in range(5):
            agent = SimpleAgent(i, self)
            self.schedule.append(agent)

class CustomText(TextElement):
    def __init__(self, text):
        self.text = text

    def render(self, model):
        return f"<p>{self.text}</p>"

text_element = CustomText("Hola Mundo")

server = ModularServer(MyModel, [text_element], "Modelo")
server.port = 8521
server.launch()
