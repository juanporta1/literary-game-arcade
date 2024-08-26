import arcade
import random
from copy import copy
import sounds
import arcade.color
import globalVars
class CrosswordView(arcade.View):
    global globalVars
    def shuffle(self):
        newList = arcade.SpriteList()
        indexs = []
        while len(indexs) != len(self.crossWords):
            i = random.randint(0,len(self.crossWords)-1)
            if i in indexs:
                continue
            else:
                indexs.append(i)
                newList.append(self.wordsSpriteList[i])
        self.wordsSpriteList = newList
        
    def __init__(self, window: arcade.Window,file,op = 5):
        super().__init__(window)
        self.op = op
        self.startOp = op
        self.gameView = None
        self.alpha = 255
        self.file = file
        self.canPass = False
        self.time = 1
        self.init = 1
        self.font_size = 16
        self.principalFontSize = 30
        self.spacesFontSize = 16
        self.word: str = file["word"]
        self.crossWords: list[str] = file["crosswords"]
        
        for i in range(len(self.crossWords)):
            
            self.crossWords[i] = self.crossWords[i].upper()
            
        self.letters = []
        for i in range(len(self.word)):
            letter = self.word[i].upper()
            self.letters.append(letter)
        
        self.indexs = []
        for i in range(len(self.word)):
            letter = self.letters[i]
            self.indexs.append([])
            for j in range(len(self.crossWords[i])):
                if self.crossWords[i][j] == letter:
                   self.indexs[i].append(j)
                     

        
        
        
        self.wordsSpriteList = arcade.SpriteList()   
        for i in range(len(self.crossWords)):
                
                sprite = arcade.SpriteSolidColor((len(self.crossWords[i]) * self.font_size)+6,20,arcade.color.GRAY_ASPARAGUS)
                sprite.isCatched = False
                sprite.word = self.crossWords[i]
                self.wordsSpriteList.append(sprite) 
                   
        self.principalSpriteList = arcade.SpriteList()
        height = len(self.letters) * self.principalFontSize + (len(self.letters) -1) * 50
        diff = self.window.height - height
        y = diff / 2 + height
        height /= len(self.letters)        
        for i in range(len(self.letters)):
            sprite = arcade.SpriteSolidColor(self.principalFontSize + 50,self.principalFontSize,arcade.color.AERO_BLUE)
            sprite.center_x = self.window.width / 2
            sprite.center_y = y
            sprite.wordIndex = self.indexs[i][random.randint(0,len(self.indexs[i])-1)]
            sprite.word = self.crossWords[i]
            sprite.isMaked = False
            sprite.letterColor = arcade.color.WHITE
            sprite.time = 0
            if random.randint(0,1):
                sprite.hide = True
            else:
                sprite.hide = False
            sprite.count = False
            self.principalSpriteList.append(sprite)
            y -= height
        self.shuffle()
        y = (self.window.height/2) + (self.font_size * (len(self.crossWords)/2)) + 30 * len(self.crossWords)/2
        for sprite in self.wordsSpriteList:
            sprite.center_x = self.window.width - sprite.width/3
            sprite.center_y = y
            sprite.startX = copy(sprite.center_x)
            sprite.startY = copy(sprite.center_y)
            y -= self.font_size + 30 
        
    def on_show(self):
        self.init = 0    
    def on_hide_view(self):
        canPass = self.canPass
        gameView = self.gameView
        self.__init__(self.window,self.file)
        self.gameView = gameView
        self.canPass = canPass   
         
    
    def on_draw(self):
        arcade.start_render()
        self.clear()
        l = 0
        arcade.draw_text("COMPLETA EL CRUCIGRAMA ARRASTRANDO CADA UNA DE LAS ETIQUETAS A SU RESPECTIVA LETRA",self.window.width/2,0,font_name="Retro Gaming",font_size=15,anchor_x="center",anchor_y="bottom")
        arcade.draw_text(f"Oportunidades: {self.op}/{self.startOp}",10,self.window.height,font_name="Retro Gaming",font_size=20,anchor_x="left",anchor_y="top")
        for s in self.principalSpriteList:
            
            
            center = s.center_x
            x = center - (self.spacesFontSize * s.wordIndex + 20 * s.wordIndex)
            for i in range(len(s.word)):
                if not s.isMaked:
                    if i != s.wordIndex and i != " ":
                        arcade.draw_text("_",x,s.center_y + 6,font_size=self.spacesFontSize,font_name="Retro Gaming",anchor_x="center",anchor_y="top")
                else:
                    if i != s.wordIndex:
                        arcade.draw_text(f"{s.word[i]}",x,s.center_y + 6,font_size=self.spacesFontSize,font_name="Retro Gaming",anchor_x="center",anchor_y="top",color=arcade.color.TEA_GREEN)

                x += self.spacesFontSize + 20
            if not s.hide:    
                arcade.draw_text(f"{self.letters[l]}",s.center_x,s.center_y,font_name="Retro Gaming",font_size=self.principalFontSize,anchor_x="center",anchor_y="center",color=s.letterColor)
            else:         
                arcade.draw_text(f"?",s.center_x,s.center_y,font_name="Retro Gaming",font_size=self.principalFontSize,anchor_x="center",anchor_y="center",color=s.letterColor)

            l+=1

        for i in self.wordsSpriteList:
            i.draw()
            arcade.draw_text(f"{i.word}",i.center_x,i.center_y,font_name="Retro Gaming",font_size=self.font_size,anchor_x="center",anchor_y="center")
        arcade.draw_rectangle_filled(self.window.width/2,self.window.height/2,self.window.width,self.window.height,(0,0,0,self.alpha))
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.op != 0:
            try: 
                for s in self.wordsSpriteList:
                    sprite = arcade.get_sprites_at_point((x,y),self.wordsSpriteList)[0]
                    sprite.isCatched = True
                    break
            except:
                pass
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.op != 0:
            for s in self.wordsSpriteList:
                s.isCatched = False
            
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        
        if self.op != 0:
            for s in self.principalSpriteList:
                for mw in self.wordsSpriteList:
                    if mw.word != s.word:
                        pass
            
            for s in self.wordsSpriteList:
                
                
                if s.isCatched and s.left + dx >= 0 and s.right + dx <= self.window.width + 100 and s.bottom + dy >= 0 and s.top + dy <= self.window.height:
                        
                    s.center_x += dx
                    s.center_y += dy
            
    def on_update(self, delta_time: float):
        if self.init == 0:
            self.time -= delta_time
            if self.time <= 0:
                self.init = 1
                self.time = 0
            self.alpha = 255 * (self.time / 1)
        if self.init == 2:
            self.time += delta_time
            if self.time >= 3:
                self.time = 1
                self.alpha = 255
                self.init = 1
                self.window.show_view(self.gameView)
            self.alpha = 255 * (self.time / 3)
        
        
        list = []
        for s in self.principalSpriteList:
            list.append(s.isMaked)
        if all(list):
            self.canPass = True
            self.init = 2 
    
        for s in self.principalSpriteList:
            if s.count:
                s.time += delta_time
            if s.time >= 3:
                s.count = False
                s.time = 0
                if not s.isMaked:
                    s.letterColor = arcade.color.WHITE
                else:
                    s.letterColor = arcade.color.TEA_GREEN
        for s in self.wordsSpriteList:
                    for s2 in self.wordsSpriteList:
                        if arcade.check_for_collision(s,s2) and not s == s2:
                            if s2.left <= s.right:
                                s2.center_x += 1
                            if s2.right >= s.left:
                                s2.center_x -= 1
                                    
                            if s2.bottom <= s.top:
                                
                                s2.center_y += 1
                            if s2.top >= s.bottom:
                                s2.center_y -= 1
                                
        for s in self.wordsSpriteList:
            if s.left < 0:
                s.center_x += 1
            if s.bottom < 0:
                s.center_y += 1
            if s.top > self.window.height:
                s.center_y -= 1
                
        
        for s in self.principalSpriteList:
            for mW in arcade.check_for_collision_with_list(s,self.wordsSpriteList):
                if not mW.isCatched:
                    if mW.word == s.word:
                        s.isMaked = True
                        mW.kill()
                        s.letterColor = arcade.color.TEA_GREEN
                        s.hide = False
                        sounds.success.play()
                        for s in self.wordsSpriteList:
                            s.isCatched = False
                    else:
                        if not s.isMaked:
                            mW.center_x = mW.startX
                            mW.center_y = mW.startY
                            
                            s.letterColor = arcade.color.RED_DEVIL
                            s.count = True
                            sounds.failed.play()
                            self.op -= 1
                            if self.op == 0:
                                self.init = 2
                                globalVars.LIFES -= 1
                                if globalVars.APPEND_LIFES != 0:
                                    globalVars.APPEND_LIFES -= 1
                            for s in self.wordsSpriteList:
                                s.isCatched = False