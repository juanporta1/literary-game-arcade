import arcade
import arcade.gui
import random
class TextView(arcade.View):
    def __init__(self, window: arcade.Window, text: str,nextView: arcade.View,style = {
        "font_name": "Retro Gaming",
        "bg_color": None,
        "bg_color_pressed": None,
        "border_color": arcade.color.WHITE,
        "font_size": 16
    }):
        super().__init__(window)
        self.canPass = False
        self.text = text
        self.nextView = nextView
        self.textsParts = self.text.split(" ")
        self.style = style
        self.currentText = ""
        self.currentTime = 0
        self.label = self.makeText()
        


    def on_draw(self):
        self.window.clear()
        self.label.draw()
        arcade.set_background_color(arcade.color.BLACK)

    def makeText(self):

        if self.canPass:
            pressKey = arcade.gui.UILabel(text="PRESIONE CUALQUIER TECLA PARA CONTINUAR",font_name="Retro Gaming", font_size=15)
        else: 
            pressKey = arcade.gui.UILabel(text=" ",font_size=15,font_name="Retro Gaming")

       
        gui = arcade.gui.UIManager()
        box = arcade.gui.UIBoxLayout()

        label = arcade.gui.UIFlatButton(text=self.currentText, style= self.style,width=1200,height=680)
        box.add(label.with_space_around(0,0,10,0))
        box.add(pressKey)
        gui.add(arcade.gui.UIAnchorWidget(
            child=box,
            anchor_x="center_x",
            anchor_y="center_y"
        ))
        return gui
    
    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.nextView)

    def on_update(self, delta_time: float):
        self.currentTime += delta_time

        if self.currentTime >=  random.random()/2 and len(self.textsParts) != 0:
            word = self.textsParts.pop(0)
            self.currentText += word + " "
            self.label = self.makeText()
            self.currentTime = 0
        if len(self.textsParts) == 0 and self.currentTime > 1:
            self.canPass = True
            self.label = self.makeText()