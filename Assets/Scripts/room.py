import arcade
from Player import Player
import random
import maps as Maps
from PauseMenu import PauseMenu
from questionsMenu import QuestionMenu
import questions as q
import globalVars
from gameOver import GameOverView
import sounds

class Key(arcade.Sprite):
    def __init__(self, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: str | None = "Simple", hit_box_detail: float = 4.5, texture: arcade.Texture = None, angle: float = 0,questionMenu: QuestionMenu = None):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)
        
        self.canPass = False
        self.questionMenu = questionMenu


class Room(arcade.View):
    global globalVars
    
    def __init__(self,window,tilemap,x,y,scale,menu,questions,game,keys,previousRoom = None, nextRoom = None):
        super().__init__(window)
        
        self.keys = keys
        self.canPass = False
        self.previousRoom = previousRoom
        self.nextRoom = nextRoom
        
        self.speed = 5
        self.jump = 25
        self.game = game
        self.player = Player(x,y,scale)
        self.gameOverView = GameOverView(self.window,menu)
        self.scene = arcade.Scene.from_tilemap(Maps.initalMap)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        self.scene.add_sprite_list("Key")
        
        for key in keys:
            newKey = Key(filename=key["filename"],center_x=key["center_x"], center_y=key["center_y"],questionMenu=key["questionMenu"],scale=key["scale"])
            newKey.questionMenu.gameView = self
            
            self.scene.add_sprite("Key",newKey)
        
        self.menu = menu
        self.x = x
        self.y = y
        self.playerCamera = arcade.Camera(1280,720)
        self.guiCamera = arcade.Camera(1280,720)
       
        self.pause = PauseMenu(self.window,self,menu)
        arcade.set_background_color(arcade.csscolor.DIM_GREY)
        self.physicsEngine = arcade.PhysicsEnginePlatformer(player_sprite=self.player, walls=self.scene["Floor"],gravity_constant=0)
        
        
        self.player.center_x = self.x
        self.player.center_y = self.y
        self.lastX = self.player.center_x
        self.lastY = self.player.center_y
        
        self.fillHeart = arcade.load_texture("Assets/Sprites/UI/fillHeart.png")
        self.emptyHeart = arcade.load_texture("Assets/Sprites/UI/emptyHeart.png")
        
        self.walkChannel = sounds.walk.play()
        sounds.walk.stop()
        
    def roomSetup(self):
        self.scene = arcade.Scene.from_tilemap(Maps.initalMap)
        
        self.player.center_x = self.x
        self.player.center_y = self.y
        self.lastX = self.player.center_x
        self.lastY = self.player.center_y
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        
        for key in self.keys:
            newKey = Key(filename=key["filename"],center_x=key["center_x"], center_y=key["center_y"],questionMenu=key["questionMenu"],scale=key["scale"])
            newKey.questionMenu.gameView = self
            self.scene.add_sprite("Key",newKey)
        
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
        arcade.set_background_color(arcade.color.BLACK)
        self.playerCamera.use()
        self.scene.draw()
        self.guiCamera.use()
        
        x = 10
        
        for i in range(globalVars.TOTAL_LIFES):
            if i <= globalVars.LIFES - 1:
                arcade.draw_lrwh_rectangle_textured(x,650,64,64,self.fillHeart)
            else:
                arcade.draw_lrwh_rectangle_textured(x,650,64,64,self.emptyHeart)
            x += 64
                
        
        if arcade.check_for_collision_with_list(self.player, self.scene["Key"]) and not self.canPass:
            arcade.draw_text("Presiona E",600,100,arcade.color.WHITE,24,font_name="Retro Gaming")


    def update_player_velocity(self):
        if self.player.moveUp and not self.player.moveDown:
            self.player.change_y = self.speed
        if self.player.moveDown and not self.player.moveUp:
            self.player.change_y = -self.speed
        if (not self.player.moveUp and not self.player.moveDown) or (self.player.moveUp and self.player.moveDown):
            self.player.change_y = 0
    
        if self.player.moveLeft and not self.player.moveRight:
            self.player.change_x = -self.speed
        if self.player.moveRight and not self.player.moveLeft:
            self.player.change_x = self.speed
        if (not self.player.moveLeft and not self.player.moveRight) or (self.player.moveLeft and self.player.moveRight):
            self.player.change_x = 0
        
        
    def on_key_press(self, key: int, modifiers: int):
        
        if key == arcade.key.A:
            self.player.moveLeft = True
        if key == arcade.key.D:
            self.player.moveRight = True
        if key == arcade.key.W:
            self.player.moveUp = True
        if key == arcade.key.S:
            self.player.moveDown = True
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.pause)
        
        if arcade.check_for_collision_with_list(self.player,self.scene["Key"]) and key == arcade.key.E:
            for key in arcade.check_for_collision_with_list(self.player,self.scene["Key"]):
                self.window.show_view(key.questionMenu)
        print(self.player.change_x)
        print(self.player.change_y)
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A:
            self.player.moveLeft = False
        if key == arcade.key.D:
            self.player.moveRight = False
        if key == arcade.key.W:
            self.player.moveUp = False
        if key == arcade.key.S:
            self.player.moveDown = False
    def checkKeys(self):
        allPasses = []
        for i in self.scene.get_sprite_list("Key"):
            allPasses.append(i.questionMenu.canPass)
        canPass = all(allPasses)
        print(allPasses)
        print(canPass)
        return canPass
    
    def on_update(self, delta_time: float):
        self.canPass = self.checkKeys()
        
        if arcade.check_for_collision_with_list(self.player,self.scene["ExitDoor"]) and self.nextRoom is not None and self.canPass:
            self.window.show_view(self.nextRoom)
        if arcade.check_for_collision_with_list(self.player,self.scene["EntryDoor"]) and self.previousRoom is not None and self.canPass:
            self.window.show_view(self.previousRoom)
        
        if self.player.change_x != 0:
            if self.walkChannel.get_busy():
                pass
            else:
                sounds.walk.play()
                
        else:
            sounds.walk.stop()
        
        if globalVars.LIFES == 0:
            globalVars.LIFES = 5
            self.window.show_view(self.gameOverView)
        self.update_player_velocity()
        self.centerCameraFromPlayer()
        self.physicsEngine.update()
        self.scene.get_sprite_list("Player").update_animation()
        if self.player.center_y < 0:
            self.setup()
        if self.player.left < 0:
            self.player.change_x = 0
    
        