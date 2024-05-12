import arcade
import functions

class Player(arcade.Sprite):
    
    
    def updateFrame(self,spritesList,side):    
        
        if self.indexAnimation < len(spritesList) - 1:
            self.texture = spritesList[self.indexAnimation][side]
            self.indexAnimation += 1
            self.time= 0
        else:
            self.texture = spritesList[self.indexAnimation][side]
            self.indexAnimation = 0
            self.time = 0
    
    def __init__(self,x,y,scale):
        super().__init__(filename="Assets/Sprites/Player/Individual Sprites/adventurer-idle-2-00.png",center_x= x, center_y=y,scale= scale)
        self.indexAnimation = 0
        self.animationIdleList = functions.createAnimationList("Assets/Sprites/Player/Individual Sprites/adventurer-idle-2-0",2)
        self.animationWalkList = functions.createAnimationList("Assets/Sprites/Player/Individual Sprites/adventurer-run-0",2)
        
        
        self.isSeeRight = True
        self.time = 0
        
    def update_animation(self, delta_time: float = 1 / 60):
        
        self.time += delta_time
        
        if self.change_x > 0:
            self.isSeeRight = True
        elif self.change_x < 0:
            self.isSeeRight = False
        
        
        if self.change_x == 0 and self.time >= .1: 
           if self.isSeeRight:
                self.updateFrame(self.animationIdleList,0)
           else:
               self.updateFrame(self.animationIdleList,1)
        if self.change_x != 0 and self.time >= .25:
            if self.isSeeRight:
                self.updateFrame(self.animationWalkList,0)
            else:
                self.updateFrame(self.animationWalkList,1)
            
    
                
        