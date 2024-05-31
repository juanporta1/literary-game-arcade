import arcade
import arcade.color
import arcade.color
import arcade.gui
from Player import Player
from PauseMenu import PauseMenu
import maps as Maps
import questions
import random
from questionsMenu import QuestionMenu
from room import Room
import globalVars
from textView import TextView

class Game(arcade.View):
    global globalVars
    def __init__(self,window,menu):
        super().__init__(window)
        commonQuestion = arcade.load_texture("Assets/Sprites/QuestionMenu/commonQuestion.png")
        keysLevelOne = [{
                "filename": "Assets/Sprites/UI/fillHeart.png",
                "center_x": 4415,
                "center_y": 310,
                "questionMenu": QuestionMenu(self.window,questions.levelOne,None,menu,5,3,boxTexture=commonQuestion),
                "scale": 1
            },{
                "filename": "Assets/Sprites/UI/fillHeart.png",
                "center_x": 3000,
                "center_y": 400,
                "questionMenu": QuestionMenu(self.window,questions.levelOne,None,menu,5,3,boxTexture=commonQuestion),
                "scale": 1
            }
        ]
        
        keysLevelTwo = [{
                "filename": "Assets/Sprites/UI/emptyHeart.png",
                "center_x": 5000,
                "center_y": 200,
                "questionMenu": QuestionMenu(self.window,questions.levelOne,None,menu,1,1,boxTexture=commonQuestion),
                "scale": 1
            },{
                "filename": "Assets/Sprites/UI/emptyHeart.png",
                "center_x": 2500,
                "center_y": 400,
                "questionMenu": QuestionMenu(self.window,questions.levelOne,None,menu,1,1,boxTexture=commonQuestion),
                "scale": 1
            }
        ]
        
        
        self.room1 = Room(self.window,Maps.initalMap,3600,300,4,menu,questions.levelOne,self,keysLevelOne)
        self.room2 = Room(self.window,Maps.initalMap,2500,500,4,menu,questions.levelOne,self,keysLevelTwo)  
        self.firstText = TextView(self.window,"Hola muy buenas tardes, este es el primer texto de mi view, utilizo este texto para ver si funciona la creacion de estos menues",self.room1)
        self.room1.previousRoom = self.room2
        self.room1.nextRoom = self.room2
        self.room2.previousRoom = self.room1
        self.room2.nextRoom = self.room1
        
    def on_update(self, delta_time: float):
        self.window.show_view(self.firstText)
            
        
        
        
    
    
    