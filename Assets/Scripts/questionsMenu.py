import arcade
import arcade.color
import arcade.gui
import random
from PauseMenu import PauseMenu
import globalVars
from copy import copy

class QuestionMenu(arcade.View):
    global globalVars

    def __init__(self, window, questions, gameView, menuView, opportunities, quantityQuestions):
        super().__init__(window)
        self.questions = questions
        self.gameView = gameView
        self.menuView = menuView
        self.pause = PauseMenu(self.window, self, self.menuView)
        self.quantityQuestions = quantityQuestions
        self.opportunities = opportunities
        self.currentOportunities = opportunities
        self.questionIndex = 0
        self.usedQuestions = []
        self.canPass = False
        self.init = 1
        self.alpha = 255
        self.time = 1
        self.questionStyle = {
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": arcade.color.BLACK,
            "border_color_pressed": arcade.color.BLACK,
            "font_color_pressed": arcade.color.WHITE,
            "font_name": "Retro Gaming",
            "font_size": 15
        }

        self.opportunitiesStyleDefault = {
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed": None,
            "font_name": "Retro Gaming"
        }

        self.opportunitiesStyleEmpty = {
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed": None,
            "font_name": "Retro Gaming"
        }

    
        self.colors = [arcade.color.BLUE_BELL,arcade.color.BLUE_SAPPHIRE,arcade.color.BLUE_YONDER,arcade.color.BLUEBERRY,arcade.color.BLEU_DE_FRANCE]
        
        self.boxTexture = arcade.load_texture("Assets/Sprites/QuestionMenu/commonQuestion.png")
        self.actualQuestion = self.getQuestion(self.questions)
        self.menu = self.questionsMenu(self.actualQuestion[0],self.actualQuestion[1])

    def getQuestion(self, questions):
        randomNumber = random.randint(0, len(questions) - 1)
        while randomNumber in self.usedQuestions:
            randomNumber = random.randint(0, len(questions) - 1)

        question = questions[str(randomNumber)]["question"]
        responses = questions[str(randomNumber)]["responses"]
        correct = responses[0]
        random.shuffle(responses)
        self.correct = responses.index(correct)
        self.usedQuestions.append(randomNumber)
        return question, responses
    def on_show_view(self):
        self.init = 0
    
    def questionsMenu(self, question, responses):
        self.fillX = arcade.load_texture("Assets/Sprites/UI/fillX.png")
        self.emptyX = arcade.load_texture("Assets/Sprites/UI/emptyX.png")

        missingBox = arcade.gui.UIBoxLayout(vertical=False)
        missingLabel = arcade.gui.UILabel(text=f"Preguntas: {self.questionIndex + 1}/{self.quantityQuestions}", font_name="Retro Gaming", font_size=18)
        missingBox.add(missingLabel)

        guiMenu = arcade.gui.UIManager()
        principalBox = arcade.gui.UIBoxLayout()
        principalBox.add(missingBox.with_space_around(0, 0, 20, 0))

        
        secondBox = arcade.gui.UIBoxLayout(vertical=False)
        questionBox = arcade.gui.UIFlatButton(text=question, width=1000, height=200, style=self.questionStyle)
        secondBox.add(questionBox.with_space_around(2, 2, 2, 2))

        opportunitiesBox = arcade.gui.UIBoxLayout()
        opportunitiesLabel = arcade.gui.UILabel(text="Oportunidades", font_name="Retro Gaming", font_size=12)
        opportunitiesBox.add(opportunitiesLabel)

        for i in range(self.opportunities):
            if i <= self.currentOportunities - 1:
                x = arcade.gui.UITextureButton(width=32, height=32, style=self.opportunitiesStyleDefault, texture=self.fillX)
            else:
                x = arcade.gui.UITextureButton(width=32, height=32, style=self.opportunitiesStyleEmpty, texture=self.emptyX)
            opportunitiesBox.add(x.with_space_around(5, 5, 0, 5))

        secondBox.add(opportunitiesBox.with_space_around(2, 2, 2, 2))
        principalBox.add(secondBox)
        responsesStyle = {
            "font_name": "Retro Gaming",
            "border_color": None,
            "border_color_focused": None,
            "bg_color_focused": self.colors[0],
            "border_radius": 100
        }
        responsesBoxOne = arcade.gui.UIBoxLayout(vertical=False)
        responseOne = arcade.gui.UIFlatButton(text=responses[0], width=600, height=160, style=responsesStyle)
        responsesBoxOne.add(responseOne.with_space_around(10, 20, 10, 20))
        responsesStyle = {
            "font_name": "Retro Gaming",
            "border_color": None,
            "border_color_focused": None,
            "bg_color_focused": self.colors[1],
            "border_radius": 100
        }
        responseTwo = arcade.gui.UIFlatButton(text=responses[1], width=600, height=160, style=responsesStyle)
        responsesBoxOne.add(responseTwo.with_space_around(10, 20, 10, 20))

        principalBox.add(responsesBoxOne.with_space_around(10, 20, 10, 20))

        responsesBoxTwo = arcade.gui.UIBoxLayout(vertical=False)
        responsesStyle = {
            "font_name": "Retro Gaming",
            "border_color": None,
            "border_color_focused": None,
            "bg_color_focused": self.colors[2],
            "border_radius": 100
        }
        responseThree = arcade.gui.UIFlatButton(text=responses[2], width=600, height=160, style=responsesStyle)
        responsesBoxTwo.add(responseThree.with_space_around(10, 20, 10, 20))
        responsesStyle = {
            "font_name": "Retro Gaming",
            "border_color": None,
            "border_color_focused": None,
            "bg_color_focused": self.colors[3],
            "border_radius": 100
        }
        responseFour = arcade.gui.UIFlatButton(text=responses[3], width=600, height=160, style=responsesStyle)
        responsesBoxTwo.add(responseFour.with_space_around(10, 20, 10, 20))

        principalBox.add(responsesBoxTwo.with_space_around(10, 20, 10, 20))
        guiMenu.add(arcade.gui.UIAnchorWidget(child=principalBox, anchor_x="center_x", anchor_y="center_y"))

        self.responsesList = [responseOne, responseTwo, responseThree, responseFour]
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
        arcade.set_background_color(arcade.color.ASH_GREY)
        arcade.draw_rectangle_filled(self.window.width/2,self.window.height/2,self.window.width,self.window.height,(0,0,0,self.alpha))

    def pressCorrect(self, event):
        self.actualQuestion = self.getQuestion(self.questions)
        self.questionIndex += 1
        if self.questionIndex < self.quantityQuestions:
            self.menu = self.questionsMenu(self.actualQuestion[0],self.actualQuestion[1])
            self.menu.enable()
        else:
            self.canPass = True
            self.init = 2

    def pressIncorrect(self, event):
        self.currentOportunities -= 1
        if self.currentOportunities == -1:
            self.init = 2
            if globalVars.APPEND_LIFES > 0:
                globalVars.APPEND_LIFES -= 1
            globalVars.LIFES -= 1
            self.currentOportunities = copy(self.opportunities)
            self.questionIndex = 0
        self.menu = self.questionsMenu(*self.actualQuestion)
        self.menu.enable()

    def on_show(self):
        self.menu.enable()

    def on_hide_view(self):
        self.menu.disable()

    def on_update(self, delta_time: float):
        if self.init == 0:
            self.time -= delta_time
            if self.time <= 0:
                self.time = 0
                self.init = 1
            self.alpha = 255 * abs(self.time / 1)
            
        if self.init == 2:
            self.time += delta_time
            if self.time >= 1:
                self.time = 1
                self.init = 1
                self.window.show_view(self.gameView)
            self.alpha = 255 * abs(self.time/1)
        