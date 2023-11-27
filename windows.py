import dearpygui.dearpygui as dpg

from utils import approach_list, agent_start_x, obstacle_start_x, zone_start_x



# Class for agent, obstacle, and zone windows.
class Entity_Window:
    
    def __init__(self, entity, width = 300, x_pos = 0, y_pos = 0):
        self.entity = entity
        self.width = width
        with dpg.theme() as self.theme:
            with dpg.theme_component(dpg.mvThemeCol_WindowBg):
                dpg.add_theme_color(
                    dpg.mvThemeCol_WindowBg, 
                    self.entity.color + (255,), 
                    category=dpg.mvThemeCat_Core)
                
        with dpg.window(
                label="{} : {}".format(self.entity.entity_type, self.entity.name),
                no_close=True,
                pos=(x_pos, y_pos), 
                width = self.width, 
                collapsed=True) as self.window: 
            dpg.bind_item_theme(self.window, self.theme) # Not working >:C
            self.type_to_window(self.window)
            with dpg.group(horizontal=True):
                dpg.add_text("Autoload")
                self.autoload_checkbox_id = dpg.add_checkbox(default_value=self.entity.autoload, tag=self.n("autoload_checkbox"))
        
    # Add name to string. 
    # Same for all entity-types.
    def n(self, s):
        s = "{}_{}".format(self.entity.name, s)
        return(s)
            
    # Move data from the entity to the window.
    # Remake for agents, obstacles, and zones.
    def type_to_window(self, window):
        pass
          
    # Move data from window to entity.
    # Remake for agents, obstacles, and zones.
    def window_to_entity(self):
        pass
    
    
    
# How do have dictionaries or lists in windows.
class Window_Dict:
    
    def __init__(
            self,
            window_group,           # Window or group in which to render.
            label,                  # Label of list/dictionary.
            entity_name,            # Name of entity.
            keys = [],              # Keys of dictionary (leave as [] for list).
            values = [],            # Labels of list/dictionary.
            actually_list = False): # Only allow editing keys if a dictionary. 
        
        self.window_group = window_group
        self.label = label
        self.entity_name = entity_name
        if(values == []):   # If there are no values, make empty key/value pair.
            keys = ["None"]
            values = ["None"]
        if(keys == []):     # If no keys, add default keys. 
            keys = [i+1 for i in range(len(values))]
        self.dict = {key : value for key, value in zip(keys, values)}
        self.actually_list = actually_list
        self.render()
        
    # Show the dictionary/list.
    def render(self):
        with dpg.group(parent = self.window_group):
            # If already rendered, remove old render. 
            if hasattr(self, 'group_id') and dpg.does_item_exist(self.group_id):
                dpg.delete_item(self.group_id)
            if hasattr(self, 'row_group_ids'):
                for row_group_id in self.row_group_ids:
                    if dpg.does_item_exist(row_group_id):
                        dpg.delete_item(row_group_id)
            # Render and track rows.
            self.group_id = dpg.add_group()
            self.row_group_ids = []
            with dpg.group(horizontal=True, parent=self.group_id):
                dpg.add_text(self.label)
                self.add_add_button()
            for i, (key, value) in enumerate(self.dict.items()):
                row_group_id = dpg.add_group()
                self.row_group_ids.append(row_group_id)
                with dpg.group(horizontal=True, parent=row_group_id):
                    if(self.actually_list):
                        dpg.add_text(key)
                    else:
                        dpg.add_input_text(label="", default_value=key, width=25, tag="{}_{}_{}_key".format(self.entity_name, self.label, i))
                        
                    dpg.add_input_text(label="", default_value=value, tag="{}_{}_{}".format(self.entity_name, self.label, i))
                    dpg.add_button(label="-", callback=self.minus_button, user_data=(key, row_group_id))
                    
    # A subclass replaces this button with a dropdown.
    def add_add_button(self):
        dpg.add_button(label="+", callback=self.add_button)
            
    # Add default key and empty value.
    def add_button(self, sender, app_data, user_data):
        i = 1
        keys = list(self.dict.keys())
        while(i in keys or str(i) in keys):
            i += 1
        self.dict[i] = ""
        self.renew_keys()
        self.render()
    
    # Remove key and value from row of button clicked. 
    def minus_button(self, sender, app_data, user_data):
        key_to_remove, row_group_id = user_data
        del self.dict[key_to_remove]
        self.renew_keys()
        self.render()
        
    # Update dictionary based on input text.
    def update_dict(self):
        updated_dict = {}
        for i, row_group_id in enumerate(self.row_group_ids):
            if dpg.does_item_exist(row_group_id):
                key_tag = None if self.actually_list else "{}_{}_{}_key".format(self.entity_name, self.label, i)
                value_tag = "{}_{}_{}".format(self.entity_name, self.label, i)
                key = dpg.get_value(key_tag) if key_tag and dpg.does_item_exist(key_tag) else i
                value = dpg.get_value(value_tag) if dpg.does_item_exist(value_tag) else None
                if key is not None and value is not None:
                    updated_dict[key] = value
        self.dict = updated_dict
        self.renew_keys()
        
    def give_dict(self):
        self.update_dict()
        return(self.dict)
        
    def renew_keys(self):
        if(self.actually_list):
            sorted_items = sorted(self.dict.items())
            self.dict = {new_key: value for new_key, (_, value) in enumerate(sorted_items, start=1)}
            
            
            
# How do have dictionaries or lists in windows, with dropdown.
class Window_Dropdown(Window_Dict):
    
    def __init__(
            self,
            window_group,           # Window or group in which to render.
            label,                  # Label of list/dictionary.
            entity_name,            # Name of entity.
            keys = [],              # Keys of dictionary (leave as [] for list).
            values = []):           # Labels of list/dictionary.
        
        self.window_group = window_group
        self.combo_id = None
        super().__init__(window_group=window_group,label=label,entity_name=entity_name,
                         keys=keys,values=values,actually_list=True)
        
    # A subclass replaces this button with a dropdown.
    def add_add_button(self, window_list = []):
        self.window_list = [window for window in window_list if window.entity.name in self.dict.values()]
        if self.combo_id and dpg.does_item_exist(self.combo_id):
            dpg.delete_item(self.combo_id)
        l = [window.entity.name for window in window_list if window.entity.name not in self.dict.values()]
        self.combo_id = dpg.add_combo(l, label="+", callback=self.add_button, parent=self.group_id)
            
    # Add default key and empty value.
    def add_button(self, sender, app_data):
        i = 1
        keys = list(self.dict.keys())
        while(i in keys or str(i) in keys):
            i += 1
        self.dict[i] = app_data
        self.renew_keys()
        self.render()
        
        
                   
# Windows for agents.
class Agent_Window(Entity_Window): 
    
    def __init__(self, entity, width = 525, x_pos = agent_start_x, y_pos = 0):  
        super().__init__(entity, width, x_pos, y_pos)
        
    # Override type_to_window method for Agent-specific behavior.
    def type_to_window(self, window):
        with dpg.group(horizontal=True):
            dpg.add_text("Description")
            dpg.add_input_text(label="", default_value=self.entity.description, tag=self.n("description"))
        with dpg.group(horizontal=True):
            dpg.add_text("Refresh")
            dpg.add_input_text(label="", default_value=self.entity.refresh, width=25, tag=self.n("refresh"))
            dpg.add_text("Fate Points")
            dpg.add_input_text(label="", default_value=self.entity.fate_points, width=25, tag=self.n("fate_points"))
        with dpg.group(horizontal=True):
            for name, value in self.entity.approaches.items():
                dpg.add_text(name)
                dpg.add_input_text(label="", default_value=value, width=25, tag=self.n("approach_{}".format(name)))
        
        aspects_group = dpg.add_group()
        self.aspects = Window_Dict(
            window_group = aspects_group,
            label = "Aspects", 
            entity_name = self.entity.name, 
            keys = list(self.entity.aspects.keys()), 
            values = list(self.entity.aspects.values()), 
            actually_list = True)
            
        stunts_group = dpg.add_group()
        self.stunts = Window_Dict(
            window_group = stunts_group,
            label = "Stunts", 
            entity_name = self.entity.name, 
            keys = list(self.entity.stunts.keys()), 
            values = list(self.entity.stunts.values()), 
            actually_list = True)
            
        stress_group = dpg.add_group()
        self.stress = Window_Dict(
            window_group = stress_group,
            label = "Stress", 
            entity_name = self.entity.name, 
            keys = list(self.entity.stress.keys()), 
            values = list(self.entity.stress.values()), 
            actually_list = False)
            
        consequencess_group = dpg.add_group()
        self.consequences = Window_Dict(
            window_group = consequencess_group,
            label = "Consequences", 
            entity_name = self.entity.name, 
            keys = list(self.entity.consequences.keys()), 
            values = list(self.entity.consequences.values()), 
            actually_list = False)
                  
    # Override window_to_entity method for Agent-specific behavior.
    def window_to_entity(self):
        self.entity.description = dpg.get_value(self.n("description"))
        self.entity.refresh = dpg.get_value(self.n("refresh"))
        self.entity.fate_points = dpg.get_value(self.n("fate_points"))
        for name in approach_list:
            self.entity.approaches[name] = dpg.get_value(self.n("approach_{}".format(name)))
        self.entity.aspects = self.aspects.give_dict()
        self.entity.stunts = self.stunts.give_dict()
        self.entity.stress = self.stress.give_dict()
        self.entity.consequences = self.consequences.give_dict()
        self.entity.autoload = dpg.get_value(self.n("autoload_checkbox"))
        self.entity.save()
    
                        
               
# Windows for obstacles.
class Obstacle_Window(Entity_Window): 
    
    def __init__(self, entity, width = 225, x_pos = obstacle_start_x, y_pos = 0):  
        super().__init__(entity, width, x_pos, y_pos)
        
    # Override type_to_window method for Obstacle-specific behavior.
    def type_to_window(self, window):
        with dpg.group(horizontal=True):
            dpg.add_text("Now")
            dpg.add_input_text(label="", default_value=self.entity.now, width=25, tag=self.n("now"))
            dpg.add_text("Win")
            dpg.add_input_text(label="", default_value=self.entity.win, width=25, tag=self.n("win"))
            dpg.add_text("Lose")
            dpg.add_input_text(label="", default_value=self.entity.lose, width=40, tag=self.n("lose"))
  
    # Override window_to_entity method for Obstacle-specific behavior.
    def window_to_entity(self):
        self.entity.now = dpg.get_value(self.n("now"))
        self.entity.win = dpg.get_value(self.n("win"))
        self.entity.lose = dpg.get_value(self.n("lose"))
        self.entity.autoload = dpg.get_value(self.n("autoload_checkbox"))
        self.entity.save()
    
    

# Windows for zones.
class Zone_Window(Entity_Window): 
    
    def __init__(self, entity, width = 225, x_pos = zone_start_x, y_pos = 0):  
        super().__init__(entity, width, x_pos, y_pos)
        
    # Override type_to_window method for Zone-specific behavior.
    def type_to_window(self, window):
        
        agents_group = dpg.add_group()
        self.agents = Window_Dropdown(
            window_group = agents_group,
            label = "Agents", 
            entity_name = self.entity.name, 
            keys = [], 
            values = self.entity.agent_names)
        
        obstacles_group = dpg.add_group()
        self.obstacles = Window_Dropdown(
            window_group = obstacles_group,
            label = "Obstacles", 
            entity_name = self.entity.name, 
            keys = [], 
            values = self.entity.obstacle_names)
          
    # Override window_to_entity method for Zone-specific behavior.
    def window_to_entity(self):
        self.entity.agent_names = self.agents.give_dict()
        self.entity.obstacle_names = self.obstacles.give_dict()
        self.entity.autoload = dpg.get_value(self.n("autoload_checkbox"))
        self.entity.save()