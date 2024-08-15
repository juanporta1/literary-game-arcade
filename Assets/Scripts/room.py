import arcade
import arcade.gui
import arcade.key
from Player import Player
import random
from PauseMenu import PauseMenu
from questionsMenu import QuestionMenu
import globalVars
from gameOver import GameOverView
import sounds
from textView import TextView
import pygame
import json
import functions

class Key(arcade.Sprite):
    def __init__(self,x,y, filename: str = None, scale: float = 1,questionMenu: QuestionMenu = None):
        super().__init__(filename = filename,scale = scale, center_x= x, center_y=y)
        
        self.canPass = False
        self.questionMenu = questionMenu

class Life(arcade.Sprite):
    
    def __init__(self, filename: str = "Assets/Sprites/UI/PickupHeart/tile000.png", x = 0,y = 0):
        super().__init__(filename, scale = 2, center_x=x,center_y=y)
        self.time = 0
        self.animationIndex = 0
        self.spriteList = functions.createAnimationList("Assets//Sprites//UI//PickupHeart//tile00",6)
        self.scale = 3
    def update_animation(self, delta_time: float = 1 / 60):
        self.time += delta_time
        
        if self.time >= .15:
            if self.animationIndex == len(self.spriteList) - 1:
                self.animationIndex = 0
            else:
                self.animationIndex += 1
            self.texture = self.spriteList[self.animationIndex]
            self.time = 0  
        
    
class Room(arcade.View):
    global globalVars
    
    def __init__(self,window,menu,game,jsonFile, nextRoom = None):
        super().__init__(window)
        
        self.lastLifes = globalVars.LIFES
        with open(jsonFile,"r") as file:
            data = file.read()
          
        jsonData = json.loads(data)
        keys = jsonData["keys"]
        lifes = jsonData["lifes"]
        self.falseFloorbgs = ["hole1","hole2","hole3","hole4","hole5"]
        self.falseFloorTexts = ["Has caído en un pozo oculto, el castillo guarda más secretos de los que imaginabas.","Has caído en un pozo oculto, cuidado con tus pasos en la oscuridad.","Te has caído en un pozo oculto, vigila mejor tus pasos.","Has caído en un pozo escondido, este castillo tiene trampas inesperadas.","Te has tropezado con un pozo oculto, parece que el castillo no ha revelado todos sus secretos.","Un pozo oculto te ha sorprendido, el camino es más peligroso de lo que pensabas.","Has caído en un pozo oculto, el castillo es más traicionero de lo que parece."]

        self.holeTexts = ["Has caído en un pozo por descuido, un paso en falso te ha costado caro.","Has caído en un pozo, la prisa te jugó una mala pasada.","Te has tropezado y caído en un pozo, un error torpe en el momento equivocado.","Has caído en un pozo, un pequeño desliz y aquí estás.","Has caído en un pozo, un paso en falso fue todo lo que necesitó.","Te has caído en un pozo, un error tonto que te costó caro.","Has caído en un pozo, un tropiezo que no viste venir."]
        
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
            newKey = Key(filename=key["filename"],x=key["center_x"], y=key["center_y"],questionMenu=qm,scale=key["scale"])
            newKey.questionMenu.gameView = self
            self.scene.add_sprite("Key",newKey)
            
        for life in lifes:
            sprite = Life(x= life["x"],y=life["y"])
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
        
        self.manualBridges = []
        
        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"ManualBridge{i}"]:
                    self.manualBridges.append(f"ManualBridge{i}")
                    self.scene[f"ManualBridge{i}"].visible = False
            except:
                break
            
        
        
        self.manualBridgeKeys = []
        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"ManualBridgeKey{i}"]:
                    self.manualBridgeKeys.append(f"ManualBridgeKey{i}")
                    self.scene[f"ManualBridgeKey{i}"].visible = True
            except:
                break
        
         
        self.bridges = []
        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"Bridge{i}"]:
                    self.bridges.append(f"Bridge{i}")
                    self.scene[f"Bridge{i}"].visible = True
            except:
                break
            
        self.holes = []
        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"Hole{i}"]:
                    self.holes.append(f"Hole{i}")
                    self.scene[f"Hole{i}"].visible = True
            except:
                break
        
        self.player.center_x = self.x
        self.player.center_y = self.y
        self.lastX = self.player.center_x
        self.lastY = self.player.center_y
        
        self.fillHeart = arcade.load_texture("Assets/Sprites/UI/fillHeart.png")
        self.emptyHeart = arcade.load_texture("Assets/Sprites/UI/emptyHeart.png")
        
        
        
        self.interface = arcade.gui.UIManager()
        
         
               

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

        for i in range(len(self.manualBridgeKeys)):
            if arcade.check_for_collision_with_list(self.player,self.scene[self.manualBridgeKeys[i]]):
                if self.scene[self.manualBridges[i]].visible:
                    pass
                else:
                    arcade.draw_text("Presiona E Para Activar",(1280/2 - 80),100,font_name="Retro Gaming",font_size=16)
             
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
        if self.player.center_x >= 0 and self.player.center_y >= 0 and not self.player.wasDeath:
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
        
        for i in range(len(self.manualBridges)):
            if arcade.check_for_collision_with_list(self.player,self.scene[self.manualBridgeKeys[i]]) and key == arcade.key.E and not self.scene[self.manualBridges[i]].visible:
                self.scene[self.manualBridges[i]].visible = True
                self.scene[self.manualBridgeKeys[i]].visible = False
                sounds.mechanism.play()
                
                for j in range(len(self.falseFloors)):
                    try:
                        if arcade.check_for_collision_with_list(self.scene[self.manualBridges[i]][0],self.scene[self.falseFloors[j]]):
                            self.scene[self.falseFloors[i]].visible = True
                            print("Entro")
                        
                        
                    except:
                        pass
            
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A or self.player.wasDeath:
            self.player.moveLeft = False
        if key == arcade.key.D or self.player.wasDeath:
            self.player.moveRight = False
        if key == arcade.key.W or self.player.wasDeath:
            self.player.moveUp = False
        if key == arcade.key.S or self.player.wasDeath:
            self.player.moveDown = False
    def checkKeys(self):
        allPasses = []
        for i in self.scene.get_sprite_list("Key"):
            allPasses.append(i.questionMenu.canPass)
        canPass = all(allPasses)
        return canPass
    
    def on_update(self, delta_time: float):
        
        if self.player.wasDeath:
            self.player.moveDown = False
            self.player.moveLeft = False
            self.player.moveRight = False
            self.player.moveUp = False
        
        if self.lastLifes < globalVars.LIFES:
            self.lastLifes = globalVars.LIFES
        
        if self.lastLifes > globalVars.LIFES:
            self.lastLifes = globalVars.LIFES
            sounds.lostlife.play()
        self.canPass = self.checkKeys()
        if not globalVars.MUSIC.get_busy() and isinstance(self.window.current_view,self.__class__):
            globalVars.MUSIC = sounds.ambient[random.randint(0,2)]
            globalVars.MUSIC = globalVars.MUSIC.play()
            

        for life in arcade.check_for_collision_with_list(self.player,self.scene["Life"]):
            if globalVars.LIFES < globalVars.TOTAL_LIFES:
                globalVars.LIFES += 1
            else:
                globalVars.APPEND_LIFES += 1
                globalVars.LIFES += 1
            sounds.getlife1.play()

            life.kill()
        if self.holes and not self.bridges:
            for i in range(len(self.holes)):
                if arcade.check_for_collision_with_list(self.player,self.scene[self.holes[i]]):
                    self.holeView = TextView(self.window,self.holeTexts[random.randint(0,len(self.holeTexts)-1)],self,bg=f"Assets/Backgrounds/{self.falseFloorbgs[random.randint(0,len(self.falseFloorbgs)-1)]}.jpg",quickPass=True)
                    self.player.center_x = self.lastX
                    self.player.center_y = self.lastY
                    globalVars.LIFES -= 1
                    if globalVars.APPEND_LIFES > 0:
                        globalVars.APPEND_LIFES -= 1
                    self.window.show_view(self.holeView)
        else:
            for hole in self.holes:
                for bridge in self.bridges:
                    haveTouch = False
                    for i in range(len(self.scene[hole])):
                        if arcade.check_for_collision_with_list(self.scene[hole][i],self.scene[bridge]):
                            haveTouch = True
                            break                        
                    if haveTouch:
                        if arcade.check_for_collision_with_list(self.player,self.scene[hole]) and not arcade.check_for_collision_with_list(self.player,self.scene[bridge]):
                            sounds.fall1.play()
                            self.holeView = TextView(self.window,self.holeTexts[random.randint(0,len(self.holeTexts)-1)],self ,bg=f"Assets/Backgrounds/{self.falseFloorbgs[random.randint(0,len(self.falseFloorbgs)-1)]}.jpg",quickPass=True)
                            self.player.center_x = self.lastX
                            self.player.center_y = self.lastY
                            globalVars.LIFES -= 1
                            if globalVars.APPEND_LIFES > 0:
                                globalVars.APPEND_LIFES -= 1
                            self.window.show_view(self.holeView)
        if self.falseFloors and not self.manualBridges:
            try:    
                for i in range(len(self.falseFloors)):
                    if arcade.check_for_collision_with_list(self.player,self.scene[self.falseFloors[i]]):
                        if self.scene[self.falseFloors[i]].visible == False:
                            sounds.floorbreakings[random.randint(0,len(sounds.floorbreakings))].play()
                        sounds.fall1.play()
                        self.falseFloorView = TextView(self.window,self.falseFloorTexts[random.randint(0,len(self.falseFloorTexts)-1)],self ,bg=f"Assets/Backgrounds/{self.falseFloorbgs[random.randint(0,len(self.falseFloorbgs)-1)]}.jpg",quickPass=True,time=3)
                        self.scene[self.falseFloors[i]].visible = True
                        self.player.center_x = self.lastX
                        self.player.center_y = self.lastY
                        globalVars.LIFES -= 1
                        if globalVars.APPEND_LIFES > 0:
                            globalVars.APPEND_LIFES -= 1
                        
                        self.window.show_view(self.falseFloorView)
            except:
                pass
        else:
            try:
                for floor in self.falseFloors:
                    for bridge in self.manualBridges:
                        haveTouch = False
                        for i in range(len(self.scene[floor])):
                            if arcade.check_for_collision_with_list(self.scene[floor][i],self.scene[bridge]):
                                haveTouch = True
                                break
                        if haveTouch:      
                            if arcade.check_for_collision_with_list(self.player,self.scene[bridge]) and self.scene[bridge].visible:
                                print("Toca con puente")
                                continue
                            elif arcade.check_for_collision_with_list(self.player,self.scene[floor]):
                                sounds.fall1.play()
                                if self.scene[floor].visible == False:
                                    sounds.floorbreakings[random.randint(0,len(sounds.floorbreakings))].play()
                                self.falseFloorView = TextView(self.window,self.falseFloorTexts[random.randint(0,len(self.falseFloorTexts)-1)],self,bg=f"Assets/Backgrounds/{self.falseFloorbgs[random.randint(0,len(self.falseFloorbgs)-1)]}.jpg",quickPass=True,time=3)
                                self.scene[floor].visible = True
                                self.player.center_x = self.lastX
                                self.player.center_y = self.lastY
                                globalVars.LIFES -= 1
                                if globalVars.APPEND_LIFES > 0:
                                    globalVars.APPEND_LIFES -= 1
                                self.window.show_view(self.falseFloorView)
            except:
                pass                
        self.update_player_velocity()
        self.centerCameraFromPlayer()
        self.physicsEngine.update()
        self.scene.get_sprite_list("Player").update_animation()
        self.scene.get_sprite_list("Life").update_animation()
        if self.canPass:
            
            self.window.show_view(self.nextRoom)
        if globalVars.LIFES <= 0:
            globalVars.LIFES = globalVars.TOTAL_LIFES
            self.window.show_view(self.gameOverView)
            
    
    
        