import arcade
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
        
    def setup(self):
        
        self.scene = arcade.Scene.from_tilemap(Maps.initalMap)
        self.playerCamera = arcade.Camera(1280,720)
        
        
    
        self.player = Player(120,350,4)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.PhysycsEngine = arcade.PhysicsEnginePlatformer(player_sprite=self.player, walls=self.scene["Terrain"],gravity_constant=1)

    def on_draw(self):
        arcade.start_render()
        self.clear()
       
        self.scene.draw()
        self.playerCamera.use()
        self.putDecoration(self.lamp,400,245, 100,200)
        self.scene.get_sprite_list("Player").draw()
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
        
if __name__ == '__main__':
    window = Game()
    window.setup()
    arcade.run()
    