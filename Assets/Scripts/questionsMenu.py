import arcade
import arcade.color
import arcade.gui
import random
from PauseMenu import PauseMenu
from Player import Player
import globalVars
from copy import copy

class QuestionMenu(arcade.View):
    global globalVars
    def __init__(self, window, questions,gameView,menuView,oportunities,quantityQuestions):
        super().__init__(window)
        self.usedQuestions = []
        self.questions = questions
        self.gameView = gameView
        self.menuView = menuView
        self.pause = PauseMenu(self.window,self,self.menuView)
        self.quantityQuestions = quantityQuestions
        self.questionIndex = 0
        self.oportunities = oportunities
        self.currentOportunities = oportunities 
        self.questionStyle = {
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": arcade.color.BLACK,
            "border_color_pressed" : arcade.color.BLACK,
            "font_color_pressed": arcade.color.WHITE
        }
        self.missingQuestionStyleFocus = {
            "bg_color": arcade.color.WHITE_SMOKE,
            "bg_color_pressed": arcade.color.WHITE_SMOKE,
            "border_color": arcade.color.WHITE_SMOKE,
            "border_color_pressed" : arcade.color.WHITE_SMOKE
        }
        
        self.missingQuestionStyleCorrect = {
            "bg_color": arcade.color.DARK_GREEN,
            "bg_color_pressed": arcade.color.DARK_GREEN,
            "border_color": arcade.color.DARK_GREEN,
            "border_color_pressed" : arcade.color.DARK_GREEN
        } 
        self.missingQuestionStyleDefault = {
            "bg_color": arcade.color.ASH_GREY,
            "bg_color_pressed": arcade.color.ASH_GREY,
            "border_color": arcade.color.ASH_GREY,
            "border_color_pressed" : arcade.color.ASH_GREY
        }
        self.opportunitiesStyleDefault = {
            "bg_color": arcade.color.GREEN,
            "bg_color_pressed": arcade.color.GREEN,
            "border_color": arcade.color.GREEN,
            "border_color_pressed" : arcade.color.GREEN
        }
        self.opportunitiesStyleEmpty = {
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed" : None
        }
        self.actualQuestion = self.getQuestion(self.questions)
        self.menu = self.questionsMenu(*self.actualQuestion)
        self.canPass = False
        
    def getQuestion(self,questions):
        randomNumber = random.randint(0,len(questions)-1)
        while self.usedQuestions.count(randomNumber) != 0:
            randomNumber = random.randint(0,len(questions))
         
                
        question = questions[randomNumber]["question"]
        responses = questions[randomNumber]["responses"]
        correct = responses[0]
        random.shuffle(responses)
        self.correct = responses.index(correct)
        self.usedQuestions.append(randomNumber)
        return question,responses
    
    
    
    def questionsMenu(self,question,responses):
        
        
        
        missingBox = arcade.gui.UIBoxLayout(vertical=False)
        missingLabel = arcade.gui.UILabel(text="Preguntas: ",font_name="Retro Gaming", font_size=18)
        missingBox.add(missingLabel)
        
        for i in range(self.quantityQuestions):
            if i == self.questionIndex:
                x = arcade.gui.UIFlatButton(width=32,height=32,style=self.missingQuestionStyleFocus)
            elif i < self.questionIndex:
                x = arcade.gui.UIFlatButton(width=32,height=32,style=self.missingQuestionStyleCorrect)
            else:
                x = arcade.gui.UIFlatButton(width=32,height=32,style=self.missingQuestionStyleDefault)
            missingBox.add(x.with_space_around(0,5,0,5))
            
         
        
        guiMenu = arcade.gui.UIManager()

        
        
        principalBox = arcade.gui.UIBoxLayout()
        
        principalBox.add(missingBox.with_space_around(0,0,20,0))
        
        responsesStyle = {
            "font_name": "Retro Gaming",
            "border_color": None,
            "border_color_focused": None,
            "bg_color_focused": arcade.color.BLACK
        }
        secondBox = arcade.gui.UIBoxLayout(vertical=False)
        questionBox = arcade.gui.UIFlatButton(text=question,width=1100,height=200,style=self.questionStyle)
        secondBox.add(questionBox.with_space_around(2,2,2,2))
        opportunitiesBox = arcade.gui.UIBoxLayout()
        opportunitiesLabel = arcade.gui.UILabel(text="Oportunidades", font_name="Retro Gaming", font_size=12)
        opportunitiesBox.add(opportunitiesLabel)

        for i in range(self.oportunities):
            if i <= self.currentOportunities - 1:
                x = arcade.gui.UIFlatButton(width=32,height=10,style=self.opportunitiesStyleDefault)
            else:
                x = arcade.gui.UIFlatButton(width=32,height=10,style=self.opportunitiesStyleEmpty)
                
            opportunitiesBox.add(x.with_space_around(5,5,0,5))
        
        secondBox.add(opportunitiesBox.with_space_around(2,2,2,2))
        
        
        principalBox.add(secondBox)
        
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
        self.actualQuestion = self.getQuestion(self.questions)
        self.questionIndex += 1
        if self.questionIndex < self.quantityQuestions:
            self.menu = self.questionsMenu(*self.actualQuestion)
            self.menu.enable()
        else:
            self.canPass = True
            self.window.show_view(self.gameView)
            
        
        
    def pressIncorrect(self,event):
        self.currentOportunities -= 1
        if self.currentOportunities == -1:
            self.window.show_view(self.gameView)
            globalVars.LIFES -= 1   
            self.currentOportunities = copy(self.oportunities)
            self.questionIndex = 0
        self.menu = self.questionsMenu(*self.actualQuestion)
        self.menu.enable()
        
        
    def on_show(self):
        
        self.menu.enable()
        
    def on_hide_view(self):
        self.menu.disable()
        
        