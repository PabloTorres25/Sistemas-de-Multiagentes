# from flask import Flask, redirect, url_for, request
# app = Flask(__name__)
# # http://192.168.0.1//tc2008b?name=silvana
# # Punto de acceso 'tc2008b'
# @app.route('/tc2008b', methods=['GET', 'POST'])

# def tc2008b():
#     if request.method == 'POST':
#         return 'please use GET'
#     else:
#         user = request.args.get('name')
#         return 'welcome %s' % user

# if __name__ == '__main__':
#     app.run(debug = True)

from mesa import Agent, Model 
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from typing import Tuple, Any
import numpy as np
import random
from ciudad import CiudadModel, agent_portrayal, AutoInfoText



if __name__ == "__main__":
    info_text = AutoInfoText()
    grid = CanvasGrid(agent_portrayal, 24, 24, 720, 720)
    server = ModularServer(CiudadModel,
                        [grid, info_text],
                        "Ciudad Model")
    server.port = 8521 # The default
    server.launch()