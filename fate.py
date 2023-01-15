from menu import game
from things import Thing
from thing_menu import Thing_Menu, New_Thing_Menu, get_right_click_this


                
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


    
new = game.add_object("NEW", color = (0,0,0), text_color = (255, 255, 255), pos = (.01, .01), size = (.1, .1), 
             double_click = New_Thing_Menu().assemble)
load = game.add_object("LOAD", color = (0,0,0), text_color = (255, 255, 255), pos = (.12, .01), size = (.1, .1), 
             double_click = load_this)

game.run()