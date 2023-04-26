#Pong game with AI which teaches itself how to play using an algorithm called NEAT -- 
#NEAT => NEURO EVOLUTION AUGMENTED TOPOLOGIES
#Whilst this code focuses on pong its general ideas and techniques will be usefull for other game projects 
#However before thinking about any AI I must build the pong game 


#Import librarires
import pygame as pg
#Initialize pygame(always necesary)
pg.init()

#This variables are in all caps since they are constants
#Widht and height for our display 
WIDTH, HEIGHT = 700, 500
#Set up the display, where we draw everything to
WIN = pg.display.set_mode((WIDTH, HEIGHT))
#Title of the window
pg.display.set_caption("Pong")

#Implementation of the main loop of my program -- Will display the window and then draw something onto it 
def main():
    #variables used to show the display and handle the events 
    #Whenever you have a pygame game one needs a main loop--constantly running that's handling everything related to our game
    run = True

    while run:
        #This for loop will get all of the events--ie like clicking mouse, clicking keyboard, closing window
        for event in pg.event.get():
            #The fist event to check is if the player is actually closing the window
            #So basically check if we hit the red close button
            if event.tyoe == pg.QUIT:
                run = False
                break
    #Quit pygame and close the program
    pg.quit()




