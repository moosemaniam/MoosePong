import pygame
BLACK=(0,0,0)
WHITE=(255,255,255)
MAX_SPEED=20
FPS = 30
import random

def display_box(screen, message,pos):
        fontobject=pygame.font.SysFont('Arial', 40)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    (pos))
 
class boundary(object):
   def __init__(self,left,top,width,height,color):
    self.left= left
    self.top=top 
    self.width=width 
    self.height=height 
    self.Rect = pygame.Rect(left,top,width,height)
    self.color = color
   def draw(self,screen):
    screen.fill(self.color,self.Rect)
class ball(object):
   bounces=0
   width = 0
   speedx = 10
   speedy = 10
   x_sign = 1
   y_sign = 1
   x_pos=0
   y_pos=0
   def __init__(self,screen,color,pos,radius):
     self.color = color
     self.x_pos = pos[0]
     self.y_pos = pos[1]
     self.radius=radius 
     self.screen = screen
     self.Rect = pygame.draw.circle(self.screen,self.color,pos,self.radius,self.width)
   def print_pos(self):
     print self.x_pos,self.y_pos
   def draw(self):
     pygame.draw.circle(self.screen,self.color,(self.x_pos,self.y_pos),self.radius,self.width)
   def move(self):
     self.x_pos += self.x_sign * self.speedx
     self.y_pos += self.y_sign * self.speedy
     if(self.speedx <3):
         self.speedx=3
     if(self.speedy <3):
         self.speedy=3
     if(self.speedx >MAX_SPEED):
         self.speedx=MAX_SPEED
     if(self.speedy >MAX_SPEED):
         self.speedy=MAX_SPEED
     pos = (self.x_pos,self.y_pos)
   def reset(self):
     w = self.screen.get_width()
     h = self.screen.get_height()
     self.x_pos = random.randint(w/2-30,w/2+30)
     self.y_pos = random.randint(h/2-30,h/2+30)
     self.speedx = random.randint(3,7)
     self.speedy = random.randint(3,7)
     self.x_sign *= -1
     self.y_sign *= -1
     self.draw()
   
class bat(object):
   offset=7
   count_left = 0
   count_right= 0
   score=0
   def __init__(self,left,top,width,height,color,ScreenRect):
       self.Rect = pygame.Rect(left,top,width,height) 
       self.color = color
       self.ScreenRect= ScreenRect 
   def draw(self,screen):
        screen.fill(self.color,self.Rect)
   def move_left(self):
         self.count_left = self.offset
         self.Rect.move_ip(-1*(self.offset),0) 
         self.Rect= self.Rect.clamp(self.ScreenRect)
   def move_right(self):
         self.count_right= self.offset
         self.Rect.move_ip(self.offset,0) 
         self.Rect= self.Rect.clamp(self.ScreenRect)
   def update_stuff(self):
            self.move_right_delayed()
            self.move_left_delayed()
   def move_left_delayed(self):
          if(self.count_left>0):
            self.Rect.move_ip(-1*self.offset,0) 
            self.Rect= self.Rect.clamp(self.ScreenRect)
          self.count_left -=1
   def move_right_delayed(self):
          if(self.count_right>0):
            self.Rect.move_ip(self.offset,0) 
            self.Rect= self.Rect.clamp(self.ScreenRect)
          self.count_right-=1
#ai bat is going to follow the ball and try to hit it

class ai_bat(bat):

   def ai_magic(self,x): 
           if(x <= self.Rect.centerx):
            self.move_left()
           if(x >= self.Rect.centerx):
            self.move_right()

class Pong(object):
      def main(self,screen):
        boundaries = []
        bounc_flag=False
        first_time_flag=True
        wsize = screen.get_width()
        hsize = screen.get_height()
        clock1 = pygame.time.Clock()
        screen.fill(BLACK)
        screen_rect = pygame.Rect(0,0,screen.get_width(),screen.get_height())
   #boundaries
   #def __init__(self,left,top,width,height,color):
        ai_bat1 = ai_bat(10,40,50,10,WHITE,screen_rect)
        bat2 = bat(10,(screen.get_height()-50),50,10,WHITE,screen_rect)
        circle_pos = (10+(screen.get_width()>>1),screen.get_height()>>1)
        circle_radius = 4
        ball1 = ball(screen,WHITE,circle_pos,circle_radius)
        count = 0 
        while 1:
#For now , just fill the whole screen , aim for efficiency later
            count = (count + 1)%(FPS)    
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    return
                    """
                if ((event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT)):
                    bat1.move_right()
                if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT)):
                    bat1.move_left()
                    """
                if ((event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT)):
                    bat2.move_right()
                if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT)):
                    bat2.move_left()

            ball1.move() 
            bat2.update_stuff()
#Ai bat moves only if the ball is moving in its direction
            if(ball1.y_sign ==-1 and (count%20!=0)):
             ai_bat1.ai_magic(ball1.x_pos)
            else:
             ai_bat1.ai_magic(screen.get_width()/2 - (screen.get_width()/2)%(ai_bat1.Rect.width/2))
            ai_bat1.update_stuff()
            #Code for collission detection between the ball and the walls
            b_flag_sides = (ball1.x_pos-ball1.radius <= screen_rect.left) or(ball1.x_pos+ball1.radius >= screen_rect.right)
            b_flag_top = (ball1.y_pos - ball1.radius <=screen_rect.top)
            b_flag_bot= (ball1.y_pos + ball1.radius >=screen_rect.bottom)
            if(b_flag_top):
                bat2.score += 1
            if(b_flag_bot):
                ai_bat1.score += 1
            if(b_flag_sides):
                ball1.x_sign *=-1
            if(b_flag_top or b_flag_bot):
                ball1.reset()
            
            #Code for collission detection between the ball and the walls

            flag1 = ai_bat1.Rect.collidepoint(ball1.x_pos,ball1.y_pos) 
            flag2 = bat2.Rect.collidepoint(ball1.x_pos,ball1.y_pos) 
#            if(flag1):
            if(flag1):
                if((ball1.x_pos >= ai_bat1.Rect.left) and (ball1.x_pos <= ai_bat1.Rect.left + ai_bat1.Rect.width/4)):
                    ball1.speedx +=1
                    ball1.speedy -=1
                    ball1.x_sign =-1
                if((ball1.x_pos >= ai_bat1.Rect.left + 3*ai_bat1.Rect.width/4) and (ball1.x_pos <= ai_bat1.Rect.left + ai_bat1.Rect.width)):
                    ball1.speedx +=1
                    ball1.speedy -=1
                    ball1.x_sign =1
            if(flag2):
                if((ball1.x_pos >= bat2.Rect.left) and (ball1.x_pos <= bat2.Rect.left + bat2.Rect.width/4)):
                    ball1.speedx +=1
                    ball1.speedy -=1
                    ball1.x_sign =-1
                if((ball1.x_pos >= bat2.Rect.left + 3*bat2.Rect.width/4) and (ball1.x_pos <= bat2.Rect.left + bat2.Rect.width)):
                    ball1.speedx +=1
                    ball1.speedy -=1
                    ball1.x_sign =1

            if(flag1 or flag2):
               ball1.y_sign *=-1
               pygame.mixer.music.play()


            ball1.draw()
            ai_bat1.draw(screen)
            bat2.draw(screen)
            ai_bat1.draw(screen)
            msg1 = str(ai_bat1.score)
            display_box(screen,msg1,(wsize-40,30))
            msg2 = str(bat2.score)
            display_box(screen,msg2,(wsize-40,hsize-90))
            pygame.display.flip()

            clock1.tick(FPS)









#Initialize all pygame modules
pygame.init()
#Create a screen
w=400 
h=600
pygame.mixer.init()
pygame.display.set_caption("Moose Pong")
beep1="beep1.wav"
pygame.mixer.music.load(beep1)
screen = pygame.display.set_mode((w,h))
pygame.key.set_repeat(5,100)
pong_game = Pong()
pong_game.main(screen)
