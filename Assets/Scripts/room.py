import arcade
from player import Player
import random
import maps as Maps
from pauseMenu import PauseMenu
from questionsMenu import QuestionMenu
import questions as q
class Room(arcade.View):
    
    def __init__(self,window,tilemap,x,y,scale,menu,questions,player:Player,game):
        super().__init__(window)
        
        self.speed = 5
        self.jump = 25
        self.game = game
        self.scene = arcade.Scene.from_tilemap(Maps.initalMap)
        self.player = player
        self.playerCamera = arcade.Camera(1280,720)
        self.guiCamera = arcade.Camera(1280,720)
        self.pause = PauseMenu(self.window,self,menu)
        self.questionMenu = QuestionMenu(self.window,questions,self,menu,self.player)
        
        self.player.center_x = x
        self.player.center_y = y
        self.lastX = self.player.center_x
        self.lastY = self.player.center_y
        self.player.scale = scale
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        arcade.set_background_color(arcade.csscolor.DIM_GREY)
        self.physicsEngine = arcade.PhysicsEnginePlatformer(player_sprite=self.player, walls=self.scene["Floor"],gravity_constant=1)
        
        
    def centerCameraFromPlayer(self):
        
        cordY = self.player.center_y - (self.playerCamera.viewport_height / 2)
        cordX = self.player.center_x - (self.playerCamera.viewport_width / 2)
        
        if cordX < 0:
            cordX = 0
        if cordY < 0:
            cordY = 0
        
        cords = [cordX, cordY]
        self.playerCamera.move_to(cords,.1)
        
    def on_hide_view(self):
        self.lastX = self.player.center_x
        self.lastY = self.player.center_y
    
    def on_show(self):
        self.player.center_x = self.lastX
        self.player.center_y = self.lastY
    
    def on_draw(self):
        arcade.start_render()
        self.clear()
        
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
           
        if key == arcade.key.A:
            self.player.moveLeft = True
        if key == arcade.key.D:
            self.player.moveRight = True
        if key == arcade.key.SPACE and self.physicsEngine.can_jump():
            self.player.change_y = self.jump

        if key == arcade.key.ESCAPE:
            self.window.show_view(self.pause)
        
        if arcade.check_for_collision_with_list(self.player,self.scene["Key"]) and key == arcade.key.E:
            self.window.show_view(self.questionMenu)
    
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A:
            self.player.moveLeft = False
        if key == arcade.key.D:
            self.player.moveRight = False
            
    def on_update(self, delta_time: float):
        
    
        self.update_player_velocity()
        self.centerCameraFromPlayer()
        self.physicsEngine.update()
        self.scene.get_sprite_list("Player").update_animation()
        if self.player.center_y < 0:
            self.setup()
        if self.player.left < 0:
            self.player.change_x = 0
    
        