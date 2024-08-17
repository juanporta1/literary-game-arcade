import arcade
import arcade.gui
import sounds
class CodeInput(arcade.View):
    def __init__(self, window: arcade.Window,nextView,code = 1111):
        super().__init__(window)
        self.isExecuting = False
        self.code = str(code)
        self.ourCode = ""
        self.nextView = nextView
        self.interface = self.makeInterface()
        self.interface.enable()
        self.open = False
        self.wait = 0
        self.init = 1
        self.alpha = 255
        self.time = .5
        self.bg = arcade.load_texture("Assets/Backgrounds/codedoor.jpeg")
    def makeOnClickFunction(self,number):
        def onClick(event):
            self.ourCode += number
            self.interface = self.makeInterface()
            self.interface.enable()
        return onClick
    def makeInterface(self):
        manager = arcade.gui.UIManager()
        box = arcade.gui.UIBoxLayout(vertical=True,space_between=20)
        btStyle = {
        "font_size":16,
        "font_name": "Retro Gaming",
        "anchor_x":"center"
        }
        number = 1
        label = arcade.gui.UILabel(text=f"{self.ourCode}",font_name="Retro Gaming",width=200,height=100,font_size=40)
        box.add(label)
        for row in range(3):
            rowBox = arcade.gui.UIBoxLayout(vertical=False,space_between=20)
            for column in range(3):
                button = arcade.gui.UIFlatButton(text=f"{number}",style=btStyle,width=75,height=75)
                button.on_click = self.makeOnClickFunction(str(number))
                number+=1
                rowBox.add(button)
            box.add(rowBox)
        
        zerobutton = arcade.gui.UIFlatButton(text="0",style=btStyle,width=75,height=75)
        zerobutton.on_click = self.makeOnClickFunction(str(0))
        box.add(zerobutton)
        
        bt1 = arcade.gui.UIFlatButton(text="Borrar",width=150,height=50,style=btStyle)
        bt1.on_click = self.reset
        box.add(bt1)
       
        bt1 = arcade.gui.UIFlatButton(text="Atras",width=150,height=50,style=btStyle)
        bt1.on_click = self.exit
        box.add(bt1)
        
        manager.add(
            arcade.gui.UIAnchorWidget(child=box,anchor_x="center_x",anchor_y="center_y")
        )
        return manager
    

    def on_show(self):
        self.interface = self.makeInterface()
        self.interface.enable()
        self.ourCode = ""
        self.wait = 0
        self.init = 0
    def on_hide_view(self):
        self.ourCode = ""
        self.wait = 0
        self.interface.disable()
        self.init = 1
        self.alpha = 255
        self.time = .5
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,self.window.width,self.window.height,self.bg)
        self.interface.draw()
        arcade.draw_rectangle_filled(self.window.width/2,self.window.height/2,self.window.width,self.window.height,(0,0,0,self.alpha))
        
    def reset(self,event = None):
        self.wait = 0
        self.ourCode = ""
        self.isExecuting = False
        self.interface = self.makeInterface()
        self.interface.enable()
    def exit(self,event):
        self.init = 2
    def on_update(self, delta_time: float):
        
        if self.init == 0:
            self.time -= delta_time
            if self.time <= 0:
                self.init = 1
                self.time = 0
            self.alpha = 255 * abs(self.time / .5)
        if self.init == 2:
            self.time += delta_time
            if self.time >= .5:
                self.time = .5
                self.init = 1
                self.window.show_view(self.nextView)
            self.alpha = 255 * abs(self.time / .5)

        
        if len(self.ourCode) == 4:
            self.wait += delta_time
        
        if self.ourCode == str(self.code):
            self.open = True
            
            if not self.isExecuting:
                self.interface.disable()
                sounds.unlock.play()
                self.isExecuting = True
            if self.wait >= 2:
                self.reset()
                self.init = 2
                
        elif self.ourCode != str(self.code) and len(self.ourCode) == 4:
            
            if not self.isExecuting:
                sounds.lock.play()
                self.interface.disable()
                self.isExecuting = True
                
                self.reset()
            
            
            