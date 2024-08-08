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
        
        
        self.textView = TextView(self.window,'Has recorrido el castillo, encontrando los libros ocultos y respondiendo cada pregunta con éxito. Al final del último desafío, un haz de luz ilumina la sala y aparece un mensaje: "Eres digno del conocimiento de Alden. Usa esta sabiduría con honor y responsabilidad." El castillo empieza a desvanecerse, revelando un pergamino antiguo que había estado escondido. En él, encuentras el verdadero propósito del desafío: Alden buscaba un guardián digno de su conocimiento, alguien que pudiera preservar y compartir la sabiduría con el mundo.',menu)
        
    def on_update(self, delta_time: float):
        self.window.show_view(self.textView)
            
        
        
        
    
    
    