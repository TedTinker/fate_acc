from menu import game
from things import Thing
from thing_menu import Thing_Menu, New_Thing_Menu


                
def load_this():
    thing = Thing(load = True)
    if(thing.failed): return
    try:
        thing_button = game.add_object(thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), draggable = True)
        thing_menu = Thing_Menu(thing, thing_button)
        thing_button.double_click = thing_menu.assemble
        thing_button.right_click = get_right_click_this(thing_button)
        print("\nLoaded:")
        print(thing)
    except: pass
    
    
    
def get_right_click_this(obj):
    
    def right_click_this():
        positions = [(obj.pos[0] + obj.size[0], obj.pos[1] + obj.size[1] + .11*y) for y in range(3)]
        done = game.add_object("DONE", color = (200,200,200), text_color = (0, 0, 0), pos = positions[0], size = (.5, .1))
        remove = game.add_object("REMOVE {}".format(obj.name), color = (50,50,50), text_color = (0, 0, 0), pos = positions[1], size = (.5, .1))
        
        buttons = [done, remove]
        
        def get_remove_these_and(then = lambda : None):
            def remove_these_and():
                for obj in buttons: game.remove_object(obj.ID)
                then()
            return(remove_these_and)
        
        remove.double_click = get_remove_these_and(lambda : game.remove_object(obj.ID)) # game.remove_object(obj.ID)
        done.double_click = get_remove_these_and()
    return(right_click_this)


    
new = game.add_object("NEW", color = (0,0,0), text_color = (255, 255, 255), pos = (.01, .01), size = (.1, .1), 
             double_click = New_Thing_Menu().assemble)
load = game.add_object("LOAD", color = (0,0,0), text_color = (255, 255, 255), pos = (.12, .01), size = (.1, .1), 
             double_click = load_this)

game.run()