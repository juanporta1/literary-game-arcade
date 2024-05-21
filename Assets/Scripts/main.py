import arcade
from Menu import MenuView
import pygame

        
if __name__ == '__main__':
    
    window = arcade.Window(1280,720,"Habia una vez...")
    
    window.show_view(MenuView(window))
    arcade.run()