import arcade
import random
from copy import copy
class CrosswordView(arcade.View):
    def __init__(self, window: arcade.Window,word,crossWords):
        super().__init__(window)
        
        self.gameView = None
        self.font_size = 16
        self.principalFontSize = 30
        self.spacesFontSize = 20
        self.word: str = word
        self.crossWords: list[str] = crossWords
        for i in range(len(self.crossWords)):
            
            self.crossWords[i] = self.crossWords[i].upper()
            
        self.letters = []
        for i in range(len(word)):
            letter = word[i].upper()
            self.letters.append(letter)
        
        self.indexs = []
        for i in range(len(word)):
            letter = self.letters[i]
            self.indexs.append([])
            for j in range(len(self.crossWords[i])):
                if self.crossWords[i][j] == letter:
                   self.indexs[i].append(j)
                     

        
        
        
        self.wordsSpriteList = arcade.SpriteList()   
        y = (self.window.height/2) + (self.font_size * (len(self.crossWords)/2)) + 30 * len(self.crossWords)/2
        for i in range(len(self.crossWords)):
                
                sprite = arcade.SpriteSolidColor((len(self.crossWords[i]) * self.font_size)+6,20,arcade.color.GRAY_ASPARAGUS)
                sprite.center_x = self.window.width - sprite.width/2
                sprite.center_y = y
                sprite.startX = copy(sprite.center_x)
                sprite.startY = copy(sprite.center_y)
                sprite.isCatched = False
                sprite.word = self.crossWords[i]
                self.wordsSpriteList.append(sprite)
                y -= self.font_size + 30 
                
        
        self.principalSpriteList = arcade.SpriteList()
        height = len(self.letters) * self.principalFontSize + (len(self.letters) -1) * 50
        diff = self.window.height - height
        y = diff / 2 + height
        height /= len(self.letters)        
        for i in range(len(self.letters)):
            sprite = arcade.SpriteSolidColor(self.principalFontSize,self.principalFontSize,arcade.color.AERO_BLUE)
            sprite.center_x = self.window.width / 2
            sprite.center_y = y
            sprite.wordIndex = self.indexs[i][random.randint(0,len(self.indexs[i])-1)]
            sprite.word = self.crossWords[i]
            sprite.isMaked = False
            self.principalSpriteList.append(sprite)
            y -= height 
        
        self.canPass = False
        
    def on_hide_view(self):
        canPass = self.canPass
        gameView = self.gameView
        self.__init__(self.window,self.word,self.crossWords)
        self.gameView = gameView
        self.canPass = canPass   
         
    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.gameView)
    def on_draw(self):
        arcade.start_render()
        self.clear()

        l = 0
        for s in self.principalSpriteList:
            
            
            center = s.center_x
            x = center - (self.spacesFontSize * s.wordIndex + 20 * s.wordIndex)
            for i in range(len(s.word)):
                if not s.isMaked:
                    if i != s.wordIndex:
                        arcade.draw_text("_",x,s.center_y + 15,font_size=self.spacesFontSize,font_name="Retro Gaming",anchor_x="center",anchor_y="top")
                else:
                    if i != s.wordIndex:
                        arcade.draw_text(f"{s.word[i]}",x,s.center_y + 15,font_size=self.spacesFontSize,font_name="Retro Gaming",anchor_x="center",anchor_y="top")

                x += self.spacesFontSize + 20
                
            arcade.draw_text(f"{self.letters[l]}",s.center_x,s.center_y,font_name="Retro Gaming",font_size=self.principalFontSize,anchor_x="center",anchor_y="center")
            l+=1

        for i in self.wordsSpriteList:
            i.draw()
            arcade.draw_text(f"{i.word}",i.center_x,i.center_y,font_name="Retro Gaming",font_size=self.font_size,anchor_x="center",anchor_y="center")
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        
            try: 
                for s in self.wordsSpriteList:
                    sprite = arcade.get_sprites_at_point((x,y),self.wordsSpriteList)[0]
                    sprite.isCatched = True
                    break
            except:
                pass
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        for s in self.wordsSpriteList:
            s.isCatched = False
            
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        
        
        for s in self.principalSpriteList:
            for mw in self.wordsSpriteList:
                if mw.word != s.word:
                    pass
        
        for s in self.wordsSpriteList:
            
            
            if s.isCatched and s.left + dx >= 0 and s.right + dx <= self.window.width + 50 and s.bottom + dy >= 0 and s.top + dy <= self.window.height:
                    
                s.center_x += dx
                s.center_y += dy
        
    def on_update(self, delta_time: float):
        
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
            if s.right > self.window.width:
                s.center_x -= 1
            if s.bottom < 0:
                s.center_y += 1
            if s.top > self.window.height:
                s.center_y -= 1
                
        
        for s in self.principalSpriteList:
            for mW in arcade.check_for_collision_with_list(s,self.wordsSpriteList):
                
                if mW.word == s.word:
                    s.isMaked = True
                    mW.kill()
                    for s in self.wordsSpriteList:
                        s.isCatched = False
                else:
                    mW.center_x = mW.startX
                    mW.center_y = mW.startY
                    for s in self.wordsSpriteList:
                        s.isCatched = False