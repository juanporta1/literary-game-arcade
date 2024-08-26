import arcade
import arcade.gui
import random
import sounds


class TextView(arcade.View):
    def __init__(self, window: arcade.Window, text: str,nextView: arcade.View,style = {
        "font_name": "Retro Gaming",
        "bg_color": None,
        "bg_color_pressed": None,
        "border_color": None,
        "font_size": 16
    }, bg="Assets/Backgrounds/black.jpg",quickPass = False,time = 2,type = 1,width = 1200, height = 680):
        super().__init__(window)
        self.canPass = False
        self.quickPass = quickPass
        self.time = time
        self.width = width
        self.height = height
        self.text = text
        self.type = type
        self.nextView = nextView
        self.b = True
        self.textsParts = self.text.split(" ")
        self.style = style
        self.currentText = ""
        self.currentTime = 0
        self.label = self.makeText()
        self.image = bg
        self.bg = arcade.load_texture(bg)
        self.touchedKey = 0
        self.sound = sounds.writes[random.randint(0,3)]
        self.maxTime = 0
        self.imageFade = None
        self.time = 1.5
        self.alpha = 255
        self.init = 0
        
        self.wait = 0
    def on_draw(self):
        arcade.start_render()
        self.clear()
        
        arcade.draw_lrwh_rectangle_textured(0,0,1280,720,self.bg)
        self.label.draw()
        arcade.draw_rectangle_filled(self.window.width/2,self.window.height/2,1280,1920,(0,0,0,self.alpha))

    def makeText(self):
        if self.type == 1:
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
        elif self.type == 2:
            if self.canPass:
                pressKey = arcade.gui.UILabel(text="PRESIONE CUALQUIER TECLA PARA CONTINUAR",font_name="Retro Gaming", font_size=15)
            else: 
                pressKey = arcade.gui.UILabel(text=" ",font_size=15,font_name="Retro Gaming")

        
            gui = arcade.gui.UIManager()
            box = arcade.gui.UIBoxLayout()

            label = arcade.gui.UIFlatButton(text=self.currentText, style= self.style,width=self.width,height=self.height)
            box.add(label.with_space_around(0,0,10,0))
            box.add(pressKey)
            gui.add(arcade.gui.UIAnchorWidget(
                child=box,
                anchor_x="center_x",
                anchor_y="center_y"
            ))
        return gui
    
    def on_key_press(self, symbol: int, modifiers: int):
        if self.touchedKey >= 0 and self.touchedKey <= 1 and not self.quickPass and self.type == 1:
          self.touchedKey += 1
        
        elif self.touchedKey >= 0 and self.touchedKey <= 1 and self.type == 2:
          self.touchedKey += 2
        
    
    def on_hide_view(self):
        
        self.canPass = False
        self.textsParts = self.text.split(" ")
        self.currentText = ""
        self.currentTime = 0
        self.touchedKey = False
        self.sound = sounds.writes[random.randint(0,3)]
        self.maxTime = 0
        self.bg = arcade.load_texture(self.image)
        self.init = 1
        self.time = 1.4

    def on_show(self):
        self.init = 0
    def on_update(self, delta_time: float):
        self.wait += delta_time
        if self.init == 0 and self.time >= 0:
            self.time -= delta_time
            if self.time < 0:
                self.time = 0
                self.init = 1
            self.alpha = 255 * abs(self.time/1.5)
            
        elif self.init == 2 or (self.touchedKey >= 2 and not self.quickPass):
            self.time += delta_time
            if self.time >= 1.5:
                self.window.show_view(self.nextView)
            self.alpha = 255 * abs(self.time / 1.5)
            
        
        
    
        self.currentTime += delta_time 
        if self.type == 1:   
            if not self.quickPass:
                if self.touchedKey == 1 or self.touchedKey == 2:
                    time = 0
                else:
                    time = random.random()/2
                if self.currentTime >= time and len(self.textsParts) != 0:
                    word = self.textsParts.pop(0)
                    self.currentText += word + " "
                    self.label = self.makeText()
                    self.currentTime = 0
                    self.sound.play()
                    
                if len(self.textsParts) == 0 and self.currentTime > 1 and self.b:
                    self.canPass = True
                    self.label = self.makeText()
                    self.b = False
                    if self.touchedKey < 2:
                        self.touchedKey = 1
                    

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
                    if self.maxTime >= 2.5:
                        self.init = 2
        if self.type == 2:
            self.currentText = self.text
            self.label = self.makeText()
            if self.currentTime >= 4:
                self.canPass = True
                
                
            