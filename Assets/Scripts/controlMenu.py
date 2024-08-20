import arcade
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
        boxV = UIBoxLayout()
        
        boxV.add(UILabel(text="CONTROLES",font_size=24,font_name="Retro Gaming"))
        
        manager.add(UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=boxV))
        return manager
    
    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.next)
        
    def on_draw(self):
        arcade.start_render()
        
        self.menu.draw()
    def on_hide_view(self):
        globalVars.LAST_VIEW = self