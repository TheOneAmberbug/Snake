import pygame
import time
import random
import numpy as np
import csv
import pygame_textinput as pgt
from operator import itemgetter as ig



#Snake Game by Raban Strahl

game_state = "start_menu"


pygame.init()

pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 50)

width = 1200            #Width of the screen in px
height = 800            #Height of the screen in px

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

speed = 50              #Step Size of the snake in px
size = speed            #Size of the snake in px
wait = 50               #Wartezeit in Milisekunden
direction = "right"     #starting direction of the snake
random_x = 500          #starting position of apple X
random_y = 100          #starting position of apple  Y
points = 0              #points of the player
highscore = 0          #highscore of the player
player_x = 100          #starting position of player X
player_y = 100          #starting position of player Y
UpdateCount = 0         #counter for the update of the snake
counter = 0             #counter for the game loop

fps = 1                 #FPS Tracker (0 = off, 1 = on)
stone = 0               #0 = no stones, 1 = 1 stone per point
difficulty = 19         # 1 very slow --- 20 very fast     Recommendation: 16-19
Invincible = 1          #The Snake cannot die through the body (1 = on, 0 = off)
BorderLoop = False          #When activated, the snake can go out of the screen and come back on the other side (1 = on, 0 = off) !! nicht Fehlerfrei !!
Name = ""
bestplayer = ""

text = ""
TextInputActive = False
NameFinished = 0
color = (255, 0, 0)
TextInput = pgt.TextInputVisualizer()
TextInput.font_color = color
TextInput.cursor_blink_interval = 0.5
TextInput.cursor_blink = True
TextInput.cursor_color = color
TextInput.cursor_visible = True
TextToogleCounter1 = 0
TextToogleCounter2 = 0
FPSCount = 0

# csv data

with open ("snake.csv") as f:
   reader = csv.reader(f)
   next(reader)
   for line in reader:
       if len(line) > 1 and line[1].isdigit() and int(line[1]) >= highscore:
           highscore = int(line[1])
           bestplayer = line[0]
           print(bestplayer)
           print(highscore)
   f.close()
#Making Leaderboard from File
with open("snake.csv") as leadfile:
   reader = csv.reader(leadfile)
   next(reader)
   leaderboard = []

   for line in reader:
       if len(line) > 1 and line[0] and line[1].isdigit():
           leaderboard.append((line[0], int(line[1])))

   leadfile.close()

# Sort leaderboard by highscore in descending order
leaderboard_sorted = sorted(leaderboard, key=lambda x: x[1], reverse=True)



#Removing duplicates

deletedentries = 0

for p in range(len(leaderboard_sorted)):
   m = 0
   while m < len(leaderboard_sorted):
       l = m - deletedentries
       if l >= len(leaderboard_sorted) or p >= len(leaderboard_sorted):
           print("break")
           break
       elif p != l and str(leaderboard_sorted[p][0]) == str(leaderboard_sorted[l][0]) and int(leaderboard_sorted[p][1]) == int(leaderboard_sorted[l][1]):
           leaderboard_sorted.pop(l)
           deletedentries += 1
           if l < m:
               m -= 1
           continue
       m += 1




print(leaderboard_sorted)








posx = []
posy = []
stoney = []
stonex = []
stonex.append(random.randrange(0,width,size ))
stoney.append(random.randrange(0, height,size))


print(leaderboard_sorted[0][1])
print(leaderboard_sorted[10][0])



font = pygame.font.SysFont('Calibri', 30)


def draw_leaderboard(screen, leaderboard):
   global leaderboardtitle
   leaderboardtitle = font.render("Leaderboard", True, (255,255,255))



   for i, entry in enumerate(leaderboard_sorted):
       if i <= 10:
           name = entry[0]
           score = str(entry[1])
           leaderboardcontent = font.render(f"{name:<15} | {score:>5}", True, (255,255,255))
           screen.blit(leaderboardcontent, (width - width / 4, 200 + i * 40))






def draw_start_menu():
   global text, TextInputActive,Name,color

   font = pygame.font.SysFont('Calibri', 40)
   title = my_font.render('Snake', True, (255, 255, 255))
   start_button = font.render('Press Space for Start', True, (0, 255, 0))



   screen.fill(("purple"))
   draw_leaderboard(screen, leaderboard_sorted)
   screen.blit(leaderboardtitle, (width-width/6-30, 70))
   screen.blit(title, (width/6, height/4))
   screen.blit(start_button, (width/6, 400))
   pygame.display.update()


def HandleHotkeys():
   global game_state, player_x, player_y, direction, random_x, random_y, points, counter, NameFinished, TextInputActive,stone,fps,BorderLoop,Invincible
   if TextInputActive == False:
       if game_state == "start_menu":
           draw_start_menu()
           keys = pygame.key.get_pressed()
           if keys[pygame.K_SPACE]:
               game_state = "game"
               player_x = 100
               player_y = 100
               direction = "right"
               random_x = 500
               random_y = 100
               points = 0
               counter = 0
               posx.clear()
               posy.clear()
               posx.append(player_x)
               posy.append(player_y)
               stonex.clear()
               stoney.clear()
               stonex.append(random.randrange(0,width,size ))
               stoney.append(random.randrange(0, height,size))
               NameFinished = False
               TextInputActive = False
               TextInput.value = ""
               fps = 0
               stone = 0
               Invincible = 0
               BorderLoop = False


       keys = pygame.key.get_pressed()
       if keys[pygame.K_r]:
           game_state = "start_menu"
       if keys[pygame.K_q]:
           pygame.quit()
           quit()
       if keys[pygame.K_ESCAPE]:
           if game_state == "game":
               time.sleep(1)
               game_state = "pause"
           elif game_state == "pause":
               time.sleep(1)
               game_state = "game"
       if keys[pygame.K_o]:
            stone = 1
       if keys[pygame.K_f]:
            fps = 1
       if keys[pygame.K_i]:
           Invincible = 1
       if keys[pygame.K_b]:
           BorderLoop = True




def TurnUp():
   global direction
   if not direction == "down":
       direction = "up"
def TurnDown():
   global direction
   if not direction == "up":
       direction = "down"
def TurnLeft():
   global direction
   if not direction == "right":
       direction = "left"
def TurnRight():
   global direction
   if not direction == "left":
       direction = "right"
def TurnSnake():
       global direction
       keys = pygame.key.get_pressed()
       if keys[pygame.K_d]:
           if not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a]:
                   TurnRight()
       if keys[pygame.K_w]:
           if not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
                   TurnUp()
       if keys[pygame.K_a]:
           if not keys[pygame.K_d] and not keys[pygame.K_s] and not keys[pygame.K_w]:
                   TurnLeft()

       if keys[pygame.K_s]:
           if not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_w]:
                   TurnDown()

def DrawText():
   global score,highscore,points,highscore_gametext, font, fps
   score = font.render('Points:' + str(points), True, (255, 0, 0))
   highscore_gametext = font.render('Highscore:' + str(highscore), True, (255, 255, 255))
   bestplayertext = font.render('Achieved by:' + bestplayer, True, (255, 255, 255))
   fpstext = font.render('FPS:' + str(round(FPSCount,1)), True, (255, 255, 255))
   if fps == 1:
       screen.blit(fpstext, (width-width/6, 30))
   screen.blit(score, (0,10))
   screen.blit(highscore_gametext, (0,50))
   screen.blit(bestplayertext, (0,90))

def DrawBody():
   global lastmove,body,posx,posy,size,points

   #Länger werden


   for i in range(1, points + 2):
       if lastmove - i >= 0:
           if lastmove - i <= len(posx) - 1:
               body = pygame.draw.rect(screen, "green", pygame.Rect(posx[lastmove - i], posy[lastmove - i], size, size))


   #Startlänge

   body = pygame.draw.rect(screen, "green", pygame.Rect(posx[(lastmove)], posy[(lastmove)], size, size))
   body = pygame.draw.rect(screen, "green", pygame.Rect(posx[(lastmove-1)], posy[(lastmove-1)], size, size))

   if points+3 < len(posx):
       posx.pop(0)
       posy.pop(0)

def DrawStones():
   global stone,stonelength, stoneblock,stonex, stoney,size
   if stone == 1:
       stonelength = len(stoney)
       for x in range(1, stonelength+2):
           if stonelength - x >= 0:
               stoneblock = pygame.draw.rect(screen, (128,128,128), pygame.Rect(stonex[stonelength-x], stoney[stonelength-x], size, size))

def Update():

   global random_x,random_y,player_x,player_y,points,size,posx,posy, apple,head, UpdateCount, lastmove
   screen.fill("purple")

   MoveSnake()
   UpdateCount = 0
   lastmove = len(posx)-1
   DrawBody()
   DrawStones()
   DrawText()
   apple = pygame.draw.rect(screen, "red" , pygame.Rect(random_x,random_y, size, size))
   head = pygame.draw.rect(screen, "black" , pygame.Rect(player_x, player_y, size, size))

   #Position speichern
   posx.append(player_x)
   posy.append(player_y)

   head = pygame.draw.rect(screen, "black" , pygame.Rect(player_x, player_y, size, size))

   #Collision

   AppleCollisonCheck()

   #GameEnd
   IsGameOver()




def MoveSnake():
   global player_x,player_y
   if direction == "up":
       player_y -= speed


   if direction == "down":
       player_y += speed


   if direction == "left":
       player_x -= speed


   if direction == "right":
       player_x += speed


def AppleCollisonCheck():
   global apple, random_x, random_y, points,size,width,height,head
   if apple.colliderect(body) or body.colliderect(apple):
       random_x = random.randrange(0,width, size)
       random_y = random.randrange(0, height, size)
       apple = pygame.draw.rect(screen, "red" , pygame.Rect(random_x,random_y, size, size))



   if head.colliderect(apple):
       random_x = random.randrange(0,width, size)
       random_y = random.randrange(0, height, size)



       points = points + 1
       stonex.append(random.randrange(0,width,size ))
       stoney.append(random.randrange(0, height,size))

def HandleTextInput():
   global TextInput, events,TextInputActive,TextToogleCounter1, TextToogleCounter2, NameFinished,TextInputActive
   if TextInputActive == True:
       TextInput.update(events)
   events = pygame.event.get()
   keys = pygame.key.get_pressed()
   if keys[pygame.K_RETURN]:
       if TextInputActive == True:
               TextToogleCounter1 += 1
               print(TextToogleCounter1)
               if TextToogleCounter1 == 40:
                   TextInputActive = False
                   TextToogleCounter1 = 0
                   TextInput.cursor_color = (0,0,0)
                   print(TextInputActive)
                   NameFinished = True


       if TextInputActive == False:
           TextToogleCounter2 += 1
           print(TextToogleCounter2)
           if TextToogleCounter2 == 40:
               TextInputActive = True
               TextToogleCounter2 = 0
               TextInput.cursor_color = color
               print(TextInputActive)



   if NameFinished == True and TextInput.value != "":
       with open('snake.csv', 'w', newline='') as f:
           writer = csv.writer(f)
           writer.writerow(['name', 'points', 'password'])  # Write header
           for entry in leaderboard_sorted:
               writer.writerow([entry[0], entry[1], "1234"])
       Name = TextInput.value
       with open('snake.csv', 'a',newline='') as f:
           csvheader = ['name', 'points','password']
           csvdata = [Name, points, "1234"]
           writer = csv.writer(f)
           writer.writerow(csvdata)
           f.close()
       NameFinished = False
       game_state = "start_menu"










def LongHandleTextInput():
       global color,text, TextInputActive
       for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
               TextInputActive = True

               color = (255, 0, 0)
           elif event.type == pygame.KEYDOWN and TextInputActive:
               if event.key == pygame.K_RETURN:

                   if TextInputActive == True:
                       TextInputActive = False
                       Name = text
                       color = (0, 255, 0)
                       if NameFinished == 0:

                           with open('snake.csv', 'a',newline='') as f:
                               csvheader = ['name', 'points','password']
                               csvdata = [Name, points, "1234"]
                               writer = csv.writer(f)
                               writer.writerow(csvdata)
                               f.close()
                           NameFinished = 1

               elif event.key == pygame.K_BACKSPACE:
                   text =  text[:-1]
               else:
                   text += event.unicode

               pygame.TEXTINPUT



def GameOverScreen():
   global game_state, points ,highscore,Name, NameFinished,color,TextInputActive,text,TextInputActive








   if points >= highscore:
       highscore = points

   game_state = "game_over"
   screen.fill((0, 0, 0))
   font = pygame.font.SysFont('Calibri', 40)
   title = font.render('Game Over', True, (255, 255, 255))
   points_text = font.render("Points:" + str(points), True, (255, 255, 255))
   highscore_text = font.render("Highscore:" + str(highscore), True, (255, 215, 0))  # Gold color
   restart_button = font.render('R - Restart', True, (0, 255, 0))
   quit_button = font.render('Q - Quit', True, (255, 0, 0))
   savescoretext = font.render('To save your score', True, (255, 255, 255))
   starttypingtext = font.render('Hold RETURN for a second', True, (255, 255, 255))

   HandleTextInput()
   if TextInputActive == True:
       howtotexttext = font.render('Now enter your Name', True, (255, 255, 255))
   screen.blit(savescoretext, (width/2, height/8))
   screen.blit(starttypingtext, (width/2, height/8+savescoretext.get_height()))
   if TextInputActive == True:
       screen.blit(howtotexttext, (width/2, (height/8)+int(starttypingtext.get_height())+int(savescoretext.get_height())))
   screen.blit(TextInput.surface,(width/2, height/2))  #Using new TextInput
   screen.blit(title, (width/6, height/8))
   screen.blit(points_text, (width/6, height/4+50))
   screen.blit(highscore_text, (width/6, height/2-height/4+90))
   screen.blit(restart_button, (width/6, height/1.5))
   screen.blit(quit_button, (width/6, height/1.3))

   pygame.display.update()

def BodyGameOver():
   global game_state
   if Invincible == 0:

                   for r in range(len(posx) - points - 2, len(posx) - 1):

                           if head.colliderect(pygame.Rect(posx[r], posy[r], size, size)):
                               game_state = "game_over"

def BorderGameOver():
   global game_state,BorderLoop,player_x, player_y, width, height, head, body


   if BorderLoop == False:

       if player_x > width-50:
           game_state = "game_over"

       if player_x < 0:
           game_state = "game_over"

       if player_y > height-50:
           game_state = "game_over"

       if player_y < 0:
           game_state = "game_over"


   if BorderLoop == True:
       if player_x >= width-50:
           player_x = 0

       if player_x <= 0:
           player_x = width-100

       if player_y >= height-50:
           player_y = 0

       if player_y <= 0:
           player_y = height-100

def stoneGameOver():
   global game_state
   if stone == 1:
                       for y in range(0, len(stonex)):
                           if head.colliderect(pygame.Rect(stonex[y], stoney[y], size, size)):
                               game_state = "game_over"

def IsGameOver():
   BodyGameOver()
   BorderGameOver()
   stoneGameOver()



temporaryCounter = 0

while running:
   points += 0

   if fps == 1:
       start_time = time.time() # FPS Tracker

   for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False

   HandleHotkeys()
   if game_state == "game":
       TurnSnake()
       counter += 1
       if counter == 1000:   #Important Counter
           UpdateCount += 1


           if UpdateCount == ((difficulty*-1)+21) :
               Update()



           counter = 1

           time.sleep(wait/1000)
           pygame.display.flip()
           dt = clock.tick(60)/1000
           if fps == 1:
               FPSCount = clock.get_fps()



   if game_state == "game_over":



       GameOverScreen()
       #TextInput.update(events)

pygame.quit