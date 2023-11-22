# Default approches in Fate: Accelerated. Feel free to change them. 
#approach_list = ["Careful", "Clever", "Flashy", "Forceful", "Quick", "Sneaky"]
approach_list = ["Careful", "Clever", "Flashy", "Forceful", "Quick", "Sneaky"]



# Function for printing name-value pairs from dictionaries with colons aligned.
def align_colons(d):
    (names,values) = zip(*d.items()) 
    max_length = max(len(str(name)) for name in names)      
    aligned_text = ""
    for i, (name, value) in enumerate(zip(names, values)):
        aligned_text += "\n\t"
        # Pad name with spaces to align colons
        aligned_text += "{:<{width}} : {}".format(name, value, width=max_length)
    return aligned_text
    
        
        
# How to load entity-files.
def get_lines(entity_type, name):
    # If file autoloads, (autoload) is added to file name.
    f   = r"entities/{} {}.txt".format(           entity_type, name)
    f_a = r"entities/{} {} (autoload).txt".format(entity_type, name) 
    try:
        with open(f) as file:       lines = file.readlines()
    except:
        try:
            with open(f_a) as file: lines = file.readlines()
        except:
            print("\nCouldn't load {}.\n".format(f))
            lines = None
    return(lines)



# Inputs may or may not be integers. 
def maybe_int(this):
    try: this = int(this)
    except: pass 
    return(this)