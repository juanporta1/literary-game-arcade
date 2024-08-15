import arcade
import functions
import sounds
import random
import globalVars
class Player(arcade.Sprite):
    global globalVars
    
    def updateFrame(self,spritesList):    
        
        if self.indexAnimation < len(spritesList) - 1:
            self.texture = spritesList[self.indexAnimation]
            self.indexAnimation += 1
            self.time= 0
        else:
            self.texture = spritesList[self.indexAnimation]
            self.indexAnimation = 0
            self.time = 0
    
    def __init__(self,x,y,scale):
        super().__init__(filename="Assets/Sprites/Player/PlayerSprites/Idle/idle_down/tile000.png",center_x= x, center_y=y,scale= scale,hit_box_detail=1)
        self.indexAnimation = 0
        self.idle_down = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Idle/idle_down/tile00",8)
        self.idle_leftdown = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Idle/idle_leftdown/tile00",8)
        self.idle_rightdown = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Idle/idle_rightdown/tile00",8)
        self.idle_up = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Idle/idle_up/tile00",8)
        self.idle_leftup = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Idle/idle_leftup/tile00",8)
        self.idle_rightup = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Idle/idle_rightup/tile00",8)
        
        self.walk_down = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Walk/walk_down/tile00",8)
        self.walk_leftdown = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Walk/walk_leftdown/tile00",8)
        self.walk_rightdown = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Walk/walk_rightdown/tile00",8)
        self.walk_up = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Walk/walk_up/tile00",8)
        self.walk_leftup = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Walk/walk_leftup/tile00",8)
        self.walk_rightup = functions.createAnimationList("Assets/Sprites/Player/PlayerSprites/Walk/walk_rightup/tile00",8)
        
        self.death_down = functions.reverseCreateAnimationList("Assets/Sprites/Player/PlayerSprites/Death/death_down/tile00",7)
        self.death_rightdown = functions.reverseCreateAnimationList("Assets/Sprites/Player/PlayerSprites/Death/death_rightdown/tile00",7)
        self.death_leftdown = functions.reverseCreateAnimationList("Assets/Sprites/Player/PlayerSprites/Death/death_leftdown/tile00",7)
        self.death_up = functions.reverseCreateAnimationList("Assets/Sprites/Player/PlayerSprites/Death/death_up/tile00",7)
        self.death_leftup = functions.reverseCreateAnimationList("Assets/Sprites/Player/PlayerSprites/Death/death_leftup/tile00",7)
        self.death_rightup = functions.reverseCreateAnimationList("Assets/Sprites/Player/PlayerSprites/Death/death_rightup/tile00",7)
        
        self.lastLifes = globalVars.LIFES
        self.lastMove = 'down'
        self.time = 0
        self.wasDeath = False
        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False
        self.animationList = self.idle_down
        self.canPlay = False
        self.set_hit_box(((-5,-12),(5,-12),(5,-6),(-5,-6)))
        
    def update_animation(self, delta_time: float = 1 / 60):
        
        if self.lastLifes > globalVars.LIFES:
            self.lastLifes = globalVars.LIFES
            self.wasDeath = True
            if self.indexAnimation != 0:
                self.indexAnimation = 0
        if self.lastLifes < globalVars.LIFES:
            self.lastLifes = globalVars.LIFES        
        
        self.time += delta_time
        
        
        
        if not self.wasDeath:
            if self.change_x == 0 and self.change_y == 0: 
                if self.lastMove == 'down':
                    self.animationList = self.idle_down
                elif self.lastMove == 'up':
                    self.animationList = self.idle_up
                elif self.lastMove == 'leftdown':
                    self.animationList = self.idle_leftdown
                elif self.lastMove == 'rightdown':
                    self.animationList = self.idle_rightdown
                elif self.lastMove == 'leftup':
                    self.animationList = self.idle_leftup
                elif self.lastMove == 'rightup':
                    self.animationList = self.idle_rightup
                
            if self.change_x != 0 or self.change_y != 0:
                if self.moveDown and not self.moveLeft and not self.moveRight:
                    self.animationList = self.walk_down
                    self.lastMove = 'down'
                elif self.moveUp and not self.moveRight and not self.moveLeft:
                    self.animationList = self.walk_up
                    self.lastMove = 'up'
                elif self.moveLeft and not self.moveRight and not self.moveUp:
                    self.animationList = self.walk_leftdown
                    self.lastMove = 'leftdown'
                elif not self.moveLeft and self.moveRight and not self.moveUp:
                    self.animationList = self.walk_rightdown
                    self.lastMove = 'rightdown'
                elif self.moveUp and not self.moveLeft and self.moveRight:
                    self.animationList = self.walk_rightup
                    self.lastMove = 'rightup'
                elif self.moveUp and not self.moveRight and self.moveLeft:
                    self.animationList = self.walk_leftup
                    self.lastMove = 'leftup'
                    
        
            if self.time >= .125:
                self.updateFrame(self.animationList)
                self.canPlay = True
            if (self.indexAnimation == 1 or self.indexAnimation == 5) and (self.change_x != 0 or self.change_y != 0)and self.canPlay:
                sounds.footsteps[random.randint(0,2)].play()
                self.canPlay = False
        else:
            
                
            if self.lastMove == 'down':
                    self.animationList = self.death_down
            elif self.lastMove == 'up':
                self.animationList = self.death_up
            elif self.lastMove == 'leftdown':
                self.animationList = self.death_leftdown
            elif self.lastMove == 'rightdown':
                self.animationList = self.death_rightdown
            elif self.lastMove == 'leftup':
                self.animationList = self.death_leftup
            elif self.lastMove == 'rightup':
                self.animationList = self.death_rightup
                
            if self.time >= .2:
                self.updateFrame(self.animationList)
            
            if self.indexAnimation == len(self.death_down) - 1:
                self.wasDeath = False
    