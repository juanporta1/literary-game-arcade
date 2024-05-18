import arcade
import arcade.color
import arcade.color
import arcade.gui
from player import Player
from pauseMenu import PauseMenu
import maps as Maps
import questions
import random
from questionsMenu import QuestionMenu
from room import Room


class Game(arcade.View):
    def __init__(self,window,menu):
        super().__init__(window)
        self.player = Player(0,0,0)
        self.rooms = [Room(self.window,Maps.initalMap,3600,300,4,menu,questions.levelOne,self.player,self),Room(self.window,Maps.initalMap,2500,500,4,menu,questions.levelOne,self.player,self)]
        self.actualLevel = 0
        self.currentRoom = self.rooms[self.actualLevel]
        
        
    def on_update(self, delta_time: float):
        if True:
            self.window.show_view(self.currentRoom)
        

    
    
    