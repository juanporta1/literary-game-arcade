import arcade
import arcade.gui
import arcade.key
import arcade.key
import arcade.key
import arcade.key
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
from codeInput import CodeInput
from math import *
class Note(arcade.Sprite):
    def __init__(self, x,y,window,text,nextView,bg="Assets/Backgrounds/note1.jpeg",filename="Assets/Sprites/Notes/closeNote.png",scale = 1):
        super().__init__(filename, scale, center_x = x, center_y = y)
        self.view = TextView(window,text,nextView,bg=bg,type=2,style={ "font_name": "Morris Roman","bg_color": None,"bg_color_pressed": None,"border_color": None,"font_size": 25 ,"font_color":arcade.color.BLACK,"font_color_pressed":arcade.color.BLACK},width=800)
        self.set_hit_box(((-60,-60),(20,20),(-20,20),(60,-60)))

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
        notes = jsonData["notes"]
        rocks = jsonData["rocks"]
        self.falseFloorbgs = ["hole1","hole2","hole3","hole4","hole5"]
        self.falseFloorTexts = ["Has caído en un pozo oculto, el castillo guarda más secretos de los que imaginabas.","Has caído en un pozo oculto, cuidado con tus pasos en la oscuridad.","Te has caído en un pozo oculto, vigila mejor tus pasos.","Has caído en un pozo escondido, este castillo tiene trampas inesperadas.","Te has tropezado con un pozo oculto, parece que el castillo no ha revelado todos sus secretos.","Un pozo oculto te ha sorprendido, el camino es más peligroso de lo que pensabas.","Has caído en un pozo oculto, el castillo es más traicionero de lo que parece."]
        self.isInCodeDoor = False
        self.holeTexts = ["Has caído en un pozo por descuido, un paso en falso te ha costado caro.","Has caído en un pozo, la prisa te jugó una mala pasada.","Te has tropezado y caído en un pozo, un error torpe en el momento equivocado.","Has caído en un pozo, un pequeño desliz y aquí estás.","Has caído en un pozo, un paso en falso fue todo lo que necesitó.","Te has caído en un pozo, un error tonto que te costó caro.","Has caído en un pozo, un tropiezo que no viste venir."]
        self.itsOpen = False
        self.canPass = False
        self.nextRoom = nextRoom
        self.speed = 4
        self.jump = 25
        self.wait = 0
        self.game = game
        self.player = Player(jsonData["setup"]["playerX"],jsonData["setup"]["playerY"],jsonData["setup"]["playerScale"])
        self.gameOverView = GameOverView(self.window,menu)
        self.map = arcade.load_tilemap(jsonData["setup"]["tilemap"])
        self.scene = arcade.Scene.from_tilemap(self.map)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        self.scene.add_sprite_list("Key")
        self.scene.add_sprite_list("Life")
        self.scene.add_sprite_list("Note")
        self.scene.add_sprite_list("Rock")
        self.openNote = arcade.load_texture("Assets/Sprites/Notes/openNote.png")
        self.init = 1
        self.time = .75
        self.alpha = 255
        self.touchShadow = False
        self.timeWalkAway = 0
        self.showShadowView = False
        self.shadowTexts = ["Está demasiado oscuro, primero deberías encender las luces.","Conociendo los peligros de este castillo, creo que no es seguro caminar a oscuras.","Está demasiado oscuro para continuar, encuentra la forma de iluminar el camino.","Es demasiado oscuro para avanzar, deberías encontrar la forma de iluminar el lugar primero."]
        
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
        
        for note in notes:
            nt = Note(note["x"],note["y"],self.window,note["text"],self)
            self.scene.add_sprite("Note",nt)
        self.rockEngines = []
        
        for rock in rocks:
            r = arcade.Sprite(f"Assets/Sprites/DecoCastle/rocks/rock{random.randint(3,5)}.png",center_x=rock["x"],center_y=rock["y"],scale=1)
            self.scene.add_sprite("Rock",r)
            self.rockEngines.append(arcade.PhysicsEnginePlatformer(r,self.scene["Wall"],0))
            self.catchedRock = [False,r]
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
        
        self.codeDoors = []
        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"CodeDoor{i}"]:
                    self.codeDoors.append(f"CodeDoor{i}")
            except:
                break
        
        for i in range(1,len(self.codeDoors)+1):
            code = random.randint(1000,9999)
            self.scene[f"CodeDoor{i}"].input = CodeInput(self.window,self,code)
            self.scene[f"Code{i}"].codeView = TextView(self.window,f"{code}",self,bg="Assets/Backgrounds/note1.jpeg",type=2,style={ "font_name": "Morris Roman","bg_color": None,"bg_color_pressed": None,"border_color": None,"font_size": 75 ,"font_color":arcade.color.BLACK,"font_color_pressed":arcade.color.BLACK})
            
        self.shadows = []
        for i in range(1,len(self.scene.sprite_lists)):
            try:
                if self.scene[f"Shadow{i}"]:
                    self.shadows.append(f"Shadow{i}")
            except:
                break
        
        self.rockDoors = []
        for i in range(1,len(self.scene.sprite_lists)+1):
            try:
                if self.scene[f"RockDoor{i}"]:
                    self.rockDoors.append(f"RockDoor{i}")
            except:
                break
        print(self.rockDoors)
        
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
        if not self.showShadowView:    
            
            self.player.moveDown = False
            self.player.moveLeft = False
            self.player.moveRight = False
            self.player.moveUp = False
    
    def on_show(self):
        self.player.center_x = self.lastX
        self.player.center_y = self.lastY
        self.init = 0
        if self.showShadowView:
            self.touchShadow = True
            
        for i in range(1,len(self.codeDoors)+1):
            if self.scene[f"CodeDoor{i}"].input.open:
                self.scene[f"CodeDoor{i}"].visible = False
        
    def toggle(self,a):
        if a:
            return False
        else:
            return True
    def on_draw(self):
        arcade.start_render()
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)
        self.playerCamera.use()
        self.scene.draw()
        for i in self.shadows:
            self.scene[i].draw()
        self.guiCamera.use()
        self.interface.draw()
        
        x = 10
        
        for codeDoor in self.codeDoors:
            if arcade.check_for_collision_with_list(self.player,self.scene[f"{codeDoor}A"]) or arcade.check_for_collision_with_list(self.player,self.scene[f"{codeDoor}B"]):
                if self.scene[codeDoor].visible:
                    arcade.draw_text("Presiona E Para Ingresar el Codigo",(1280/2 - 180),100,font_name="Retro Gaming",font_size=16)
                else:
                    arcade.draw_text("Presiona E",(1280/2 - 80),100,font_name="Retro Gaming",font_size=16)
        for i in range(1,len(self.codeDoors)+1):
            if arcade.check_for_collision_with_list(self.player,self.scene[f"Code{i}"]):
                arcade.draw_text("Presiona E",(1280/2 - 80),100,font_name="Retro Gaming",font_size=16)
        for i in range(globalVars.TOTAL_LIFES + globalVars.APPEND_LIFES):
            if i <= globalVars.LIFES - 1:
                arcade.draw_lrwh_rectangle_textured(x,650,64,64,self.fillHeart)
            else:
                arcade.draw_lrwh_rectangle_textured(x,650,64,64,self.emptyHeart)
            x += 64
        
        for i in range(1,len(self.shadows)+1):
                if arcade.check_for_collision_with_list(self.player,self.scene[f"UnShadow{i}"]) and self.scene[f"Shadow{i}"].visible:
                    arcade.draw_text("Presiona E",(1280/2 - 80),100,font_name="Retro Gaming",font_size=16)
        
        if arcade.check_for_collision_with_list(self.player,self.scene["Key"]):
            arcade.draw_text("Presiona E",(1280/2 - 80),100,font_name="Retro Gaming",font_size=16)

        for i in range(len(self.manualBridgeKeys)):
            if arcade.check_for_collision_with_list(self.player,self.scene[self.manualBridgeKeys[i]]):
                if self.scene[self.manualBridges[i]].visible:
                    pass
                else:
                    arcade.draw_text("Presiona E Para Activar",(1280/2 - 110),100,font_name="Retro Gaming",font_size=16)
                    
        if arcade.check_for_collision_with_list(self.player,self.scene["Note"]):
            arcade.draw_text("Presiona E Para Leer",(1280/2 - 110),100,font_name="Retro Gaming",font_size=16)

        if arcade.check_for_collision_with_list(self.player,self.scene["Rock"]):
            if self.catchedRock[0]:
                pass
            else:
                arcade.draw_text("Manten Espacio Para Empujar",(1280/2 - 110),100,font_name="Retro Gaming",font_size=16)
        
        arcade.draw_rectangle_filled(self.window.width/2, self.window.height/2,self.window.width,self.window.height,(0,0,0,self.alpha))
            
    def update_player_velocity(self):
        if self.catchedRock[0]:
            self.speed = 2
        else:
            self.speed = 4
        
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
            
        if self.catchedRock[0]:
            self.catchedRock[1].change_x = self.player.change_x
            self.catchedRock[1].change_y = self.player.change_y
        else:
            self.catchedRock[1].change_x = 0
            self.catchedRock[1].change_y = 0       
        
    def on_key_press(self, key: int, modifiers: int):
        if self.player.center_x >= 0 and self.player.center_y >= 0 and not self.player.wasDeath and not self.touchShadow:
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
                    self.qm = key.questionMenu
                    self.init = 2
        for i in range(1,len(self.codeDoors)+1):
            if arcade.check_for_collision_with_list(self.player,self.scene[f"Code{i}"]) and self.scene[f"CodeDoor{i}"].visible == True and key == arcade.key.E:
                self.window.show_view(self.scene[f"Code{i}"].codeView)
                
        for i in range(len(self.manualBridges)):
            if arcade.check_for_collision_with_list(self.player,self.scene[self.manualBridgeKeys[i]]) and key == arcade.key.E and not self.scene[self.manualBridges[i]].visible:
                self.scene[self.manualBridges[i]].visible = True
                self.scene[self.manualBridgeKeys[i]].visible = False
                sounds.mechanism.play()
                
                for j in range(len(self.falseFloors)):
                    try:
                        if arcade.check_for_collision_with_list(self.scene[self.manualBridges[i]][0],self.scene[self.falseFloors[j]]):
                            self.scene[self.falseFloors[i]].visible = True 
                    except:
                        pass
        
        for note in arcade.check_for_collision_with_list(self.player,self.scene["Note"]):
            if key == arcade.key.E:
                self.window.show_view(note.view)
                sounds.notes[random.randint(0,len(sounds.notes) - 1)].play()
                note.texture = self.openNote
        for codeDoor in self.codeDoors:
            if arcade.check_for_collision_with_list(self.player,self.scene[f"{codeDoor}A"]) and key == arcade.key.E and self.scene[f"{codeDoor}"].visible == False: 
                   
                codeB = self.scene[f"{codeDoor}B"]
                x = 0
                y = 0
                for sprite in codeB:
                    x += sprite.center_x                    
                    y += sprite.center_y
                
                promX = trunc(x/len(codeB))
                promY = trunc(y/len(codeB))
                self.player.center_x = promX
                self.player.center_y = promY

            elif arcade.check_for_collision_with_list(self.player,self.scene[f"{codeDoor}B"]) and key == arcade.key.E and self.scene[f"{codeDoor}"].visible == False: 
                   
                codeA = self.scene[f"{codeDoor}A"]
                x = 0
                y = 0
                for sprite in codeA:
                    x += sprite.center_x                    
                    y += sprite.center_y
                
                promX = trunc(x/len(codeA))
                promY = trunc(y/len(codeA))
                self.player.center_x = promX
                self.player.center_y = promY
            elif (arcade.check_for_collision_with_list(self.player,self.scene[f"{codeDoor}A"]) or arcade.check_for_collision_with_list(self.player,self.scene[f"{codeDoor}B"])) and self.scene[f"{codeDoor}"].visible and key == arcade.key.E:
                self.window.show_view(self.scene[codeDoor].input)
            
            for i in range(1,len(self.shadows)+1):
                if arcade.check_for_collision_with_list(self.player,self.scene[f"UnShadow{i}"]) and key == arcade.key.E and self.scene[f"Shadow{i}"].visible:
                    self.scene[f"UnShadow{i}"].visible = False
                    self.scene[f"Shadow{i}"].visible = False  
                    
            for rock in arcade.check_for_collision_with_list(self.player,self.scene["Rock"]):
                if key == arcade.key.SPACE and not self.catchedRock[0]:
                    print("Entro en rock true")
                    self.catchedRock = [True,rock]
                    break
                
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A or self.player.wasDeath:
            self.player.moveLeft = False
        if key == arcade.key.D or self.player.wasDeath:
            self.player.moveRight = False
        if key == arcade.key.W or self.player.wasDeath:
            self.player.moveUp = False
        if key == arcade.key.S or self.player.wasDeath:
            self.player.moveDown = False
            
        if key == arcade.key.SPACE and self.catchedRock[0]:
            self.catchedRock = [False,self.catchedRock[1]]
        
    def checkKeys(self):
        allPasses = []
        for i in self.scene.get_sprite_list("Key"):
            allPasses.append(i.questionMenu.canPass)
        canPass = all(allPasses)
        return canPass
        
    def movePlayerAway(self,delta,direction):
        pass
    def on_update(self, delta_time: float):
        self.update_player_velocity()
        self.scene.get_sprite_list("Player").update_animation()
        self.scene.get_sprite_list("Life").update_animation()
        self.canPass = self.checkKeys()
        if self.init == 0:
            self.time -= delta_time
            if self.time <= 0:
                self.init = 1
                self.time = 0
            self.alpha = 255 * abs(self.time/0.75)
        if self.init == 2:
            self.time += delta_time
            if self.time >= .75:
                self.init = 1
                self.time = .75
                self.window.show_view(self.qm)
            self.alpha = 255 * abs(self.time/0.75)
        if self.init == 3:
            self.time += delta_time
            if self.time >= 1.5:
                self.init = 1
                self.time = 1.5
                self.window.show_view(self.nextRoom)
            self.alpha = 255 * abs(self.time/1.5)
        if self.init == 4:
            self.time += delta_time
            if self.time >= 1.5:
                self.init = 1
                self.time = 1.5
                self.window.show_view(self.gameOverView)
            self.alpha = 255 * abs(self.time/1.5)
            
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
            
        
        for i in range(1,len(self.shadows)+1):
            if arcade.check_for_collision_with_list(self.player,self.scene[f"Shadow{i}"]) and self.scene[f"Shadow{i}"].visible and not self.showShadowView:
                s = arcade.check_for_collision_with_list(self.player,self.scene[f"Shadow{i}"])[0]
                
                if arcade.get_sprites_at_point((s.center_x+64,s.center_y),self.scene[f"Shadow{i}"]) or arcade.get_sprites_at_point((s.center_x+64,s.center_y),self.scene["Wall"]): self.right = False
                else: self.right = True
                
                if arcade.get_sprites_at_point((s.center_x-64,s.center_y),self.scene[f"Shadow{i}"]) or arcade.get_sprites_at_point((s.center_x-64,s.center_y),self.scene["Wall"]): self.left = False
                else: self.left = True
                
                if arcade.get_sprites_at_point((s.center_x,s.center_y+64),self.scene[f"Shadow{i}"]) or arcade.get_sprites_at_point((s.center_x,s.center_y+64),self.scene["Wall"]): self.up = False
                else: self.up = True
                
                if arcade.get_sprites_at_point((s.center_x,s.center_y-64),self.scene[f"Shadow{i}"]) or arcade.get_sprites_at_point((s.center_x,s.center_y-64),self.scene["Wall"]): self.down = False
                else: self.down = True 
                    
                self.showShadowView = True
                shadowView = TextView(self.window,self.shadowTexts[random.randint(0,len(self.shadowTexts)-1)],self,bg="Assets/Backgrounds/shadow.jpeg",quickPass=True,time=.5)
                self.window.show_view(shadowView)     
        
        
        if self.touchShadow: 
            
            
            if self.timeWalkAway == 0:
                self.player.moveDown = self.down
                self.player.moveUp = self.up
                self.player.moveLeft = self.left
                self.player.moveRight = self.right
            self.timeWalkAway += delta_time
            if self.timeWalkAway >= .5:
                self.player.moveDown = False
                self.player.moveUp = False
                self.player.moveLeft = False
                self.player.moveRight = False
                self.touchShadow = False
                self.showShadowView = False
                self.timeWalkAway = 0
                
        
        
            
        if globalVars.LIFES <= 0:
            self.window.show_view(self.gameOverView)
            globalVars.LIFES = globalVars.TOTAL_LIFES     
        self.centerCameraFromPlayer()
        self.physicsEngine.update()
        for i in self.rockEngines:
            i.update()
        if self.canPass and not self.itsOpen:
            self.scene["Door"].visible = False
            sounds.openingdoor.play()
            self.itsOpen = True
            
        
        for rock in self.scene["Rock"]:
            for i in range(1,len(self.rockDoors)+1):
                if arcade.check_for_collision_with_list(rock,self.scene[f"RockDoorKey{i}"]) and not self.catchedRock[0]:
                    rock.center_x = self.scene[f"RockDoorKey{i}"][0].center_x
                    rock.center_y = self.scene[f"RockDoorKey{i}"][0].center_y
        
        if arcade.check_for_collision_with_list(self.player,self.scene["Door"]) and not self.scene["Door"].visible:
            self.init = 3
        
            
    
    
        