import arcade
import arcade.color
import arcade.color
import arcade.gui
from Player.Player import Player
import Maps.maps as Maps

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
        self.lamp = arcade.load_texture("Assets/Sprites/Terrain/OakWood/oak_woods_v1.0/decorations/lamp.png")
        self.isInMenu = False
        self.isInQuestion = False
        
    def questionsMenu(self,true):
        
        self.true = true
        
        
        guiMenu = arcade.gui.UIManager()

        principalBox = arcade.gui.UIBoxLayout()
        
        questionStyle = {
            "font_name": "Minecraftia",
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed" : None,
            "font_color_pressed": arcade.color.WHITE
        }
        questionBox = arcade.gui.UIFlatButton(text="Pregunta PreguntaPr    egunt  aPr egu nta PrPreguntaPregunta e  untaPr egunta PreguntaP  reguntaPreguntaPreg untaPPreguntaPregunta re guPreguntaPreguntanta ",width=1230,height=300,style=questionStyle)
        
        bgBox = arcade.gui.UIBorder(child=questionBox)
        
        
        principalBox.add(bgBox)
        
        responsesBoxOne = arcade.gui.UIBoxLayout(vertical=False)
        
        self.responseOne = arcade.gui.UIFlatButton(text="Respuesta Uno",width=600,height=160)
        responsesBoxOne.add(self.responseOne.with_space_around(10,20,10,20))
        
        self.responseTwo = arcade.gui.UIFlatButton(text="Respuesta Dos",width=600,height=160)
        responsesBoxOne.add(self.responseTwo.with_space_around(10,20,10,20))
        
        
        principalBox.add(responsesBoxOne.with_space_around(10,20,10,20))
        
        responsesBoxTwo = arcade.gui.UIBoxLayout(vertical=False)
        
        self.responseThree = arcade.gui.UIFlatButton(text="Respuesta Tres",width=600,height=160)
        responsesBoxTwo.add(self.responseThree.with_space_around(10,20,10,20))
        
        self.responseFour = arcade.gui.UIFlatButton(text="Respuesta Cuatro",width=600,height=160)
        responsesBoxTwo.add(self.responseFour.with_space_around(10,20,10,20))
        
        principalBox.add(responsesBoxTwo.with_space_around(10,20,10,20))
        
        guiMenu.add(arcade.gui.UIAnchorWidget(child=principalBox, anchor_x="center_x",anchor_y="center_y"))
        self.responsesList = [self.responseOne,self.responseTwo,self.responseThree,self.responseFour]
        return guiMenu
        
    def setup(self):
        
        
        self.scene = arcade.Scene.from_tilemap(Maps.initalMap)
        self.playerCamera = arcade.Camera(1280,720)
        self.guiCamera = arcade.Camera(1280,720)
        
        self.bg1 = arcade.load_texture("Assets/BGs/map1_bg.png")

        
        self.player = Player(3800,350,4)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        arcade.set_background_color(arcade.csscolor.DIM_GREY)
        self.PhysycsEngine = arcade.PhysicsEnginePlatformer(player_sprite=self.player, walls=self.scene["Terrain"],gravity_constant=1)

    def on_draw(self):
        arcade.start_render()
        self.clear()
        
            
        if self.isInQuestion:
            self.question.draw()
        else:
            
            self.playerCamera.use()
            arcade.draw_lrwh_rectangle_textured(0,0,7200,7200,self.bg1)
            self.scene.draw()
            self.guiCamera.use()
            if arcade.check_for_collision_with_list(self.player, self.scene["Llave"]):
                arcade.draw_text("Presiona E",600,100,arcade.color.WHITE,24,font_name="Pixel-Art")

        
    def on_key_press(self, key: int, modifiers: int):
        if not self.isInMenu and not self.isInQuestion:    
            if key == arcade.key.A:
                self.player.change_x = -self.speed
            if key == arcade.key.D:
                self.player.change_x = self.speed
            if key == arcade.key.SPACE and self.PhysycsEngine.can_jump():
                self.player.change_y = self.jump

            if arcade.check_for_collision_with_list(self.player,self.scene["Llave"]) and key == arcade.key.E:
                self.question = self.questionsMenu(1)
                self.question.enable()
                self.isInQuestion = True
    
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0
        if key == arcade.key.SPACE:
            self.player.change_y = 0
    
    def quesitonMenuController(self):
        if self.responsesList[self.true].pressed:
            self.isInQuestion = False
       
    def on_update(self, delta_time: float):
        self.centerCameraFromPlayer()
        self.PhysycsEngine.update()
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
    