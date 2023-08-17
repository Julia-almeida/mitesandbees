from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer

# change this to match your file name if it's not direct_contact.py!
from bees_mites_model import *

# The parameters we run the model with.
# Feel free to change these!
# params = {"N": 600,
#           "width": 70,
#           "height": 50}
params = {"N": 600,
          "width": 60,
          "height": 60}

def agent_portrayal(agent):
    if agent.critter_type == "bee":
        portrayal = {"Shape": "circle",
                     "Color": "#ffd700", # a darkish yellow or gold
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.75}
    else:
        portrayal = {"Shape": "circle",
                     "Color": "brown",
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.35}
    # if agent.infected and agent.days_since_infected < 20:
    #     portrayal["Color"] = "LimeGreen"
    #     portrayal["Layer"] = 1
    if agent.critter_type == "bee":
        if agent.infected:
            print(f'INFECTED: {agent.unique_id} for {agent.hours_since_infected} hours')
            if agent.hours_since_infected >= 5:
                print(f'FADED: {agent.unique_id}')
                portrayal["Color"] = "Blue"
                portrayal["Filled"] = "false"
                portrayal["r"] = 0.5
                portrayal["Layer"] = 1
    return portrayal

grid = CanvasGrid(agent_portrayal,
                  params["width"],
                  params["height"],
                  20 * params["width"],
                  20 * params["height"])

infected_chart = ChartModule([{"Label": "Infected",
                               "Color": "LimeGreen"}],
                             data_collector_name="datacollector")

server = ModularServer(InfectionModel,
                       [grid, infected_chart],
                       "Infection Model",
                       params)
server.launch()

