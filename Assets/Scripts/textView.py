import arcade
import arcade.gui

class TextView(arcade.View):
    def __init__(self, window: arcade.Window, text: str,nextView: arcade.View,style = {
        "font_name": "Retro Gaming",
        "bg_color": None,
        "bg_color_pressed": None
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

    def makeText(self):

        if self.canPass:
            pressKey = arcade.gui.UILabel(text="PRESIONE CUALQUIER TECLA PARA CONTINUAR",font_name="Retro Gaming", font_size=15)
        else: 
            pressKey = arcade.gui.UILabel()


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

        if self.currentTime >= .1 and self.textsParts:
            word = self.textsParts.pop(0)
            self.currentText += word + " "
            self.label = self.makeText()
            self.currentTime = 0
        if not self.textsParts:
            self.canPass = True