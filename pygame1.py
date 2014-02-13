import pygame
def display_box(screen, message):
        fontobject=pygame.font.SysFont('Arial', 18)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
       # pygame.display.flip()


class Pong(object):
      def main(self,screen):
        color =(240,240,240)
        ball_r=240
        ball_g=100
        ball_b=000
        white=(255,255,255)
        black=(0,0,0)
        bat_rect=pygame.Rect(10,10,50,10) 
        pos = (Swidth/2,Sheight/2)
        mx = 20 
        my = 23 
        pos_offset = 2
        x_sign= 1
        y_sign= 1
        wall_rect = pygame.Rect(10,10,Swidth-20,Sheight-20)
        clock1 = pygame.time.Clock()
        offset = 5
        count =0
#This flag is to check if the ball is inside the screen
        inside_flag = True
#For every 10 bounces , increase the speed
        bounces=0
        temp =(0,0)
        bounc_flag=False
        end_flag = False
#Make it black
#rect = pygame.draw.lines(screen,color,0,((0,0),(120,90)),1)
        pygame.draw.rect(screen,white,wall_rect,1)
        pygame.draw.rect(screen,color,bat_rect,1)
        while 1:
#For now , just fill the whole screen , aim for efficiency later
            screen.fill((0,0,0))
            pygame.draw.rect(screen,white,wall_rect,1)
            circ_color = (ball_r,ball_g,ball_b)
            circ_rect = pygame.draw.circle(screen,circ_color,pos,3,0)
            pygame.draw.rect(screen,white,bat_rect,1)
            clock1.tick(30)
            if((bounces>0) and (bounces%10==0)):
                display_box(screen,"Lets speed things a bit :)")
                ball_r = (ball_r+30)%255
                ball_g = (ball_g+50)%255
                ball_b = (ball_b+20)%255
            else:
                display_box(screen,str(bounces))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    return
                if ((event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT)):
                    sign_offset = 1 
                    count = count + 5 
                if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT)):
                    sign_offset = -1  
                    count = count + 5 
            #Collision detection for the ball
            #Bounce on Collision with walls
            bounc_flag=False
            inside_flag = True
            
            if(((circ_rect.left - wall_rect.left) <= 1) or (((wall_rect.right- circ_rect.right)<= 1))):
                x_sign = x_sign*-1
            if((((wall_rect.bottom- circ_rect.bottom)<= 1))):
                y_sign= y_sign*-1
            
            #Bounce on Collision with bat
            bounc_flag = circ_rect.colliderect(bat_rect)
            #if ball hits the sides of the bat , consider as not bounced
            if(bat_rect.contains(circ_rect)==True):
                end_flag=True


            if(((circ_rect.right- bat_rect.left) == 0) or (((circ_rect.left- bat_rect.right)== 0))):
                inside_flag=False
            if((circ_rect.topleft == bat_rect.bottomright) or ((circ_rect.topright == bat_rect.bottomleft))):
                inside_flag=False

            if(bounc_flag==True):
                    y_sign= y_sign*-1
                    bounces +=1
            if((bounces!=0)and (bounces%10 == 0) and (bounc_flag==True)):
                pos_offset +=1
            inside_flag= circ_rect.colliderect(wall_rect)
            if((inside_flag == False) or (end_flag==True)):
                screen.fill((0,0,0))
                msg = "Your score is " + str(bounces)
                display_box(screen,msg)
                pygame.display.flip()
                clock1.tick(1)
                screen.fill((0,0,0))
                msg = "Bye!"
                display_box(screen,msg)
                pygame.display.flip()
                clock1.tick(1)
                return
            mx += x_sign * pos_offset 
            my += y_sign * pos_offset 
            pos = (mx,my)
            if(count>0):
                bat_rect=bat_rect.move((sign_offset * offset,0)) 
                count = count - 1
            bat_rect = bat_rect.clamp(wall_rect)


            #Move the rectangle , let it bounce left and right

#Initialize all pygame modules
pygame.init()
#Create a screen
Swidth = 240
Sheight= 180 
screen = pygame.display.set_mode((Swidth,Sheight))
pygame.key.set_repeat(5,100)
pong_game = Pong()
pong_game.main(screen)
