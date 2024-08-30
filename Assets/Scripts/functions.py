import arcade
import globalVars
def createAnimationList(rute, quantity):
        list = []
        for i in range(quantity):
            image = arcade.load_texture(f"{rute}{i}.png")
            list.append(image)
        return list
    
def reverseCreateAnimationList(rute,quantity):
    list = []
    for i in range(quantity,-1,-1):
        image  = arcade.load_texture(f"{rute}{i}.png")
        list.append(image)
    return list

def scaleInt(n):
    global globalVars
    return int((n*globalVars.ACTUAL_WIDTH) / globalVars.DEFAULT_WIDTH)

def scaleFloat(n):
    global globalVars
    return (n*globalVars.ACTUAL_WIDTH) / globalVars.DEFAULT_WIDTH
