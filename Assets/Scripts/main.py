import arcade
from Menu import MenuView
import pygame


class Window(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)

if __name__ == '__main__':
    
    window = Window(1280,720,"Habia una vez...")
    
    window.show_view(MenuView(window)) 
    arcade.run()