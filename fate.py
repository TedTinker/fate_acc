#%% 

# Thoughts:
    # Zone windows should be arrowed right even with collapsed windows. 
    # Lists should be updated without closing the user's selection.
    # Get colors working.
    
import os
import dearpygui.dearpygui as dpg
import threading

from entities import Agent, Obstacle, Zone
from windows import Agent_Window, Obstacle_Window, Zone_Window



# Main window and environment for Fate.
class Fate_Env:
    
    def __init__(self):

        self.agent_windows = []
        self.obstacle_windows = []
        self.zone_windows = []
        self.dialog_id = None
        
        dpg.create_context()
        dpg.create_viewport(title='Fate', width=1920, height=1080)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        
        with dpg.window(
                label="Main Window", 
                no_title_bar=True, 
                no_resize=True, 
                no_move=True,
                width = 1920,
                height = 1080,
                tag="Primary Window") as self.main_window:
            dpg.set_primary_window("Primary Window", True)
            with dpg.child_window(label="Options", width = 310, height = 150):
                with dpg.group(horizontal=True) as self.load_group:
                    dpg.add_text("Load ")
                    self.load_id = dpg.add_combo([], label="", callback=self.load_dialog)
                with dpg.group(horizontal=True) as self.save_group:
                    dpg.add_text("Save ")
                    self.save_id = dpg.add_combo([], label="", callback=self.save_dialog)
                with dpg.group(horizontal=True) as self.close_group:
                    dpg.add_text("Close")
                    self.close_id = dpg.add_combo([], label="", callback=self.close_dialog)
                with dpg.group(horizontal=True):
                    self.add_agent_name_id = dpg.add_input_text(label="", default_value="Name", width=200, tag="add_agent_name")
                    dpg.add_button(label="New Agent", callback=self.new_entity, tag="new_agent_button")
                with dpg.group(horizontal=True):
                    self.add_obstacle_name_id = dpg.add_input_text(label="", default_value="Name", width=200, tag="add_obstacle_name")
                    dpg.add_button(label="New Obstacle", callback=self.new_entity, tag="new_obstacle_button")
                with dpg.group(horizontal=True):
                    self.add_zone_name_id = dpg.add_input_text(label="", default_value="Name", width=200, tag="add_zone_name")
                    dpg.add_button(label="New Zone", callback=self.new_entity, tag="new_zone_button")

        self.arrows = []
        self.drawing_layer = None

        for file in os.listdir("entities"):
            if(file.endswith("(autoload).txt")):
                self.load_file(file)
                
        self.maintain_background()
        self.maintain_zone_options()
        self.maintain_zone_arrows()
                                        
        dpg.start_dearpygui()
        dpg.destroy_context()
        
    # Make new agent/obstacle/zone. 
    def new_entity(self, sender, app_data, user_data):
        if sender == "new_agent_button":
            new_name = dpg.get_value(self.add_agent_name_id)
            if(new_name in [window.entity.name for window in self.agent_windows]):
                print("Existing agent.")
            else:
                self.agent_windows.append(Agent_Window(Agent(name = new_name)))
            dpg.set_value(self.add_agent_name_id, "Name")
        if sender == "new_obstacle_button":
            new_name = dpg.get_value(self.add_obstacle_name_id)
            if(new_name in [window.entity.name for window in self.obstacle_windows]):
                print("Existing obstacle.")
            else:
                self.obstacle_windows.append(Obstacle_Window(Obstacle(name = new_name)))
            dpg.set_value(self.add_obstacle_name_id, "Name")
        if sender == "new_zone_button":
            new_name = dpg.get_value(self.add_zone_name_id)
            if(new_name in [window.entity.name for window in self.zone_windows]):
                print("Existing zone.")
            else:
                self.zone_windows.append(Zone_Window(Zone(name = new_name)))
            dpg.set_value(self.add_zone_name_id, "Name")
        
    # Keep background in back.
    def maintain_background(self):
        #dpg.bring_to_back(self.main_window) # Not a real thing?
        threading.Timer(.1, self.maintain_background).start()
                
    # Keep zone-lists correct. This should also do the env's load/save/close lists!
    def maintain_zone_options(self):
        for zone_window in self.zone_windows:
            zone_window.agents.add_add_button(self.agent_windows)
            zone_window.obstacles.add_add_button(self.obstacle_windows)
        threading.Timer(5, self.maintain_zone_options).start()
        used_files = []
        unused_files = []
        for file in os.listdir("entities"):
            entity_type = file.split(" ")[0]
            name = file.replace("(autoload)", "")[:-4]
            name = name.replace(entity_type, "").strip()
            if(name in [window.entity.name for window in self.agent_windows + self.obstacle_windows + self.zone_windows]): 
                used_files.append(name)
            else:
                unused_files.append(file)
        for window in self.agent_windows + self.obstacle_windows + self.zone_windows:
            if(not window.entity.name in used_files):
                used_files.append(window.entity.name)
        used_files.sort()
        unused_files.sort()
        dpg.delete_item(self.load_id)
        self.load_id = dpg.add_combo(unused_files, label="", callback=self.load_dialog, parent = self.load_group)
        dpg.delete_item(self.save_id)
        self.save_id = dpg.add_combo(["All"] + used_files, label="", callback=self.save_dialog, parent = self.save_group)
        dpg.delete_item(self.close_id)
        self.close_id = dpg.add_combo(["All"] + used_files, label="", callback=self.close_dialog, parent = self.close_group)
        
    # Keep zone-arrows correct.
    def maintain_zone_arrows(self):
        self.arrows.clear()
        for zone_window in self.zone_windows:
            #zone_window_state = dpg.get_item_state(zone_window.window)
            #zone_window_collapsed = zone_window_state['collapsed']
            for window in zone_window.agents.window_list:
                #window_state = dpg.get_item_state(window.window)
                #window_collapsed = window_state['collapsed']
                #if not zone_window_collapsed and not window_collapsed:
                self.add_arrow(zone_window, window)
            for window in zone_window.obstacles.window_list:
                #window_state = dpg.get_item_state(window.window)
                #window_collapsed = window_state['collapsed']
                #if not zone_window_collapsed and not window_collapsed:
                self.add_arrow(zone_window, window)
        self.draw_arrows()
        threading.Timer(.1, self.maintain_zone_arrows).start()
    
    # Create an arrow. (Doesn't work well with collapsed windows.)
    def add_arrow(self, window_1, window_2):
        try:
            start_x = dpg.get_item_pos(window_1.window)[0] + dpg.get_item_width(window_1.window) / 2
            start_y = dpg.get_item_pos(window_1.window)[1] + dpg.get_item_height(window_1.window) / 2
            end_x = dpg.get_item_pos(window_2.window)[0] + dpg.get_item_width(window_2.window) / 2
            end_y = dpg.get_item_pos(window_2.window)[1] + dpg.get_item_height(window_2.window) / 2
        except:
            start_x = start_y = end_x = end_y = 0
        self.arrows.append(((start_x, start_y), (end_x, end_y), window_1.entity.color))
        
    # Draw arrows from window to window in the main window.
    def draw_arrows(self):
        if self.drawing_layer and dpg.does_item_exist(self.drawing_layer):
            dpg.delete_item(self.drawing_layer)
        with dpg.draw_layer(parent=self.main_window) as self.drawing_layer:
            for start_pos, end_pos, color in self.arrows:
                dpg.draw_arrow(p1=start_pos, p2=end_pos, color=color + (255,), thickness=2)

    # Load entity from file. 
    def load_file(self, file):
        file = file.replace("(autoload)", "")[:-4]
        words = file.split()
        entity_type = words[0].strip()
        name = ' '.join(word for word in words[1:]).strip()
        if(entity_type == "agent"):
            entity = Agent(name = name)
            entity.load()
            self.agent_windows.append(Agent_Window(entity = entity))
        if(entity_type == "obstacle"):
            entity = Obstacle(name = name)
            entity.load()
            self.obstacle_windows.append(Obstacle_Window(entity = entity))
        if(entity_type == "zone"):
            entity = Zone(name = name)
            entity.load()
            self.zone_windows.append(Zone_Window(entity = entity))
            
    # Select file to load entity. 
    def load_dialog(self, sender, app_data):
        file = app_data
        file = file.split("\\")[-1]
        self.load_file(file)
            
    # Save entities from windows to text files.
    def save_dialog(self, sender, app_data):
        for entity_window in self.agent_windows + self.obstacle_windows + self.zone_windows:
            if(entity_window.entity.name == app_data or app_data == "All"):
                entity_window.window_to_entity()
                
    # Save and remove entity and window.
    def close_window(self, entity_window):
        entity_window.window_to_entity()
        dpg.delete_item(entity_window.window)
        del(entity_window)
            
    # Save and remove entitiy and window.
    def close_dialog(self, sender, app_data):
        print("Closing", app_data)
        new_agent_windows = []
        new_obstacle_windows = []
        new_zone_windows = []
        for entity_window in self.agent_windows:
            if(entity_window.entity.name != app_data and app_data != "All"):
                new_agent_windows.append(entity_window)
            else:
                self.close_window(entity_window)
        for entity_window in self.obstacle_windows:
            if(entity_window.entity.name != app_data and app_data != "All"):
                new_obstacle_windows.append(entity_window)
            else:
                self.close_window(entity_window)
        for entity_window in self.zone_windows:
            if(entity_window.entity.name != app_data and app_data != "All"):
                new_zone_windows.append(entity_window)
            else:
                self.close_window(entity_window)
        self.agent_windows = new_agent_windows
        self.obstacle_windows = new_obstacle_windows 
        self.zone_windows = new_zone_windows
                
                
        
        
        
if __name__ == "__main__":
    fate_env = Fate_Env()