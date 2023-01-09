from game import Game, Object, w, h

game = Game()
    
    

class Menu:
    
    def __init__(self, ID, list_of_rows = [], bg_color = (50, 50, 50), space_between = .05, saving = False):
        
        self.ID = ID
        
        self.cancel = Object(
            "CLOSE", color = (255, 0, 0), text_color = (0,0,0),
            double_click = self.reset_and_close if saving else self.save_and_close)
        list_of_rows.append([self.cancel])
        self.saving = saving
        if(self.saving):
            self.save = Object(
                "SAVE",   color = (0, 255, 0), text_color = (0,0,0), double_click = self.save_and_close)
            list_of_rows[-1].append(self.save)
        
        for row in list_of_rows:
            for obj in row:
                obj.ID = self.ID + " " + obj.ID
                        
        self.original = [[obj.copy() for obj in row] for row in list_of_rows]
        self.current  = [[obj.copy() for obj in row] for row in list_of_rows]
        self.saved    = [[obj.copy() for obj in row] for row in list_of_rows]
        self.active   = [[obj.copy() for obj in row] for row in list_of_rows]
        
        self.bg = Object(self.ID + " bg", color = bg_color)
        self.space_between = space_between
        self.x_start = space_between ; self.x_end = w/h - space_between
        self.y_start = space_between ; self.y_end = 1 - space_between
        self.bg.pos, self.bg.size = self.pos_size()
        
    def pos_size(self, x = None, y = None, len_row = "bg"):
        if(len_row == "bg"):
            pos = (self.x_start, self.y_start)
            size = (self.x_end - self.x_start, self.y_end - self.y_start)
            return(pos, size)
        y_dif = (self.y_end - self.y_start - self.space_between) / len(self.active)
        x_dif = (self.x_end - self.x_start - self.space_between) / len_row
        pos = (self.x_start + x * x_dif + self.space_between, self.y_start + y * y_dif + self.space_between)
        size = (x_dif - self.space_between, y_dif - self.space_between)
        return(pos, size)
        
    def assemble_menu(self):  
        self.just_close()
        print("\n\n")
        game.objects.append(self.bg)
        for y, row in enumerate(self.active):
            for x, obj in enumerate(row):
                obj.pos, obj.size = self.pos_size(x, y, len(row))
                game.objects.append(obj)
                print("Adding ", obj.ID, end = ".   ")
                
    def adjust_thing(self):
        pass # For Superclasses
        
    def just_save(self):
        self.saved = [[obj.copy() for obj in row] for row in self.active]
        self.adjust_thing()
        
    def just_reset(self):
        self.current = [[obj.copy() for obj in row] for row in self.saved]
        self.active = [[obj.copy() for obj in row] for row in self.saved]
        
    def totally_reset(self):
        self.current = [[obj.copy() for obj in row] for row in self.original]
        self.saved   = [[obj.copy() for obj in row] for row in self.original]
        self.active  = [[obj.copy() for obj in row] for row in self.original]
                
    def just_close(self):
        print("\n\n")
        game.remove_object(self.bg.ID)
        for row in self.current:
            for obj in row:
                print("Removing ", obj.ID, end = ".   ")
                game.remove_object(obj.ID)
                
    def save_and_close(self):
        self.just_save()
        self.just_close()
        
    def reset_and_close(self):
        self.just_reset()
        self.just_close()
        
    def __str__(self):
        s = "\n\n"
        for row in self.saved:
            for obj in row:
                s += obj.__str__() + ", "
            s += "\n"
        return(s)