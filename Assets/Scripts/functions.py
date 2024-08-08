import arcade

def createAnimationList(rute, quantity):
        list = []
        for i in range(quantity):
            image = arcade.load_texture(f"{rute}{i}.png")
            list.append(image)
        return list

