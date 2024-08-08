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
        super().__init__(filename="Assets/Sprites/Player/PlayerSprites/idle_down/tile000.png",center_x= x, center_y=y,scale= scale,hit_box_detail=1)
        self.indexAnimation = 0
        self.idle_down = functions.createAnimationList("Assets/Sprites/idle_down/tile00",8)
        self.idle_leftdown = functions.createAnimationList("Assets/Sprites/idle_leftdown/tile00",8)
        self.idle_rightdown = functions.createAnimationList("Assets/Sprites/idle_rightdown/tile00",8)
        self.idle_up = functions.createAnimationList("Assets/Sprites/idle_up/tile00",8)
        self.idle_leftup = functions.createAnimationList("Assets/Sprites/idle_leftup/tile00",8)
        self.idle_rightup = functions.createAnimationList("Assets/Sprites/idle_rightup/tile00",8)
        
        
        self.isSeeRight = True
        self.time = 0
        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False
        
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
            
    
                
    