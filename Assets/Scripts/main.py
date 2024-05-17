import arcade
import arcade.color
import arcade.color
import arcade.gui
from Player import Player
import maps as Maps
import questions
import random

class Game(arcade.Window):
    
    
    def putDecoration(self, image, posx,posy,width,height):
        arcade.draw_texture_rectangle(posx,posy,texture=image,width=width,height=height)
    
    def centerCameraFromPlayer(self):
        
        cordY = self.player.center_y - (self.playerCamera.viewport_height / 2)
        cordX = self.player.center_x - (self.playerCamera.viewport_width / 2)
        
        if cordX < 0:
            cordX = 0
        if cordY < 0:
            cordY = 0
        
        cords = [cordX, cordY]
        self.playerCamera.move_to(cords,.1)
        
        
    
    def __init__(self):
        super().__init__(width=1280,height=720,title="LiteraryGame")
        self.speed = 5
        self.jump = 25
        
        self.isInMenu = True
        self.isPaused = False
        self.isInQuestion = False
        self.usedQuestions = []
        self.correct = 0
        
    
    def principalMenu(self,isPaused):
        principalManager = arcade.gui.UIManager()
        
        vBox = arcade.gui.UIBoxLayout()
        text = arcade.gui.UILabel(text="Habia una vez...",font_name="Retro Gaming",font_size=30)
        vBox.add(text.with_space_around(0,0,20,0))
        
        if isPaused:
            playText = "Continuar"
        else:
            playText = "Jugar"
        
        buttonStyle = {
            "font_name": "Retro Gaming",
        }
        
        play = arcade.gui.UIFlatButton(text=playText,style=buttonStyle,width=300,height=50)
        vBox.add(play.with_space_around(10,0,10,0))
        exit = arcade.gui.UIFlatButton(text="Salir",style=buttonStyle,width=300,height=50)
        vBox.add(exit.with_space_around(10,0,10,0))
        
        self.menuButtons = [play,exit]
        principalManager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=vBox
            )
        )
        
        return principalManager
        
        
        
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
        questionBox = arcade.gui.UIFlatButton(text=question,width=1230,height=300,style=questionStyle)
        
        bgBox = arcade.gui.UIBorder(child=questionBox)
        
        
        principalBox.add(bgBox)
        
        responsesBoxOne = arcade.gui.UIBoxLayout(vertical=False)
        
        self.responseOne = arcade.gui.UIFlatButton(text=responses[0],width=600,height=160,style=responsesStyle)
        responsesBoxOne.add(self.responseOne.with_space_around(10,20,10,20))
        
        self.responseTwo = arcade.gui.UIFlatButton(text=responses[1],width=600,height=160,style=responsesStyle)
        responsesBoxOne.add(self.responseTwo.with_space_around(10,20,10,20))
        
        
        principalBox.add(responsesBoxOne.with_space_around(10,20,10,20))
        
        responsesBoxTwo = arcade.gui.UIBoxLayout(vertical=False)
        
        self.responseThree = arcade.gui.UIFlatButton(text=responses[2],width=600,height=160,style=responsesStyle)
        responsesBoxTwo.add(self.responseThree.with_space_around(10,20,10,20))
        
        self.responseFour = arcade.gui.UIFlatButton(text=responses[3],width=600,height=160,style=responsesStyle)
        responsesBoxTwo.add(self.responseFour.with_space_around(10,20,10,20))
        
        principalBox.add(responsesBoxTwo.with_space_around(10,20,10,20))
        
        guiMenu.add(arcade.gui.UIAnchorWidget(child=principalBox, anchor_x="center_x",anchor_y="center_y"))
        self.responsesList = [self.responseOne,self.responseTwo,self.responseThree,self.responseFour]
        return guiMenu
        
    def setup(self):
        
        self.menu = self.principalMenu(False)
        self.menu.enable()
        
        self.scene = arcade.Scene.from_tilemap(Maps.initalMap)
        self.playerCamera = arcade.Camera(1280,720)
        self.guiCamera = arcade.Camera(1280,720)

        
        self.player = Player(100,350,4)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        arcade.set_background_color(arcade.csscolor.DIM_GREY)
        self.PhysicsEngine = arcade.PhysicsEnginePlatformer(player_sprite=self.player, walls=self.scene["Floor"],gravity_constant=1)

    def on_draw(self):
        arcade.start_render()
        self.clear()
        if self.isInMenu and not self.isPaused and False:
            self.menu.draw()
        
        else:   
            if self.isInQuestion:
                self.question.draw()
            else:
                
                self.playerCamera.use()
                self.scene.draw()
                self.guiCamera.use()
               
                if arcade.check_for_collision_with_list(self.player, self.scene["Key"]):
                    arcade.draw_text("Presiona E",600,100,arcade.color.WHITE,24,font_name="Retro Gaming")


    def update_player_velocity(self):
        if self.player.moveLeft and not self.player.moveRight:
            self.player.change_x = -self.speed
        if self.player.moveRight and not self.player.moveLeft:
            self.player.change_x = self.speed
        if not self.player.moveLeft and not self.player.moveRight:
            self.player.change_x = 0
        if self.player.moveLeft and self.player.moveRight:
            self.player.change_x = 0
    
    def on_key_press(self, key: int, modifiers: int):
        if not self.isInMenu and not self.isInQuestion:    
            if key == arcade.key.A:
                self.player.moveLeft = True
            if key == arcade.key.D:
                self.player.moveRight = True
            if key == arcade.key.SPACE and self.PhysicsEngine.can_jump():
                self.player.change_y = self.jump

            if arcade.check_for_collision_with_list(self.player,self.scene["Key"]) and key == arcade.key.E:
                self.question = self.questionsMenu(questions.levelOne)
                self.question.enable()
                self.isInQuestion = True
    
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A:
            self.player.moveLeft = False
        if key == arcade.key.D:
            self.player.moveRight = False
    
    def quesitonMenuController(self):
        if self.responsesList[self.correct].pressed:
            self.isInQuestion = False
    
            
    def on_update(self, delta_time: float):
        
        if self.isInMenu and False:
            
            self.menuController()
            
                
        else:   
            self.update_player_velocity()
            self.centerCameraFromPlayer()
            self.PhysicsEngine.update()
            self.scene.get_sprite_list("Player").update_animation()
            if self.player.center_y < 0:
                self.setup()
            if self.player.left < 0:
                self.player.change_x = 0
            
            if self.isInQuestion:
                self.quesitonMenuController()
        
        
        
        
if __name__ == '__main__':
    window = Game()
    window.setup()
    arcade.run()
    