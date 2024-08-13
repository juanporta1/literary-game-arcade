import arcade
import arcade.gui
from Player import Player
import random
import maps as Maps
from PauseMenu import PauseMenu
from questionsMenu import QuestionMenu
import globalVars
from gameOver import GameOverView
import sounds
import pygame
import json

class Key(arcade.Sprite):
    def __init__(self, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: str | None = "Simple", hit_box_detail: float = 4.5, texture: arcade.Texture = None, angle: float = 0,questionMenu: QuestionMenu = None):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)
        
        self.canPass = False
        self.questionMenu = questionMenu


class Room(arcade.View):
    global globalVars
    
    def __init__(self,window,menu,game,jsonFile, nextRoom = None):
        super().__init__(window)
        
        with open(jsonFile,"r") as file:
            data = file.read()
          
        jsonData = json.loads(data)
        keys = jsonData["keys"]
        lifes = jsonData["lifes"]
        self.canPass = False
        self.nextRoom = nextRoom
        self.speed = 4
        self.jump = 25
        self.game = game
        self.player = Player(jsonData["setup"]["playerX"],jsonData["setup"]["playerY"],jsonData["setup"]["playerScale"])
        self.gameOverView = GameOverView(self.window,menu)
        self.map = arcade.load_tilemap(jsonData["setup"]["tilemap"])
        self.scene = arcade.Scene.from_tilemap(self.map)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        self.scene.add_sprite_list("Key")
        self.scene.add_sprite_list("Life")
        
    
        
        for key in keys:
            with open(key["qm"]["questions"],"r") as f:
                data = f.read()
            questions = json.loads(data)
            qm = QuestionMenu(self.window,questions,self.game,menu,key["qm"]["op"],key["qm"]["qq"])
            
            newKey = Key(filename=key["filename"],center_x=key["center_x"], center_y=key["center_y"],questionMenu=qm,scale=key["scale"])
            newKey.questionMenu.gameView = self
            
            self.scene.add_sprite("Key",newKey)
            
        for life in lifes:
            sprite = arcade.Sprite("Assets/Sprites/UI/fillHeart.png",2,center_x=life["x"],center_y=life["y"])
            self.scene.add_sprite("Life",sprite)
        self.menu = menu
        self.x = jsonData["setup"]["playerX"]
        self.y = jsonData["setup"]["playerY"]
        self.playerCamera = arcade.Camera(1280,720)
        self.guiCamera = arcade.Camera(1280,720)
       
        self.pause = PauseMenu(self.window,self,menu)
        arcade.set_background_color(arcade.csscolor.DIM_GREY)
        self.physicsEngine = arcade.PhysicsEnginePlatformer(player_sprite=self.player, walls=self.scene["Wall"],gravity_constant=0)
        
        self.falseFloors = []

        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"FalseFloor{i}"]:
                    self.falseFloors.append(f"FalseFloor{i}")
                    self.scene[f"FalseFloor{i}"].visible = False
            except:
                break
            
        self.bridges = []
        
        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"Bridge {i}"]:
                    self.bridges.append(f"Bridge{i}")
                    self.scene[f"Bridge{i}"].visible = False
            except:
                break
            
        print(self.bridges)
            
        self.bridgeKeys = []
        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"BridgeKey{i}"]:
                    self.bridgeKeys.append(f"BridgeKey{i}")
                    self.scene[f"BridgeKey{i}"].visible = True
            except:
                break
            
            
        self.player.center_x = self.x
        self.player.center_y = self.y
        self.lastX = self.player.center_x
        self.lastY = self.player.center_y
        
        self.fillHeart = arcade.load_texture("Assets/Sprites/UI/fillHeart.png")
        self.emptyHeart = arcade.load_texture("Assets/Sprites/UI/emptyHeart.png")
        
        
        
        self.interface = arcade.gui.UIManager()
        self.ambient: pygame.mixer.Sound = sounds.ambient[random.randint(0,2)]
        self.channel = self.ambient.play()  
        self.channel.stop()           

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
        self.player.moveDown = False
        self.player.moveLeft = False
        self.player.moveRight = False
        self.player.moveUp = False
        self.channel.stop()
    
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
        self.interface.draw()
        x = 10
        
        for i in range(globalVars.TOTAL_LIFES + globalVars.APPEND_LIFES):
            if i <= globalVars.LIFES - 1:
                arcade.draw_lrwh_rectangle_textured(x,650,64,64,self.fillHeart)
            else:
                arcade.draw_lrwh_rectangle_textured(x,650,64,64,self.emptyHeart)
            x += 64
        
        if arcade.check_for_collision_with_list(self.player,self.scene["Key"]):
            arcade.draw_text("Presiona E",(1280/2 - 80),100,font_name="Retro Gaming",font_size=16)
                
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
        if self.player.center_x >= 0 and self.player.center_y >= 0:
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
        
        if key == arcade.key.E and arcade.check_for_collision_with_list(self.player,self.scene["Key"]):
            for key in arcade.check_for_collision_with_list(self.player,self.scene["Key"]):
                if not key.questionMenu.canPass:
                    self.window.show_view(key.questionMenu)
            
            
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
        return canPass
    
    def on_update(self, delta_time: float):
        self.canPass = self.checkKeys()
        if not self.channel.get_busy() and isinstance(self.window.current_view,self.__class__):
            self.ambient = sounds.ambient[random.randint(0,2)]
            self.channel = self.ambient.play()

        for life in arcade.check_for_collision_with_list(self.player,self.scene["Life"]):
            if globalVars.LIFES < globalVars.TOTAL_LIFES:
                globalVars.LIFES += 1
            else:
                globalVars.APPEND_LIFES += 1
                globalVars.LIFES += 1

            life.kill()
        
        for name in self.falseFloors:
            try:
                if arcade.check_for_collision_with_list(self.player,self.scene[name])[0]:
                    print(name)
                    self.scene[name].visible = True
                    self.player.center_x = self.lastX
                    self.player.center_y = self.lastY
                    globalVars.LIFES -= 1
                    if globalVars.APPEND_LIFES > 0:
                        globalVars.APPEND_LIFES -= 1
            except:
                pass
        
        
        self.update_player_velocity()
        self.centerCameraFromPlayer()
        self.physicsEngine.update()
        self.scene.get_sprite_list("Player").update_animation()
        if self.canPass:
            
            self.window.show_view(self.nextRoom)
        if globalVars.LIFES <= 0:
            globalVars.LIFES = globalVars.TOTAL_LIFES
            self.window.show_view(self.gameOverView)
    
    
        