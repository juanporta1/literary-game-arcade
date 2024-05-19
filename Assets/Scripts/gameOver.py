import arcade


class GameOverView(arcade.View):
    
    def __init__(self,window : arcade.Window,menu: arcade.View):
        super().__init__(window)
        
        self.menu = menu
        self.time = 0
    def on_draw(self):
        self.window.clear()
        arcade.text_pyglet.draw_text("GAME OVER",font_name="Retro Gaming",font_size=100,color=arcade.color.RED_DEVIL,start_x=1280/2 - 400, start_y=720/2-20)
        arcade.set_background_color(arcade.color.BLACK)
        
    def on_update(self, delta_time: float):
        self.time += delta_time
        if self.time >= 3:
            self.time = 0
            self.window.show_view(self.menu)
        
        