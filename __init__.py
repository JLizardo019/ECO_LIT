"""
Made and written by: Julie Lizardo
"""

import pygame as pg,sys
import random as r
from pygame.locals import *

# display box
import tkinter
from tkinter import messagebox

#hide main window
root = tkinter.Tk()
root.withdraw()


# start pygame
pg.init()
pg.font.init()
pg.mixer.init()
myfont = pg.font.SysFont('Verdana', 30)
DISPLAYSURF=pg.display.set_mode((700,700))

# Background
bkgd = pg.image.load('Images/background.jpg')
background = pg.transform.scale(bkgd, (700,700))

# Background Music
# Source Music: https://www.bensound.com
music1 = pg.mixer.Sound("Images/bensound-jazzyfrenchy.ogg")
music1.set_volume(0.5)
music1.play(-1)

# window name
pg.display.set_caption("ECO_LIT")


class Bottle:
    def __init__(self):
        self.image = pg.image.load('Images/waterbottle.png').convert_alpha()
        self.bottle = pg.transform.scale(self.image, (60,60))
        self.rect=self.bottle.get_rect()
    def display(self):
        DISPLAYSURF.blit(self.bottle, self.rect)

class Bin:
    def __init__(self):
        self.image = pg.image.load('Images/bin.png').convert_alpha()
        self.bin = pg.transform.scale(self.image, (90,110))
        self.rect = self.bin.get_rect()
        self.rect.x = 300
        self.rect.y = 600
    def keyboard_move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
             self.rect.x -= 20
        if keys[pg.K_RIGHT]:
             self.rect.x += 20
    def display(self):
        if self.rect.x < 600 and self.rect.x >0:
            DISPLAYSURF.blit(self.bin, self.rect)
        elif self.rect.x >= 600:
            self.rect.x = 600
            DISPLAYSURF.blit(self.bin, self.rect)
        else:
            self.rect.x = 0
            DISPLAYSURF.blit(self.bin, self.rect)


result= "yes"
while result =="yes":
    bin= Bin()
    # make bottle row
    bottleslist=[]
    for i in range(6): #6 bottles on the screen at all times
        b = Bottle()
        b.rect.x = r.randint(0, 600)
        b.rect.y = 0
        bottleslist.append(b)

    notcaught= ""
    caught=0

    #game loop
    while len(notcaught)<3:
        DISPLAYSURF.blit(background, (0,0))
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()


        bin.keyboard_move()

        textscore = myfont.render('Plastic Bottles Recycled: '+str(caught), False, (0, 100, 0))
        DISPLAYSURF.blit(textscore, (0, 0))
        missed = myfont.render('Missed: ' + str(notcaught), False, (255, 0, 0))
        DISPLAYSURF.blit(missed, (0, 50))

        bin.display()

        # falling bottles
        rownum=1
        for i in bottleslist:
            # display bottle
            i.display()

            # Move the bottle down 5 pixels
            i.rect.y += (2*rownum)

            # If the bottle has moved off the bottom of the screen
            if i.rect.y >= 650:
                # Reset it just above the top
                i.rect.y = -1
                notcaught +="X"
                # Give it a new x position
                x = r.randint(0, 600)
                i.rect.x = x

            #did they catch any bottles?
            if i.rect.colliderect(bin.rect):
                # sound effect
                #https://freetousesounds.com/glass-bottle-rolling-sound-effects-crushing-plastic-bottle/
                effect= pg.mixer.Sound("Images/bottle_sound.ogg")
                effect.set_volume(1)
                effect.play()

                caught+=1
                # Reset it just above the top
                i.rect.y = -1
                # Give it a new x position
                x = r.randint(0, 600)
                i.rect.x = x


            rownum += 0.5



        pg.display.flip()
        pg.time.delay(50)

    f_num = r.randint(0,4)
    facts =['Did you know:\n"91% of plastic isn\'t recycled." (National Geographic)',
            'Did you know:\n"Plastic takes more than 400 years to degrade, so most of it still exists in some form." (National Geographic)',
            'Did you know:\n"8 million metric tons of plastic ends up in the oceans every year." (National Geographic)',
            'Did you know:\nYou can replace up to 1,460 plastic water bottles by using a reusable bottle for one year. (Arcadia Power)',
            'Did you know:\n"1 to 5 trillion plastic bags are consumed worldwide everyyear. If tied together, 5 trillion plastic bags would cover an area twice the size of France." (UNEP)'
            ]
    message = "Great Job! You recycled "+str(caught)+ " plastic water bottles!\n\n"+ facts[f_num]

    messagebox.showinfo("Result", message)
    result= messagebox.askquestion("Continue", "Do you want to play again?", icon='warning')
    if result == 'no':
        pg.quit()
        sys.exit()