import arcade
import arcade.color
import arcade.gui
import sounds

class GameOverView(arcade.View):
    
    def __init__(self,window : arcade.Window,menu: arcade.View):
        super().__init__(window)
        
        self.menu = menu
        self.time = 0
        self.size = 0
        self.canPass = False
        self.label = self.printLabel(0,False)
        
    def printLabel(self,delta,canPass):
        if self.size <= 100:
           self.size += delta * 50
           
        if canPass:
            text = arcade.gui.UILabel(text="PRESIONA CUALQUIER TECLA PARA CONTINUAR",font_name="Retro Gaming", font_size=18)
        else:
            text = arcade.gui.UILabel(text="")
        manager = arcade.gui.UIManager()
        box = arcade.gui.UIBoxLayout()
        label = arcade.gui.UILabel(font_name="Retro Gaming", font_size=self.size, text="GAME OVER", text_color= (200,0,0))
        box.add(label)
        box.add(text)
        anchorWidget = arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=box)
        manager.add(anchorWidget)
        return manager
    
    def on_draw(self):
        self.window.clear()
        self.label.draw()
        arcade.set_background_color(arcade.color.BLACK)
    def on_update(self, delta_time: float):
        self.time += delta_time
        
        if self.time >= 12:
            self.canPass = True
            self.label = self.printLabel(delta_time,self.canPass)
        else:
            self.label = self.printLabel(delta_time,self.canPass)
    def on_show(self):
        self.label.enable()
        sounds.defeat.play()
    def on_hide_view(self):
        self.label.disable()
        sounds.defeat.stop()
        
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol and self.canPass:
            self.time = 0
            self.size = 0
            self.window.show_view(self.menu)