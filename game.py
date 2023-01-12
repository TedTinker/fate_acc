import pygame
from pygame.locals import RESIZABLE, VIDEOEXPOSE

from time import time

import pyautogui
w, h = pyautogui.size()



class Object:
    
    def __init__(
            self, ID, name = None, color = (0,0,0), text_color = None, pos = (0, 0), size = (1, 1), text = "", 
            typeable = False, draggable = False, click = lambda : None, double_click = lambda : None):
        
        self.ID = ID ; self.name = name if name != None else ID
        self.color = color ; self.text_color = text_color 
        self.obj = pygame.Surface((1,1)) ; self.obj.fill(self.color)
        
        self.pos = pos ; self.size = size
        if(self.pos[0] == "center"): self.pos = ((w/h - self.size[0])/2, self.pos[1])
        if(self.pos[1] == "center"): self.pos = (self.pos[0], (1 - self.size[1])/2)
        
        self.text = text ; self.typeable = typeable ; self.text_box = None ; self.add_text()
        self.draggable = draggable ; self.click = click ; self.double_click = double_click
        self.clicked_on = False ; self.last_time_clicked = None
        self.being_dragged = False ; self.being_typed = False
        
    def add_text(self, font = "arial"):
        if(self.text_color == None): return
        else:
            name_empty = self.name.replace(" ", "") == ""
            text_empty = self.text.replace(" ", "") == ""
            if(name_empty and text_empty): text = " "
            elif(name_empty): text = self.text 
            elif(text_empty): text = self.name 
            else:             text = self.name + " : " + self.text
        font = pygame.font.SysFont(font, 1000)
        self.text_box = font.render(text, False, self.text_color)
        
    def on_click(self):
        self.click()
        
    def on_double_click(self):
        self.double_click()
        
    def copy(self):
        obj_copy = Object(
            ID = self.ID, name = self.name, color = self.color, text_color = self.text_color, 
            pos = self.pos, size = self.size, text = self.text, draggable = self.draggable, 
            typeable = self.typeable, click = self.click, double_click = self.double_click)
        return(obj_copy)
    
    def __str__(self):
        return("{}: {}".format(self.name, self.text))
        


class Game:
    
    def __init__(self, size = [w//2, h//2]):
        pygame.init()
        self.paras = {"size" : size} 
        self.objects = [] 
        self.bg = self.add_object("bg", "bg", color = (255, 255, 255), size = (w/h, 1), pos = (0, 0))
        self.screen = pygame.display.set_mode(self.paras["size"], RESIZABLE)
        
    def add_object(self, *args, **kwargs):
        obj = Object(*args, **kwargs)
        self.objects.append(obj)
        return(obj)
    
    def remove_object(self, ID):
        pop_these = []
        for i, obj in enumerate(self.objects):
            if obj.ID == ID:
                pop_these.append(i)
        for i in reversed(pop_these): self.objects.pop(i) 
        
    def obj_size(self, obj):
        ww, wh = self.paras["size"]
        wider = wh/ww < h/w
        w_size = wh if wider else ww*h/w
        size = [s*w_size for s in obj.size]
        return(size)
    
    def obj_pos(self, obj):
        ww, wh = self.paras["size"]
        wider = wh/ww < h/w
        w_size = wh if wider else ww*h/w
        sw, sh = self.obj_size(self.bg)
        pos  = [p*w_size for p in obj.pos]
        if(wider): pos[0] += (ww - sw)/2
        else:      pos[1] += (wh - sh)/2
        return(pos)
    
    def obj_click(self, obj, pos):
        size = self.obj_size(obj) ; obj_pos  = self.obj_pos(obj)
        if(pos[0] > obj_pos[0] and pos[0] < obj_pos[0] + size[0]):
            if(pos[1] > obj_pos[1] and pos[1] < obj_pos[1] + size[1]):
                return(True)
        return(False)
    
    def render(self, obj):
        size = self.obj_size(obj) ; pos = self.obj_pos(obj)
        OBJ = pygame.transform.scale(obj.obj, size)
        self.screen.blit(OBJ, pos)
        obj.add_text()
        if(obj.text_box != None):
            x_1, y_1, x_2, y_2 = obj.text_box.get_rect()
            x = x_2 - x_1 ; y = y_2 - y_1 ; text_ratio = x / y
            x_change = size[0] / x ; y_change = size[1] / y ; change = max([x_change, y_change])
            if(change == x_change): 
                text_size = (size[1] * text_ratio, size[1]) 
                text_pos = (pos[0] + size[0]/2 - text_size[0]/2, pos[1])
            else:                   
                text_size = (size[0], size[0] / text_ratio) 
                text_pos = (pos[0], pos[1] + size[1]/2 - text_size[1]/2)
            # If possible, add /n to make new lines
            text = pygame.transform.scale(obj.text_box, text_size)
            self.screen.blit(text, text_pos)
        
    def run(self):
        running = True ; frames = 0
        old_pos = pygame.mouse.get_pos()
        while running:
            frames += 1 ; pos = pygame.mouse.get_pos()
            
            for obj in self.objects: 
                self.render(obj)
            
            events = pygame.event.get()
            for event in events:
                
                if event.type == pygame.QUIT: running = False
                if event.type == VIDEOEXPOSE: 
                    pygame.display.update()
                    self.paras["size"] = self.screen.get_size()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for obj in reversed(self.objects):
                        obj.being_typed = False
                        if(self.obj_click(obj, pos)):
                            obj.clicked_on = True
                            if(obj.typeable): obj.being_typed = True
                            break
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    for obj in reversed(self.objects):
                        if(self.obj_click(obj, pos) and not obj.being_dragged):
                            obj.on_click() ; clicked_this = obj
                            if(obj.last_time_clicked != None and time() - obj.last_time_clicked <= .5): 
                                obj.on_double_click()
                            obj.last_time_clicked = time()
                            break
                    for obj in reversed(self.objects): 
                        obj.clicked_on = False ; obj.being_dragged = False
                        if(clicked_this != obj): obj.last_time_clicked = None
                        
                if event.type == pygame.KEYDOWN:
                    key = event.unicode
                    for obj in reversed(self.objects):
                        if(obj.being_typed):
                            if(event.key == pygame.K_RETURN): 
                                obj.being_typed = False ; break
                            if(event.key == pygame.K_BACKSPACE):
                                obj.text = obj.text[:-1]
                            else:
                                obj.text += key
                            break
                
            for obj in reversed(self.objects):
                if(obj.draggable and obj.clicked_on):
                    change_x = pos[0] - old_pos[0] ; change_y = pos[1] - old_pos[1]
                    bg_size = self.obj_size(self.bg)
                    change_x /= bg_size[1] ; change_y /= bg_size[1]
                    obj.pos = (obj.pos[0] + change_x, obj.pos[1] + change_y)
                    if(change_x > 0 or change_y > 0): obj.being_dragged = True
                                     
            old_pos = pos
            pygame.display.flip()
        pygame.quit()
        
        
        
        
        
        
        
        
if __name__ == "__main__":
    
    def new_button():
        new_button = Object("REMOVE", color = (255, 1, 1),  text_color = (0,0,0), size = (.1, .1), pos = (.5, .5),
                     click = lambda: print("CLICKED"), double_click = lambda: print("DOUBLE CLICKED"))
        new_button.double_click = get_remove_button("REMOVE")
        game.objects.append(new_button)
        pass
    
    def get_remove_button(name):
        def remove_button():
            game.remove_object(name)
        return(remove_button)




    game = Game()
    #click = game.add_object("CLICK", color = (255, 1, 1), size = (.1, .1), pos = (.1, .1), text_color = (0,0,0),
    #             click = lambda: print("CLICKED"), double_click = lambda: print("DOUBLE CLICKED"))
    #drag = game.add_object("DRAG", color = (1, 255, 1), size = (.1, .1), pos = (.2, .2), text_color = (0,0,0),
    #              draggable = True, click = lambda: print("CLICKED"), double_click = lambda: print("DOUBLE CLICKED"))
    typing = game.add_object("TYPE", color = (1, 1, 255), size = (1, .1), pos = (.3, .3), text_color = (0,0,0),
                  typeable = True, click = lambda: print("CLICKED"), double_click = lambda: print("DOUBLE CLICKED"))
    #new = game.add_object("NEW", color = (255, 1, 255), size = (.1, .1), pos = (.4, .4),  text_color = (0,0,0),
    #              click = lambda: print("CLICKED"), double_click = new_button)
    game.run()