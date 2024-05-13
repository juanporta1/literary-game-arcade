import arcade
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
        
        
    def questionsMenu(self):
        
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
        
        self.responsesOne = arcade.gui.UIFlatButton(text="Respuesta Uno",width=600,height=160)
        responsesBoxOne.add(self.responsesOne.with_space_around(10,20,10,20))
        
        self.responsesTwo = arcade.gui.UIFlatButton(text="Respuesta Dos",width=600,height=160)
        responsesBoxOne.add(self.responsesTwo.with_space_around(10,20,10,20))
        
        
        principalBox.add(responsesBoxOne.with_space_around(10,20,10,20))
        
        responsesBoxTwo = arcade.gui.UIBoxLayout(vertical=False)
        
        self.responsesTrhee = arcade.gui.UIFlatButton(text="Respuesta Tres",width=600,height=160)
        responsesBoxTwo.add(self.responsesTrhee.with_space_around(10,20,10,20))
        
        self.responsesFour = arcade.gui.UIFlatButton(text="Respuesta Cuatro",width=600,height=160)
        responsesBoxTwo.add(self.responsesFour.with_space_around(10,20,10,20))
        
        principalBox.add(responsesBoxTwo.with_space_around(10,20,10,20))
        
        guiMenu.add(arcade.gui.UIAnchorWidget(child=principalBox, anchor_x="center_x",anchor_y="center_y"))
        return guiMenu
    def setup(self):
        self.question = self.questionsMenu()
        self.question.enable()
        self.scene = arcade.Scene.from_tilemap(Maps.initalMap)
        self.playerCamera = arcade.Camera(1280,720)
        
        self.bg1 = arcade.load_texture("Assets/BGs/map1_bg.png")

        
        self.player = Player(120,350,4)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        arcade.set_background_color(arcade.csscolor.DIM_GREY)
        self.PhysycsEngine = arcade.PhysicsEnginePlatformer(player_sprite=self.player, walls=self.scene["Terrain"],gravity_constant=1)

    def on_draw(self):
        arcade.start_render()
        self.clear()
        
            
        if True:
            
            
            self.question.draw()
        else:
            arcade.draw_lrwh_rectangle_textured(0,0,7200,7200,self.bg1)
            self.scene.draw()
            self.playerCamera.use()

       
        
        
    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.A:
            self.player.change_x = -self.speed
        if key == arcade.key.D:
            self.player.change_x = self.speed
        if key == arcade.key.SPACE and self.PhysycsEngine.can_jump():
            self.player.change_y = self.jump
        
    
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0
        if key == arcade.key.SPACE:
            self.player.change_y = 0
        
    def on_update(self, delta_time: float):
        self.centerCameraFromPlayer()
        self.PhysycsEngine.update()
        self.scene.get_sprite_list("Player").update_animation()
        if self.player.center_y < 0:
            self.setup()
        if self.player.left < 0:
            self.player.change_x = 0
        
        if arcade.check_for_collision_with_list(self.player, self.scene["Llave"]):
            print("Hola")
        
        if self.responsesOne.pressed == True:
            print("Genial")
        
        
if __name__ == '__main__':
    window = Game()
    window.setup()
    arcade.run()
    