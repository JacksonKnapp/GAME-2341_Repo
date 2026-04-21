import sys
import pygame
import random
import math

pygame.init()

width = 800
height = 600
size = (width, height)
black = (0,0,0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dinosaur Click Game")

Dinosaur = pygame.image.load("GAME-2341_Repo/ManipulateChickenDrop/dinosaur.png")
powerUp = pygame.image.load("GAME-2341_Repo/ManipulateChickenDrop/powerUp.png")

def distance(x1,x2,y1,y2):
  # returns the distance between two points (x, y) in a 2d plane
  # only realized after I made this math.hypot exists
  return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

iterator = 0
numofDinosaur = 5
numofPowerUp = 0
powerUpX = 0
powerUpY = 0
startX = []
startY = []
speed = []

while iterator < numofDinosaur:
  startX.append(random.randint(0, width - Dinosaur.get_width() + 1))
  startY.append(0 - random.randint(Dinosaur.get_height(), Dinosaur.get_height() * 2))
  speed.append(0.5)
  iterator += 1

replayscreen = False

#Set up game over stuff
bigfont = pygame.font.SysFont(None, 200)
playagaintext = bigfont.render("Play Again?", True, (0,200,0))
pax = width/2 - playagaintext.get_rect().width/2

smallfont = pygame.font.SysFont(None, 100)
yestext = smallfont.render("YES", True, (0, 200, 0))
yesx = width/4 - yestext.get_rect().width/2
notext = smallfont.render("NO", True, (0,200,0))
nox = width - width/4 - yestext.get_rect().width/2

#Game Loop

gameover = False

while gameover == False:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameover = True

  #Clicking on the Dinosaur
  if pygame.mouse.get_pressed()[0]:
    coords = pygame.mouse.get_pos()
    if replayscreen == False:
      iterator = 0
      while iterator < numofDinosaur:
        # checks mouse cursor and position of dinosaurs in an while loop
        if coords[0] >= startX[iterator] and coords[0] <= startX[iterator] + Dinosaur.get_width() and coords[1] > startY[iterator] and coords[1] < startY[iterator] + Dinosaur.get_height():
          startX[iterator] =  random.randint(0, width - Dinosaur.get_width() + 1)
          startY[iterator] = 0 - random.randint(Dinosaur.get_height(), Dinosaur.get_height() * 2)
          speed[iterator] = 0.5
          break
        iterator += 1
    else:
      if coords[0] > yesx and coords[0] < yesx + yestext.get_rect().width and coords[1] > 450 and coords[1] < 450 + yestext.get_rect().height:
        iterator = 0
        while iterator < numofDinosaur:
          startX[iterator] =  random.randint(0, width - Dinosaur.get_width() + 1)
          startY[iterator] = 0 - random.randint(Dinosaur.get_height(), Dinosaur.get_height() * 2)
          speed[iterator] = 0.5
          iterator +=1
        replayscreen = False

      if coords[0] > nox and coords[0] < nox + notext.get_rect().width and coords[1] > 450 and coords[1] < 450 + notext.get_rect().height:
        gameover = True


  #Updating
  if replayscreen == False:
    iterator = 0
    #Game over
    while iterator < numofDinosaur:
      if startY[iterator] + Dinosaur.get_height() > height:
        replayscreen = True
        break
      # checks if the iterated dinosaur is close enough to the powerup
      if numofPowerUp > 0:
        # separated if statements to not waste resources if a power-up is not yet made
        if distance((startX[iterator]),powerUpX,(startY[iterator]), powerUpY) < 50:
          print("POWERED UP!")
          numofPowerUP = 0
        
      startY[iterator] += speed[iterator]
      iterator += 1


  #Drawing

  if replayscreen == False:
    screen.fill(black)
    iterator = 0
    while iterator < numofDinosaur:
      screen.blit(Dinosaur, (startX[iterator], startY[iterator]))
      iterator += 1
    if numofPowerUp == 1:
        screen.blit(powerUp,(powerUpX, powerUpY))

    iterator = 0
  else:
    screen.fill((200,0,0))

    screen.blit(playagaintext, (pax, 150))
    screen.blit(yestext, (yesx, 450))
    screen.blit(notext, (nox, 450))

  pygame.display.flip()

  if numofPowerUp < 1 and random.random() > .999:
    #checks if a powerup already exists. If not, theres a 1% chance of spawning one
    numofPowerUp = 1
    print("Power Up Available")
    powerUpX = random.randint(0, width - powerUp.get_width() + 1)
    powerUpY = 500 - random.randint(powerUp.get_height(), powerUp.get_height() * 2)

pygame.display.quit()