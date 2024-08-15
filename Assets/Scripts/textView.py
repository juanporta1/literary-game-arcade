import arcade
import arcade.gui
import random
import sounds
class TextView(arcade.View):
    def __init__(self, window: arcade.Window, text: str,nextView: arcade.View,style = {
        "font_name": "Retro Gaming",
        "bg_color": None,
        "bg_color_pressed": None,
        "border_color": arcade.color.WHITE,
        "font_size": 16
    }, bg="Assets/Backgrounds/black.jpg",quickPass = False):
        super().__init__(window)
        self.canPass = False
        self.quickPass = quickPass
        self.text = text
        self.nextView = nextView
        self.textsParts = self.text.split(" ")
        self.style = style
        self.currentText = ""
        self.currentTime = 0
        self.label = self.makeText()
        self.bg = arcade.load_texture(bg)
        self.touchedKey = False
        self.sound = sounds.writes[random.randint(0,3)]
        self.maxTime = 0
    def on_draw(self):
        self.window.clear()
        arcade.draw_lrwh_rectangle_textured(0,0,1280,720,self.bg)
        self.label.draw()
        

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
        if not self.touchedKey:
            self.touchedKey = True
        else:
            self.window.show_view(self.nextView)
    
    def on_hide_view(self):
        self.canPass = False
        self.textsParts = self.text.split(" ")
        self.currentText = ""
        self.currentTime = 0
        self.touchedKey = False
        self.sound = sounds.writes[random.randint(0,3)]
        self.maxTime = 0

    def on_update(self, delta_time: float):
        self.currentTime += delta_time
        if not self.quickPass:
            if self.touchedKey:
                time = 0
            else:
                time = random.random()/2
            if self.currentTime >= time and len(self.textsParts) != 0:
                word = self.textsParts.pop(0)
                self.currentText += word + " "
                self.label = self.makeText()
                self.currentTime = 0
                self.sound.play()
                
            if len(self.textsParts) == 0 and self.currentTime > 1:
                self.canPass = True
                self.label = self.makeText()
        else:
            time = random.random()/3
            if self.currentTime >= time and len(self.textsParts) != 0:
                word = self.textsParts.pop(0)
                self.currentText += word + " "
                self.label = self.makeText()
                self.currentTime = 0
                self.sound.play()    
            if len(self.textsParts) == 0:
                self.maxTime += delta_time
                if self.maxTime >= 2:
                    self.window.show_view(self.nextView)
        