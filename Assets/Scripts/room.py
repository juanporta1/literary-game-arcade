import arcade
from Player import Player

class Room(arcade.Scene):
    
    def __init__(self,tilemap):
        super().__init__()
        self.from_tilemap(tilemap)
        
        
        
        