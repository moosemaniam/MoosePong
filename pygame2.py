import pygame
BLACK=(0,0,0)
WHITE=(255,255,255)
WINNING_SCORE=20

def display_box(screen, message,pos):
        fontobject=pygame.font.SysFont('Arial', 12)
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
   speedx = 4
   speedy = 4
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
     pos = (self.x_pos,self.y_pos)
   
class bat(object):
   offset=5
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
        top = boundary(-20,-20,wsize,5+20,WHITE)
        bottom= boundary(0,hsize-5,wsize,5+20,WHITE)
        left= boundary(-20,-20,5+20,hsize,WHITE)
        right= boundary(wsize-5,0,5+20,hsize,WHITE)
        boundaries = [top,bottom,left,right]
        bat1 = bat(10,10,50,5,WHITE,screen_rect)
        bat2 = bat(10,(screen.get_height()-10),50,5,WHITE,screen_rect)
        circle_pos = (10+(screen.get_width()>>1),screen.get_height()>>1)
        circle_radius = 4
        ball1 = ball(screen,WHITE,circle_pos,circle_radius)

        while 1:
#For now , just fill the whole screen , aim for efficiency later
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    return
                if ((event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT)):
                    bat1.move_right()
                if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT)):
                    bat1.move_left()
                if ((event.type == pygame.KEYDOWN and event.key == pygame.K_s)):
                    bat2.move_right()
                if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_a)):
                    bat2.move_left()

            ball1.move() 
            bat1.update_stuff()
            bat2.update_stuff()
            #Code for collission detection between the ball and the walls
            b_flag_LeftorRight= right.Rect.collidepoint(ball1.x_pos,ball1.y_pos) or left.Rect.collidepoint(ball1.x_pos,ball1.y_pos)
            b_flag_ToporBottom= top.Rect.collidepoint(ball1.x_pos,ball1.y_pos) or bottom.Rect.collidepoint(ball1.x_pos,ball1.y_pos)
            if(top.Rect.collidepoint(ball1.x_pos,ball1.y_pos)):
                bat1.score -= 2
            if(bottom.Rect.collidepoint(ball1.x_pos,ball1.y_pos)):
                bat2.score -= 2
            if(b_flag_LeftorRight==True):
                ball1.x_sign *=-1
            if(b_flag_ToporBottom==True):
                ball1.y_sign *=-1
            
            #Code for collission detection between the ball and the walls

            flag1 = bat1.Rect.collidepoint(ball1.x_pos,ball1.y_pos) 
            flag2 = bat2.Rect.collidepoint(ball1.x_pos,ball1.y_pos) 
            if(flag1):
                bat1.score +=1
            if(flag2):
               bat2.score +=1
            if(flag1 or flag2):
               ball1.y_sign *=-1
               ball1.bounces +=1
               if(ball1.bounces %10 == 0):
                 ball1.speedx +=1
                 ball1.speedy +=1
            if(bat2.score == 1 and first_time_flag==True):
                bat1.score = 1
                first_time_flag = False


            ball1.draw()
            bat1.draw(screen)
            bat2.draw(screen)
            msg1 = str(bat1.score)
            display_box(screen,msg1,(wsize-30,0))
            msg2 = str(bat2.score)
            display_box(screen,msg2,(wsize-30,hsize-20))
            pygame.display.flip()
           
            if(bat1.score == WINNING_SCORE): 
                screen.fill(BLACK)
                display_box(screen,"Player 1 wins",(wsize/2,hsize/2))
                pygame.display.flip()
                clock1.tick(3)
                return

            if(bat2.score == WINNING_SCORE):
                screen.fill(BLACK)
                display_box(screen,"Player 2 wins",(wsize/2,hsize/2))
                pygame.display.flip()
                clock1.tick(3)
                return

            clock1.tick(30)









#Initialize all pygame modules
pygame.init()
#Create a screen
w=400 
h=400
pygame.display.set_caption("Moose Pong")
screen = pygame.display.set_mode((w,h))
pygame.key.set_repeat(5,100)
pong_game = Pong()
pong_game.main(screen)
