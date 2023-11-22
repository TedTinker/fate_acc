from utils import approach_list, align_colons, get_lines, maybe_int
    
    

# Class for agents, obstacles, and zones.
class Entity:
    
    def __init__(
            self,
            name = "",          # Name of the entity.
            autoload = False,   # Automatically load entity when fate-environment opens?
            **kwargs):          # Any other variables.
        
        self.entity_type = "entity" # Replace with agent, obstacle, or zone. 
        self.name = name            # All entities have a name, and can be autoloaded.
        self.autoload = autoload    
        self.use_inputs(**kwargs)   # Other inputs.
            
    # Use inputs.
    # Remake for agents, obstacles, and zones.
    def use_inputs(self, **kwargs): pass
    
    # Read file-lines.
    # Same or all entity-types. 
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
        return(multiline_tracking)
    
    # Save in file. 
    # Same for all entity-types. 
    def save(self): 
        with open(r"entities/{} {}{}.txt".format(self.entity_type, self.name, " (autoload)" if self.autoload else ""), 'w') as f:
            f.write(self.__str__())
            
    # How to print or save an entity. 
    # Remake for agents, obstacles, and zones. 
    def __str__(self):
        return(
"""Entity : {}{}""".format(
self.name, 
"\nautoload" if self.autoload else ""))        
    
    
    
class Agent(Entity):
    def __init__(self, name="", autoload=False, 
                 player         = "GM",     # Who plays this character?
                 description    = "",       # Describe agent. 
                 fate_points    = 3,        # How many fate points right now?
                 refresh        = 3,        # Maximum fate points?
                 approaches     = {i : 0 for i in approach_list},   # Approaches
                 aspects        = {i : "" for i in [1,2,3,4,5]},    # Aspects
                 stunts         = {i : "" for i in [1,2,3]},        # Stunts
                 stress         = {i : "" for i in [1,2,3]},        # Stress
                 consequences   = {i : "" for i in [2,4,6]}):       # Consequences)
        super().__init__(name, autoload, 
                         player=player, description=description, fate_points=fate_points, 
                         refresh=refresh, approaches=approaches, aspects=aspects, 
                         stunts=stunts, stress=stress, consequences=consequences)
        self.entity_type = "agent"  

    # Override use_inputs method for Agent-specific behavior.
    def use_inputs(self, **kwargs):
        self.player = kwargs["player"]
        self.description = kwargs["description"]
        self.fate_points = kwargs["fate_points"]
        self.refresh = kwargs["refresh"]
        self.approaches = kwargs["approaches"]
        self.aspects = kwargs["aspects"]
        self.stunts = kwargs["stunts"]
        self.stress = kwargs["stress"]
        self.consequences = kwargs["consequences"] 

    # Override load_line for Agent-specific file reading.
    def load_line(self, tab, variable_name, value, multiline_tracking):
        if(variable_name == "Agent"):           self.name           = value  
        if(variable_name == "Description"):     self.descriptions   = value
        if(variable_name == "Fate Points"):     self.fate_points    = value
        if(variable_name == "Refresh"):         self.refresh        = value
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
Fate Points : {}
Refresh : {}
Approaches : {}
Aspects : {}
Stunts : {}
Stress : {}
Consequences : {}{}""".format(
self.name, 
self.player, 
self.description, 
self.fate_points, 
self.refresh, 
align_colons(self.approaches), 
align_colons(self.aspects),
align_colons(self.stunts), 
align_colons(self.stress), 
align_colons(self.consequences),
"\nautoload" if self.autoload else ""))
    
    
    
class Obstacle(Entity): 
    
    def __init__(
            self,
            name = "",  autoload = False,
            now = 0,    # Current measure of overcoming the obstacle.
            win = 0,    # Measure of completly overcoming the obstacle. 
            lose = 0):  # Measure of failing the obstacle. 
        
        super().__init__(name, autoload, 
                         now=now, win=win, lose=lose)
        self.entity_type = "obstacle"  
        
    # Override use_inputs method for Obstacle-specific behavior.
    def use_inputs(self, **kwargs):
        self.now = kwargs["now"]
        self.win = kwargs["win"]
        self.lose = kwargs["lose"]
        
    # Override load_line for Obstacle-specific file reading.
    def load_line(self, tab, variable_name, value, multiline_tracking):
        if(variable_name == "Obstacle"):    self.name = value  
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
Lose : {}{}""".format(
self.name, 
self.now,
self.win,
self.lose,
"\nautoload" if self.autoload else ""))
    
    
    
class Zone(Entity):
    
    def __init__(self, name = "", autoload = False, 
            entities    = {},
            obstacles   = {}):
        
        super().__init__(name, autoload, 
                         entities=entities, obstacles=obstacles)
        self.entity_type = "zone"  
        
    # Override use_inputs method for Zone-specific behavior.
    def use_inputs(self, **kwargs):
        self.entity_names = [entity.name for entity in kwargs["entities"]]
        self.obstacle_names = [obstacle.name for obstacle in kwargs["obstacles"]]
        
    # Override load_line for Zone-specific file reading.
    def load_line(self, tab, variable_name, value, multiline_tracking):
        if(variable_name == "Zone"):            self.name           = value  
        if(variable_name == "Entities"):        multiline_tracking  = "entities"
        if(variable_name == "Obstacles"):       multiline_tracking  = "obstacles"
        if(tab):
            if(multiline_tracking == "entities"):   self.entity_names[variable_name] = value
            if(multiline_tracking == "obstacles"):  self.entity_names[variable_name] = value
        return(multiline_tracking)
        
    # Override __str__ for Zone-specific string representation.
    def __str__(self):
        return(
"""Zone : {}
Entities : {}
Zones : {}{}""".format(
self.name, 
align_colons(self.entity_names), 
align_colons(self.obstacle_names),
"\nautoload" if self.autoload else ""))
        
        

if __name__ == "__main__":
    
    example_entity = Agent(
        name = "Example Entity", 
        player = "GM", 
        description = "An entity in a Fate: Accelerated game", 
        refresh = 10, 
        aspects = {1 : "blah", 2 : "foo", 3 : "gig", 4 : "baba", 5 : "kiki"}, 
        approaches = {i : j for i, j in zip(approach_list, [0,1,2,3,4,5])}, 
        stunts = {1 : "wow", 2: "fun", 3 : "zen"}, 
        stress = {1 : "", 2 : "Stubbed toe.", 3 : ""},
        consequences = {2 : "", 4 : "Stubbed toe super hard.", 6 : ""},
        autoload = True)
    print(example_entity)
    print("\n\nCan this be saved and loaded?\n\n")
    example_entity.save()
    del example_entity
    example_entity = Entity(name = "Example Entity")
    example_entity.load()
    print(example_entity)
    
    
    
    example_obstacle = Obstacle(
        name = "Example Obstacle",
        win = 10,
        autoload = True)
    
    print("\n\n")
    print(example_obstacle)
    print("\n\nCan this be saved and loaded?\n\n")
    
    example_obstacle.save()
    example_obstacle = Obstacle(
        load = True,
        name = "Example Obstacle")
    print(example_obstacle)
    
    
    
    example_zone = Zone(
        name = "Example Zone",
        entities = [example_entity],
        obstacles = [example_obstacle],
        autoload = True)
    
    print("\n\n")
    print(example_zone)
    print("\n\nCan this be saved and loaded?\n\n")
    
    example_zone.save()
    example_zone = Zone(
        load = True,
        name = "Example Zone")
    print(example_zone)