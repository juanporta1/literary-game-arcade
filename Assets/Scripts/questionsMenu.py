import arcade
import arcade.gui
import random
from pauseMenu import PauseMenu
from player import Player

class QuestionMenu(arcade.View):
    def __init__(self, window, questions,gameView,menuView,player: Player):
        super().__init__(window)
        self.usedQuestions = []
        self.player = player
        self.questions = questions
        self.gameView = gameView
        self.menuView = menuView
        self.pause = PauseMenu(self.window,self,self.menuView)
        self.menu = self.questionsMenu(self.questions)
    def questionsMenu(self,questions):
        
        randomNumber = random.randint(0,len(questions)-1)
        while self.usedQuestions.count(randomNumber) != 0:
            randomNumber = random.randint(0,len(questions))
            
        question = questions[randomNumber]["question"]
        responses = questions[randomNumber]["responses"]
        correct = responses[0]
        random.shuffle(responses)
        self.correct = responses.index(correct)
        self.usedQuestions.append(randomNumber)
        
        
        guiMenu = arcade.gui.UIManager()

        principalBox = arcade.gui.UIBoxLayout()
        
        questionStyle = {
            "font_name": "Retro Gaming",
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed" : None,
            "font_color_pressed": arcade.color.WHITE
        }
        responsesStyle = {
            "font_name": "Retro Gaming"
        }
        questionBox = arcade.gui.UIFlatButton(text=question,width=1230,height=200,style=questionStyle)
        
        bgBox = arcade.gui.UIBorder(child=questionBox)
        
        
        principalBox.add(bgBox)
        
        responsesBoxOne = arcade.gui.UIBoxLayout(vertical=False)
        
        responseOne = arcade.gui.UIFlatButton(text=responses[0],width=600,height=160,style=responsesStyle)
        responsesBoxOne.add(responseOne.with_space_around(10,20,10,20))
        
        responseTwo = arcade.gui.UIFlatButton(text=responses[1],width=600,height=160,style=responsesStyle)
        responsesBoxOne.add(responseTwo.with_space_around(10,20,10,20))
        
        
        principalBox.add(responsesBoxOne.with_space_around(10,20,10,20))
        
        responsesBoxTwo = arcade.gui.UIBoxLayout(vertical=False)
        
        responseThree = arcade.gui.UIFlatButton(text=responses[2],width=600,height=160,style=responsesStyle)
        responsesBoxTwo.add(responseThree.with_space_around(10,20,10,20))
        
        responseFour = arcade.gui.UIFlatButton(text=responses[3],width=600,height=160,style=responsesStyle)
        responsesBoxTwo.add(responseFour.with_space_around(10,20,10,20))
        
        principalBox.add(responsesBoxTwo.with_space_around(10,20,10,20))
        
        guiMenu.add(arcade.gui.UIAnchorWidget(child=principalBox, anchor_x="center_x",anchor_y="center_y"))
        self.responsesList = [responseOne,responseTwo,responseThree,responseFour]
        
        self.responsesList[self.correct].on_click = self.pressCorrect
        
        self.responsesList.pop(self.correct)
        for i in self.responsesList:
            i.on_click = self.pressIncorrect
        
        return guiMenu
    
    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            
            self.window.show_view(self.pause)
    def on_draw(self):
        self.window.clear()
        self.menu.draw()
    
    def pressCorrect(self,event):
        self.window.show_view(self.gameView)
        self.menu = self.questionsMenu(self.questions)
        self.correctResponses += 1
        
        
    def pressIncorrect(self,event):
        self.player.lives -= 1
        self.window.show_view(self.gameView)
        self.menu = self.questionsMenu(self.questions)
        
        
    def on_show(self):
        
        self.menu.enable()
        
    def on_hide_view(self):
        self.menu.disable()
        
        