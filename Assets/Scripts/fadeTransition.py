import arcade
import numpy
class FadeTransition(arcade.View):
    
    def __init__(self, window: arcade.Window,lastView: arcade.View,nextView:arcade.View,lastViewTexture,duration = 3):
        super().__init__(window)
        self.change = False
        self.maxTime = duration/2
        self.window = window
        self.nextView = nextView
        self.lastView = lastView
        self.nextViewImage = None
        
        self.lastTexture = arcade.Texture("LastView",image=lastViewTexture)
        
        self.nextTexture = None
        self.alpha = 0
        self.time = 0
        
        
    def on_draw(self):
        arcade.start_render()
        self.clear()
        if not self.change and self.lastTexture != None:
            arcade.draw_lrwh_rectangle_textured(0,0,self.window.width,self.window.height,self.lastTexture)
        elif self.change and self.nextTexture != None:
            arcade.draw_lrwh_rectangle_textured(0,0,self.window.width,self.window.height,self.nextTexture)
        arcade.draw_lrtb_rectangle_filled(0,self.window.width,self.window.height,0,(0,0,0,self.alpha))
        
    def recall(self,nextView,lastView):
        self.time = 0
        self.lastView = lastView
        self.nextView = nextView
        self.window.show_view(self)
        
        
    def on_update(self, delta_time: float):
        
        if not self.change:
            self.time += delta_time
            self.alpha = 255 * (self.time/self.maxTime)
            if self.time >= self.maxTime:
                self.change = True
        else:
            self.time -= delta_time
            self.alpha = 255 * abs((self.time/self.maxTime))    
            if self.time <= 0:
                self.time = 0
                self.change = False
                self.window.show_view(self.nextView)
        