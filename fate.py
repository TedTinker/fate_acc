import os

from entity import Entity, Obstacle, Zone

class Fate_Env:
    
    def __init__(self):
        self.entities = []
        self.obstacles = []
        self.zones = []
        
        for file in os.listdir("entities"):
            with open("entities/" + file) as f:
                lines = f.readlines()
                if(lines[-1].strip() == "autoload"):
                    name    = ":".join(lines[0].split(":")[1:]).strip()
                    player  = ":".join(lines[1].split(":")[1:]).strip()
                    self.entities.append(Entity(load = True, name = name, player = player))
                    
        for file in os.listdir("obstacles"):
            with open("obstacles/" + file) as f:
                lines = f.readlines()
                if(lines[-1].strip() == "autoload"):
                    name    = lines[0].strip()
                    self.obstacles.append(Obstacle(load = True, name = name))
        
        for file in os.listdir("zones"):
            with open("zones/" + file) as f:
                lines = f.readlines()
                if(lines[-1].strip() == "autoload"):
                    name    = lines[0].strip()
                    self.zones.append(Zone(load = True, name = name))
                            
    def __str__(self):
        to_return = "Entities:"
        for entity in self.entities:
            to_return += "\n\t" + entity.name
        to_return += "\nZones:"
        for zone in self.zones:
            to_return += "\n\t" + zone.name
            for entity_name in zone.entity_names:
                to_return += "\n\t\t" + entity_name
        return(to_return)
                


if __name__ == "__main__":
    env = Fate_Env()
    print(env)