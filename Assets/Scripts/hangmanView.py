import sounds
import arcade
import globalVars

class Letter(arcade.SpriteSolidColor):
    def __init__(self, color,font,x,y,letter,isIn):
        super().__init__(font, font, color)
        self.letter = letter
        self.font = font
        self.center_x = x
        self.center_y = y
        self.isIn = isIn
        self.isTouched = False
        
        

class HangmanView(arcade.View):
    global globalVars
    def __init__(self, window: arcade.Window,word:str,op = 5):
        super().__init__(window)
        self.word = word
        self.canPass = False
        self.gameView = None
        self.op = op
        self.startOp = op
        self.letters = []
        for l in self.word:
            self.letters.append(l.upper())
        self.discoveredLetters = ["_" for i in range(len(self.letters))]
        self.l = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        self.fontSize = 30
        self.lettersSpriteList: arcade.SpriteList[Letter] = arcade.SpriteList()
        totalWidth = len(self.l) * (self.fontSize + 10)
        x = (self.window.width - totalWidth)/2
        width = totalWidth / len(self.l)
        
        for l in self.l:
            if self.letters.count(l):
                isIn = True
            else:
                isIn = False
            letter = Letter(arcade.color.WHITE,self.fontSize,x,200,l,isIn)
            self.lettersSpriteList.append(letter)
            x+=width
        
    def on_draw(self):
        arcade.start_render()
        self.clear()
        arcade.draw_text(f"Oportunidades: {self.op}/{self.startOp}",self.window.width/2,self.window.height,font_name="Retro Gaming",font_size=24,anchor_x="center",anchor_y="top")
        totalWidth = len(self.discoveredLetters) * (50 + 20)
        x = (self.window.width - totalWidth) / 2
        width = totalWidth / len(self.discoveredLetters)
        for l in self.discoveredLetters:
            arcade.draw_text(l,x,self.window.height*.6,font_name="Retro Gaming",font_size= 50,anchor_x="center",anchor_y="center")
            x += width
            
        for l in self.lettersSpriteList:
            arcade.draw_text(l.letter,l.center_x,l.center_y,l.color,l.font,anchor_x="center",anchor_y="center",font_name="Retro Gaming")
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        
        for b in arcade.get_sprites_at_point((x,y),self.lettersSpriteList):
            
            if self.letters.count(b.letter):
                for i in range(len(self.letters)):
                    if self.letters[i] == b.letter:
                        self.discoveredLetters[i] = b.letter
                if not self.discoveredLetters.count("_"):
                    self.canPass = True
                    self.window.show_view(self.gameView)
            else:
                self.op -= 1
                if self.op == 0:
                    globalVars.LIFES -= 1
                    if globalVars.APPEND_LIFES:
                        globalVars.APPEND_LIFES -= 1
                    self.window.show_view(self.gameView)            