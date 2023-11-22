#%% 
import os

from utils import align_colons
from entity import Agent, Obstacle, Zone

class Fate_Env:
    
    def __init__(self):
        self.agents = []
        self.obstacles = []
        self.zones = []
        
        for file in os.listdir("entities"):
            if(file.endswith("(autoload).txt")):
                with open("entities/" + file) as f:
                    file = file.replace("(autoload)", "")[:-4]
                    words = file.split()
                    entity_type = words[0].strip()
                    name = ' '.join(word for word in words[1:]).strip()
                    if(entity_type == "agent"):
                        agent = Agent(name = name)
                        agent.load()
                        self.agents.append(agent)
                    if(entity_type == "obstacle"):
                        obstacle = Obstacle(name = name)
                        obstacle.load()
                        self.obstacles.append(obstacle)
                    if(entity_type == "zone"):
                        zone = Zone(name = name)
                        zone.load()
                        self.zones.append(zone)
                            
    def __str__(self):
        to_return = "Agents:"
        to_return += align_colons([agent.name for agent in self.agents])
        to_return += "\nObstacles:"
        to_return += align_colons([obstacle.name for obstacle in self.obstacles])
        to_return += "\nZones:"
        to_return += align_colons([zone.name for zone in self.zones])
        return(to_return)
                


if __name__ == "__main__":
    env = Fate_Env()
    print(env)