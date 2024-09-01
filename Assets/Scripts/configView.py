import arcade
import arcade.color
import globalVars
from constants import *
from functions import *
class Button(arcade.Sprite):
    def __init__(self,file,x,y,function):
        self.hover = arcade.load_texture(f"{file}/Hover.png")
        self.default = arcade.load_texture(f"{file}/Default.png")
        super().__init__(f"{file}/Default.png",F_ONE,center_x= x,center_y=y)
        self.pressed = False
        self.function = function
        

class ConfigurationView(arcade.View):
    global globalVars
    def __init__(self, window: arcade.Window, nextView):
        super().__init__(window)
        self.nextView = nextView
        self.rightButton = Button("Assets/Sprites/MenuIcons/Icons/rightArrow",self.window.width*.7,self.window.height/2,self.inPressRight)
        self.leftButton = Button("Assets/Sprites/MenuIcons/Icons/leftArrow",self.window.width*.3,self.window.height/2,self.inPressLeft)
        self.buttonList = arcade.SpriteList()
        self.buttonList.append(self.leftButton)
        self.buttonList.append(self.rightButton)
        self.resolutions = ["850×480","1280x720","1920x1080"]
        for i in range(len(self.resolutions)):
            if f"{globalVars.ACTUAL_WIDTH}x{globalVars.ACTUAL_HEIGHT}" == self.resolutions[i]:
                self.index = i
                break
        
        self.actualResolution = self.resolutions[self.index]
        
        self.applyButton = arcade.SpriteSolidColor(len("APLICAR")*TWENTYFOUR,TWENTYFOUR,arcade.color.WHITE)
        self.applyButton.center_x = self.window.width /2
        self.applyButton.center_y = 100
        self.applyList = arcade.SpriteList()
        self.applyList.append(self.applyButton)
    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_text(f"{self.actualResolution}",self.window.width/2,self.leftButton.center_y,font_name="Retro Gaming",font_size=TWENTY,anchor_x="center",anchor_y="center")
        arcade.draw_text("APLICAR",self.window.width/2,self.applyButton.center_y,font_name="Retro Gaming",font_size=TWENTYFOUR,anchor_x="center",anchor_y="center")
        self.buttonList.draw()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if arcade.get_sprites_at_point((x,y),self.buttonList):
            for b in arcade.get_sprites_at_point((x,y),self.buttonList):
                if not b.pressed:
                    b.texture = b.hover
                    b.scale = scaleFloat(.9)
        else:
            for b in self.buttonList:
                if not b.pressed:
                    b.texture = b.default
                    b.scale = F_ONE
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT and arcade.get_sprites_at_point((x,y),self.buttonList):
            for b in arcade.get_sprites_at_point((x,y),self.buttonList):
                b.pressed = True
                b.function()
        for b in arcade.get_sprites_at_point((x,y),self.applyList):
            width = int(self.actualResolution.split("x")[0])
            height = int(self.actualResolution.split("x")[1])
            self.window.width = width
            self.window.height = height
            globalVars.ACTUAL_HEIGHT = height
            globalVars.ACTUAL_WIDTH = width
            self.window.show_view(self.nextView)
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for b in self.buttonList:
                b.pressed = False     
    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.nextView)
        
    def inPressLeft(self):
        if self.index == 0:
            self.index = len(self.resolutions) - 1
        else:
            self.index -= 1
    def inPressRight(self):
        if self.index == len(self.resolutions)-1:
            self.index = 0
        else:
            self.index += 1
    def on_update(self, delta_time: float):
        self.actualResolution = self.resolutions[self.index]