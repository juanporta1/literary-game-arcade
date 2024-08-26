import arcade
import arcade.color
import arcade.color
import arcade.color
import arcade.gui
from Game import Game
from controlMenu import ControlMenu
import globalVars
import sounds
class Button(arcade.SpriteSolidColor):
    def __init__(self, text,fontSize,left,center_y,function,nextView = None):
        width = fontSize * len(text) + 10
        height = fontSize
        super().__init__(width=width, height=height,color=arcade.color.WHITE)
        self.left = left
        self.center_y = center_y
        self.fontSize = fontSize
        self.text = text
        self.nextView = None
        self.pressed = False
        self.selected = False
        self.function = function



class MenuView(arcade.View):
    global globalVars
    def __init__(self, window):
        super().__init__(window)
        self.bg = arcade.load_texture("Assets/Backgrounds/mainMenu.jpeg")
        self.fontSize = 40
        self.alpha = 255
        self.init = 1
        self.time = .75 
        self.nextView = None
        self.gameView = Game(window,self)
        self.controlView = ControlMenu(self.window,self)
        self.buttonList = arcade.SpriteList()
        self.play = Button("Jugar",self.fontSize,50,window.height*.6,self.inPressPlay,self.gameView)
        self.control = Button("Controles",self.fontSize,50,window.height*.5,self.inPressControl,self.controlView)
        self.exit = Button("Salir",self.fontSize,50,window.height*.4,self.inPressExit)
        self.buttonList.append(self.play)
        self.buttonList.append(self.control)
        self.buttonList.append(self.exit)
        
    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0,0,1280,720,self.bg)
        arcade.draw_text("Habia Una Vez...",50,self.window.height*.8,arcade.color.RED_DEVIL,40,anchor_x="left",anchor_y="center",font_name="Retro Gaming")
        for b in self.buttonList:   
            arcade.draw_text(b.text,b.left,b.center_y,b.color,b.fontSize,font_name="Retro Gaming",anchor_x="left",anchor_y="center")
        arcade.draw_rectangle_filled(self.window.width/2,self.window.height/2,self.window.width,self.window.height,(0,0,0,self.alpha))

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if arcade.get_sprites_at_point((x,y),self.buttonList):
            for b in arcade.get_sprites_at_point((x,y),self.buttonList):
                if not b.pressed or not b.selected:
                    b.color = arcade.color.GRAY
                    b.fontSize = 35
                    
                
        else:
            for b in self.buttonList:
                if not b.pressed or not b.selected:
                    b.color = arcade.color.WHITE
                    b.fontSize = self.fontSize
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if arcade.get_sprites_at_point((x,y),self.buttonList):
                for b in arcade.get_sprites_at_point((x,y),self.buttonList):
                    b.color = arcade.color.BLACK
                    b.fontSize = 30
                    b.pressed = True

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if arcade.get_sprites_at_point((x,y),self.buttonList):
                for b in arcade.get_sprites_at_point((x,y),self.buttonList):
                    b.color = arcade.color.BLACK
                    b.fontSize = 40
                    b.selected = True
                    b.pressed = False
                    sounds.select.play()
            for b in self.buttonList:
                b.pressed = False
    
        
    def inPressControl(self):
        self.init = 2
        self.nextView = self.controlView
    def inPressPlay(self):

        self.init = 2
        self.nextView = self.gameView
    def inPressExit(self):
        
        self.window.close()
        
    def on_hide_view(self):
        globalVars.LAST_VIEW = self
    def on_show_view(self):
        self.buttonList = arcade.SpriteList()
        self.play = Button("Jugar",self.fontSize,50,self.window.height*.6,self.inPressPlay,self.gameView)
        self.control = Button("Controles",self.fontSize,50,self.window.height*.5,self.inPressControl,self.controlView)
        self.exit = Button("Salir",self.fontSize,50,self.window.height*.4,self.inPressExit)
        self.buttonList.append(self.play)
        self.buttonList.append(self.control)
        self.buttonList.append(self.exit)
        if globalVars.LAST_VIEW != None:
            self.init = 0
        else:
            self.init = 1
            self.time = 0
            self.alpha = 0
        try:
            if not isinstance(globalVars.LAST_VIEW,ControlMenu) and not globalVars.LAST_VIEW == None:
                self.gameView = Game(self.window,self)
        except:
            pass
    def on_update(self, delta_time: float):
        
        if self.init == 0:
            self.time -= delta_time
            if self.time <= 0:
                self.time = 0
                self.alpha = 0
                self.init = 1
            self.alpha = 255 * (self.time / .75)
        if self.init == 2:
            self.time += delta_time
            if self.time >= .75:
                self.time = .75
                self.alpha = 255
                self.init = 1
                self.window.show_view(self.nextView)
            self.alpha = 255 * (self.time / .75)
        
        
            
        for b in self.buttonList:
            
            if b.pressed:
                b.color = arcade.color.BLACK
                b.fontSize = 30
            if b.selected:
                b.color = arcade.color.BLACK
                b.fontSize = 40
                
                b.function()
        
    
    