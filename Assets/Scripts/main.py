import arcade
from Menu import MenuView   
from Game import Game
import globalVars


class Window(arcade.Window):
    global globalVars
    def __init__(self,width,height,title,fullscreen=False):
        super().__init__(width,height,title,fullscreen=fullscreen)
        globalVars.ACTUAL_WIDTH = self.width
        globalVars.ACTUAL_HEIGHT = self.height


if __name__ == '__main__':
    
    window = Window(1280,720,"Habia una vez...")
    menu = MenuView(window)
    
    window.show_view(menu)
    arcade.run()