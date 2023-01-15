from random import randint

from game import w, h
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

def roll():
    dice = []
    for i in range(4):
        die_val = randint(-1,1)
        dice.append(game.add_object("die_{}".format(i+1), name = "", text = "{}".format("+" if die_val == 1 else "-" if die_val == -1 else ""), 
                                    color = (0,255,0), text_color = (0, 0, 0), pos = (.01 + .11*(i+1), 1 - .11), size = (.1, .1)))
    dice.append(game.add_object("PLUS", color = (255,255,255), text_color = (0, 0, 0), pos = (.56, 1 - .11), size = (.2, .1), text = "0", typeable = True))
    dice.append(game.add_object("EQUAL", "", color = (0,0,255), text_color = (255, 255, 255), pos = (.77, 1 - .11), size = (.2, .1)))
    dice.append(game.add_object("STOP", color = (0,0,0), text_color = (255, 255, 255), pos = (.01, 1 - .11), size = (.1, .1)))
    
    def remove_dice():
        for die in dice:
            game.remove_object(die.ID)
            
    def sum_dice():
        value = 0
        for die in dice[:4]:
            if(die.text == "+"): value += 1 
            if(die.text == "-"): value -= 1
        try:    value += int(dice[4].text) 
        except: pass
        dice[-2].text = "= " + str(value)
    
    dice[-2].constant = sum_dice
    dice[-1].double_click = remove_dice
                 

    
new = game.add_object("NEW", color = (0,0,0), text_color = (255, 255, 255), pos = (.01, .01), size = (.1, .1), 
             double_click = New_Thing_Menu().assemble)
load = game.add_object("LOAD", color = (0,0,0), text_color = (255, 255, 255), pos = (.12, .01), size = (.1, .1), 
             double_click = load_this)
roll = game.add_object("ROLL", color = (0,0,0), text_color = (255, 255, 255), pos = (w/h - .11, 1 - .11), size = (.1, .1), 
             double_click = roll)

game.run()