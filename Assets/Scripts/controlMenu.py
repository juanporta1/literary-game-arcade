import arcade
import arcade.color
import arcade.color
from arcade.gui import *
import globalVars
class ControlMenu(arcade.View):
    global globalVars
    def __init__(self, window: arcade.Window,next):
        super().__init__(window)
        self.next = next
        self.menu = self.createMenu()
    def createMenu(self):
        labelStyle = {
            "font_name": "Retro Gaming",
        }
        
        manager = UIManager()
        principalBoxV = UIBoxLayout(space_between=20,align="left")
        
        
        
        moveBoxH = UIBoxLayout(vertical=False)
        moveBoxH.add(UILabel(text="Moverse:   ",font_size=14,text_color=arcade.color.WHITE_SMOKE,font_name="Retro Gaming"))
        moveBoxH.add(UILabel(text="W/A/S/D",font_name="Retro Gaming",font_size=20,text_color=arcade.color.BLIZZARD_BLUE))
        principalBoxV.add(moveBoxH)
        
        
        eBoxH = UIBoxLayout(vertical=False)
        eBoxH.add(UILabel(text="Interactuar:   ",font_name="Retro Gaming",font_size=14,text_color=arcade.color.WHITE_SMOKE))
        eBoxH.add(UILabel(text="E",font_name="Retro Gaming",font_size=20,text_color=arcade.color.REDWOOD))
        principalBoxV.add(eBoxH)
        
        spaceBoxH = UIBoxLayout(vertical=False)
        spaceBoxH.add(UILabel(text="Mover Rocas(Mantener):   ",font_name="Retro Gaming",font_size=14,text_color=arcade.color.WHITE_SMOKE))
        spaceBoxH.add(UILabel(text="ESPACIO",font_name="Retro Gaming",font_size= 20, text_color=arcade.color.NEON_GREEN))
        principalBoxV.add(spaceBoxH)
        
        
        escBoxH = UIBoxLayout(vertical=False)
        escBoxH.add(UILabel(text="Pausa:   ",font_name="Retro Gaming",font_size=14,text_color=arcade.color.WHITE_SMOKE))
        escBoxH.add(UILabel(text="ESCAPE",font_name="Retro Gaming",font_size= 20, text_color=arcade.color.VIVID_VIOLET))
        principalBoxV.add(escBoxH)
        
        
        manager.add(UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=principalBoxV))
        return manager
    
    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.next)
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("CONTROLES",self.window.width/2,self.window.height*.9,arcade.color.WHITE_SMOKE,24,font_name="Retro Gaming",anchor_x="center",anchor_y="center")
        self.menu.draw()
        arcade.draw_text("PRESIONE CUALQUIER TECLA PARA VOLVER",self.window.width/2,10,anchor_x="center",font_name="Retro Gaming",font_size=16)
    def on_hide_view(self):
        globalVars.LAST_VIEW = self