import arcade
import arcade.gui
from Game import Game

class Button(arcade.gui.UIFlatButton):
    def __init__(self, width: float = 100, height: float = 50, text="",style = None):
        super().__init__(width=width, height=height, text =text,style=style)
        
    def on_hover(self):
        self.style = {
            "font_name": "Retro Gaming",
            "font_size": 50,
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed": None,
            "boreder_color_focused":None,
            "font_color": arcade.color.GRAY
        }
    def on_unhover(self):
        self.style = {
            "font_name": "Retro Gaming",
            "font_size": 50,
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed": None,
            "boreder_color_focused":None,
            "font_color": arcade.color.WHITE
        }
    def collides_with_point(self,x,y):
        if (x >= self.x and x <= self.x + self.width) and (y >= self.y and y <= self.y + self.height):
            return True
        else:
            return False


        
class MenuView(arcade.View):

    def __init__(self, window,):
        super().__init__(window)
        self.bg = arcade.load_texture("Assets/Backgrounds/mainMenu.jpeg")
        self.menu = self.principalMenu()
        self.menu.enable()
        
    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0,0,1280,720,self.bg)
        self.menu.draw()
        arcade.set_background_color(arcade.color.BLACK)
        
    def principalMenu(self):
        principalManager = arcade.gui.UIManager()

        vBox = arcade.gui.UIBoxLayout()
        text = arcade.gui.UILabel(text="Habia una vez...",font_name="Retro Gaming",font_size=30)
        vBox.add(text.with_space_around(0,0,20,0))

        

        buttonStyle = {
            "font_name": "Retro Gaming",
            "font_size": 50,
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed": None,
            "boreder_color_focused":None,
        }

        self.play = Button(text="Jugar",style=buttonStyle,width=300,height=75)
        self.play.on_click = self.inPressPlay
        vBox.add(self.play.with_space_around(10,0,10,0))
        
        
        self.exit = Button(text="Salir",style=buttonStyle,width=300,height=75)
        self.exit.on_click = self.inPressExit
        vBox.add(self.exit.with_space_around(10,0,10,0))
        
        principalManager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=vBox
            )
        )

        return principalManager
        
    def inPressPlay(self,event):
        gameView = Game(self.window,self)
        self.play.style = {
            "font_name": "Retro Gaming",
            "font_size": 50,
            "bg_color": None,
            "bg_color_pressed": None,
            "border_color": None,
            "border_color_pressed": None,
            "boreder_color_focused":None,
            "font_color": arcade.color.BLACK
        }
        self.window.show_view(gameView)
    
    def inPressExit(self,event):
        
        self.window.close()
      
    def on_hide_view(self):
        self.menu.disable()
    
    def on_show_view(self):
        self.menu.enable()
    
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.play.collides_with_point(x,y):
            self.play.on_hover()
            self.menu = self.principalMenu()
            self.menu.enable()
        else:
            self.play.on_unhover()
            self.menu = self.principalMenu()
            self.menu.enable()
        
        if self.exit.collides_with_point(x,y):
            self.exit.on_hover()
            self.menu = self.principalMenu()
            self.menu.enable()
        else:
            self.exit.on_unhover()
            self.menu = self.principalMenu()
            self.menu.enable()