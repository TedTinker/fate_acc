#%%

import os 
import glob
from ast import literal_eval as make_tuple

from utils import approach_list, align_colons, get_lines, maybe_int
    
    

# Class for agents, obstacles, and zones.
class Entity:
    
    def __init__(
            self,
            entity_type = "entity",     # Replace with agent, obstacle, or zone.
            name = "",                  # Name of the entity.
            color = (255, 255, 255),    # RGB color of window.
            autoload = False,           # Automatically load entity when fate-environment opens?
            **kwargs):                  # Any other variables.
        
        self.entity_type = entity_type  # Replace with agent, obstacle, or zone. 
        self.name = name                # All entities have a name and color, and can be autoloaded.
        self.color = color              
        self.autoload = autoload    
        self.use_inputs(**kwargs)       # Other inputs.
            
    # Use inputs.
    # Remake for agents, obstacles, and zones.
    def use_inputs(self, **kwargs): pass
    
    # Read file-lines.
    # Same for all entity-types. 
    def load(self):
        # Try reading file. If we can't, abort.
        lines = get_lines(self.entity_type, self.name)
        if(lines == None): print("\n\nFailed to load {}!\n\n".format(self.name))
        # If successful, apply file. 
        self.autoload = lines[-1].strip() == "autoload" 
        multiline_tracking = None   # Track which multiline variable is being recorded. 
        # Each line is "variable name : value".
        for i, line in enumerate(lines):
            tab = line.startswith("\t") # If tabbed, probably multiline variable.
            variable_name = line.split(":")[0].strip()
            value  = ":".join(line.split(":")[1:]).strip()
            variable_name = maybe_int(variable_name)
            value = maybe_int(value)
            multiline_tracking = self.load_line(tab, variable_name, value, multiline_tracking)

    # Read one file-line. 
    # Remake for agents, obstacles, and zones.
    def load_line(self, tab, variable_name, value, multiline_tracking):
        if(variable_name == "Entity"): self.name = value 
        if(variable_name == "Color"): self.color = value 
        return(multiline_tracking)
    
    # Save in file. 
    # Same for all entity-types. 
    def save(self): 
        for file in glob.glob(r"entities/{} {}*.txt".format(self.entity_type, self.name)):
            os.remove(file)
        with open(r"entities/{} {}{}.txt".format(self.entity_type, self.name, " (autoload)" if self.autoload else ""), 'w') as f:
            f.write(self.__str__())
            
    # How to print or save an entity. 
    # Remake for agents, obstacles, and zones. 
    def __str__(self):
        return(
"""Entity : {}
Color : {}{}""".format(
self.name, self.color, 
"\nautoload" if self.autoload else ""))        
    
    

# Player-characters or NPCs.
class Agent(Entity):
    def __init__(self, name="", color=(255, 0, 0), autoload=False, 
                 player         = "GM",     # Who plays this character?
                 description    = "",       # Describe agent. 
                 refresh        = 3,        # Maximum fate points?
                 fate_points    = 3,        # How many fate points right now?
                 approaches     = None,     # Approaches
                 aspects        = None,     # Aspects
                 stunts         = None,     # Stunts
                 stress         = None,        # Stress
                 consequences   = None):       # Consequences)
    
        if(approaches == None): approaches = {i : 0 for i in approach_list}
        if(aspects == None):    aspects = {i : "" for i in [1,2,3,4,5]}
        if(stunts == None):     stunts = {i : "" for i in [1,2,3]}
        if(stress == None):     stress = {i : "" for i in [1,2,3]}
        if(consequences == None): consequences = {i : "" for i in [2,4,6]}
        super().__init__(entity_type="agent", name=name, color=color, autoload=autoload, 
                         player=player, description=description, fate_points=fate_points, 
                         refresh=refresh, approaches=approaches, aspects=aspects, 
                         stunts=stunts, stress=stress, consequences=consequences)

    # Override use_inputs method for Agent-specific window reading.
    def use_inputs(self, **kwargs):
        self.player = kwargs["player"]
        self.description = kwargs["description"]
        self.refresh = kwargs["refresh"]
        self.fate_points = kwargs["fate_points"]
        self.approaches = kwargs["approaches"]
        self.aspects = kwargs["aspects"]
        self.stunts = kwargs["stunts"]
        self.stress = kwargs["stress"]
        self.consequences = kwargs["consequences"] 

    # Override load_line for Agent-specific file reading.
    def load_line(self, tab, variable_name, value, multiline_tracking):
        if(variable_name == "Agent"):           self.name           = value  
        if(variable_name == "Color"):           self.color          = make_tuple(value)  
        if(variable_name == "Description"):     self.description    = value
        if(variable_name == "Refresh"):         self.refresh        = value
        if(variable_name == "Fate Points"):     self.fate_points    = value
        if(variable_name == "Approaches"):      multiline_tracking  = "approaches"
        if(variable_name == "Aspects"):         multiline_tracking  = "aspects"
        if(variable_name == "Stunts"):          multiline_tracking  = "stunts"
        if(variable_name == "Stress"):          multiline_tracking  = "stress"
        if(variable_name == "Consequences"):    multiline_tracking  = "consequences"
        if(tab):
            if(multiline_tracking == "approaches"):     self.approaches[variable_name] = value
            if(multiline_tracking == "aspects"):        self.aspects[variable_name] = value
            if(multiline_tracking == "stunts"):         self.stunts[variable_name] = value
            if(multiline_tracking == "stress"):         self.stress[variable_name] = value
            if(multiline_tracking == "consequences"):   self.consequences[variable_name] = value
        return(multiline_tracking)

    # Override __str__ for Agent-specific string representation.
    def __str__(self):
        return(
"""Agent : {}
Player : {}
Description : {}
Refresh : {}
Fate Points : {}
Approaches : {}
Aspects : {}
Stunts : {}
Stress : {}
Consequences : {}
Color : {}{}""".format(
self.name, 
self.player, 
self.description, 
self.refresh, 
self.fate_points, 
align_colons(self.approaches), 
align_colons(self.aspects),
align_colons(self.stunts), 
align_colons(self.stress), 
align_colons(self.consequences),
self.color,
"\nautoload" if self.autoload else ""))
    
    

# Difficulties to overcome. 
class Obstacle(Entity): 
    
    def __init__(self, name = "", color = (0, 0, 0), autoload = False,
            now = 0,    # Current measure of overcoming the obstacle.
            win = 0,    # Measure of completly overcoming the obstacle. 
            lose = "None"):  # Measure of failing the obstacle. 
        
        super().__init__(entity_type="obstacle", name=name, color=color, autoload=autoload, 
                         now=now, win=win, lose=lose)
        
    # Override use_inputs method for Obstacle-specific window reading.
    def use_inputs(self, **kwargs):
        self.now = kwargs["now"]
        self.win = kwargs["win"]
        self.lose = kwargs["lose"]
        
    # Override load_line for Obstacle-specific file reading.
    def load_line(self, tab, variable_name, value, multiline_tracking):
        if(variable_name == "Obstacle"):    self.name = value  
        if(variable_name == "Color"):       self.color = make_tuple(value)  
        if(variable_name == "Now"):         self.now = value
        if(variable_name == "Win"):         self.win = value
        if(variable_name == "Lose"):        self.lose = value
        return(multiline_tracking)
        
    # Override __str__ for Obstacle-specific string representation.
    def __str__(self):
        return(
"""Obstacle : {}
Now : {}
Win : {}
Lose : {}
Color : {}{}""".format(
self.name, 
self.now,
self.win,
self.lose,
self.color,
"\nautoload" if self.autoload else ""))
    
    

# Categories for agents and obstacles. 
class Zone(Entity):
    
    def __init__(self, name = "", color = (255, 255, 255), autoload = False, 
            agents      = [],   # Agents in the zone.
            obstacles   = []):  # Obstacles in the zone. 
        
        super().__init__(entity_type="zone", name=name, color=color, autoload=autoload, 
                         agents=agents, obstacles=obstacles)
        
    # Override use_inputs method for Zone-specific window reading.
    def use_inputs(self, **kwargs):
        self.agent_names = [agent.name for agent in kwargs["agents"]]
        self.obstacle_names = [obstacle.name for obstacle in kwargs["obstacles"]]
        
    # Override load_line for Zone-specific file reading.
    def load_line(self, tab, variable_name, value, multiline_tracking):
        if(variable_name == "Zone"):            self.name           = value  
        if(variable_name == "Color"):           self.color          = make_tuple(value) 
        if(variable_name == "Agents"):          multiline_tracking  = "agents"
        if(variable_name == "Obstacles"):       multiline_tracking  = "obstacles"
        if(tab):
            if(multiline_tracking == "agents"):     self.agent_names.append(value)
            if(multiline_tracking == "obstacles"):  self.obstacle_names.append(value)
        return(multiline_tracking)
        
    # Override __str__ for Zone-specific string representation.
    def __str__(self):
        return(
"""Zone : {}
Agents : {}
Obstacles : {}
Color : {}{}""".format(
self.name, 
align_colons(self.agent_names), 
align_colons(self.obstacle_names),
self.color,
"\nautoload" if self.autoload else ""))
        
        

if __name__ == "__main__":
    
    example_agent = Agent(
        name = "Example Agent", 
        player = "GM", 
        description = "A character in a Fate: Accelerated game", 
        refresh = 10, 
        aspects = {1 : "blah", 2 : "foo", 3 : "gig", 4 : "baba", 5 : "kiki"}, 
        approaches = {i : j for i, j in zip(approach_list, [0,1,2,3,4,5])}, 
        stunts = {1 : "wow", 2: "fun", 3 : "zen"}, 
        stress = {1 : "", 2 : "Stubbed toe.", 3 : ""},
        consequences = {2 : "", 4 : "Stubbed toe super hard.", 6 : ""},
        autoload = True)
    print(example_agent)
    print("\n\nCan this be saved and loaded?\n\n")
    example_agent.save()
    del example_agent
    example_agent = Agent(name = "Example Agent")
    example_agent.load()
    print(example_agent)
    
    
    
    example_obstacle = Obstacle(
        name = "Example Obstacle",
        win = 10,
        autoload = True)
    print("\n\n")
    print(example_obstacle)
    print("\n\nCan this be saved and loaded?\n\n")
    example_obstacle.save()
    del example_obstacle
    example_obstacle = Obstacle(name = "Example Obstacle")
    example_obstacle.load()
    print(example_obstacle)
    
    
    
    example_zone = Zone(
        name = "Example Zone",
        agents = [example_agent],
        obstacles = [example_obstacle],
        autoload = True)
    print("\n\n")
    print(example_zone)
    print("\n\nCan this be saved and loaded?\n\n")
    example_zone.save()
    del example_zone
    example_zone = Zone(name = "Example Zone")
    example_zone.load()
    print(example_zone)
# %%
