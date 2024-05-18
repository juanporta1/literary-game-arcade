import arcade
import arcade.gui
from game import Game

class MenuView(arcade.View):

    def __init__(self, window,):
        super().__init__(window)
    
        self.menu = self.principalMenu()
        self.menu.enable()
        
    def on_draw(self):
        self.clear()
        self.menu.draw()
        
    def principalMenu(self):
        principalManager = arcade.gui.UIManager()

        vBox = arcade.gui.UIBoxLayout()
        text = arcade.gui.UILabel(text="Habia una vez...",font_name="Retro Gaming",font_size=30)
        vBox.add(text.with_space_around(0,0,20,0))

        

        buttonStyle = {
            "font_name": "Retro Gaming",
        }

        play = arcade.gui.UIFlatButton(text="Jugar",style=buttonStyle,width=300,height=75)
        vBox.add(play.with_space_around(10,0,10,0))
        play.on_click = self.inPressPlay
        exit = arcade.gui.UIFlatButton(text="Volver al Menu Principal",style=buttonStyle,width=300,height=75)
        vBox.add(exit.with_space_around(10,0,10,0))
        exit.on_click = self.inPressExit
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
        self.window.show_view(gameView)
    
    def inPressExit(self,event):
        
        self.window.close()
      
    def on_hide_view(self):
        self.menu.disable()
    
    def on_show_view(self):
        self.menu.enable()