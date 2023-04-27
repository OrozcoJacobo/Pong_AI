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
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pg.font.SysFont('comicsans', 50)
WINNING_SCORE = 10
#Title of the window
pg.display.set_caption("Pong")


#Since we are going to have multiple paddles I dont want to rewrite the code, so this is a Paddle object
class Paddle:
    COLOR = WHITE
    VELOCITY = 4
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self, WINDOW):
        pg.draw.rect(WINDOW, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up = True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x     
        self.y = self.original_y   


class Ball:
    MAX_VELOCITY = 5
    COLOR = WHITE
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pg.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1


#Function that manages draWINDOWg, it takes one variables(window its going to draw on)
def draw(window, paddles, ball, left_score, right_score):
    window.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)

    window.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    window.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

   

    for paddle in paddles: 
        paddle.draw(window)

    #Draw a dotted line in the middle of the window to act as net
    for i in range(10, HEIGHT, HEIGHT//20):#loop 20 times (maybe 19)
        #The idea is to draw a bunch of rectangles to represent kind of a dashed or dotted line 
        if i % 2 == 1: #Essentially what this means is if i is an even number 
            continue
        pg.draw.rect(window, WHITE, (WIDTH//2 -5, i, 10, HEIGHT//20))

    ball.draw(window)
    pg.display.update()


#Funtion tu handle paddle movement
def handle_paddle_movement(keys, left_paddle, right_paddle):
    #Check if the user is pressing the keys and making sure that the paddles can't go off screen
    if keys[pg.K_w] and left_paddle.y - left_paddle.VELOCITY >=0:
        left_paddle.move(up = True)
    if keys[pg.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up = False)

    if keys[pg.K_UP] and right_paddle.y - right_paddle.VELOCITY >=0:
        right_paddle.move(up = True)
    if keys[pg.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up = False)


#Function to handle collisions
def handle_collision(ball, left_paddle, right_paddle):
    #if the ball is going to hit the bottom of the cieling 
    if ball.y + ball.radius >= HEIGHT: #ball.y is the center of the ball, use paint to imagine calculating the distance between the center of the pallet to the center of the ball to determine rebound
        ball.y_velocity *= -1 
    elif ball.y - ball.radius <= 0:
        ball.y_velocity *= -1
    
    #Check if we are hitting the left paddle or the right paddle
    #Left paddle
    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1 

                #Now to deal with the angle for rebound
                #Calculate the displacement between the ball and the center of the paddle and then determine the angle of that to bounce it off  
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                #Determine what the velocity should be 
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_velocity

    else: 
        #right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1

                
                #Now to deal with the angle for rebound
                #Calculate the displacement between the ball and the center of the paddle and then determine the angle of that to bounce it off  
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                #Determine what the velocity should be 
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_velocity

        

#Implementation of the main loop of my program -- Will display the window and then draw something onto it 
def main():
    #variables used to show the display and handle the events 
    #Whenever you have a pygame game one needs a main loop--constantly running that's handling everything related to our game
    run = True
    
    
    #Implement clock, so that regulati is established on the frame rate
    clock = pg.time.Clock()


    #Create the paddles, to undestand why this is like this, its best to go to paint, draw the window and place the paddles and do the math yourself
    #Remember the top left corner is coordinates (0,0), so the bottom right corner is your heigth
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    #Creating the ball
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    #Variable for score system
    left_score = 0
    right_score = 0


    while run:
        clock.tick(FPS)
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)
        #This for loop will get all of the events--ie like clicking mouse, clicking keyboard, closing window
        for event in pg.event.get():
            #The fist event to check is if the player is actually closing the window
            #So basically check if we hit the red close button
            if event.type == pg.QUIT:
                run = False
                break
        #This is going to give us a list containing all of the different keys that have been pressed 
        keys = pg.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0: 
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False

        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_test = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, WHITE)
            WINDOW.blit(text, (WIDTH//2 - text.get_widht()//2, HEIGHT//2 - text.get_height()//2))
            pg.display.update()
            pg.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    #Quit pygame and close the program
    pg.quit()


#Call the main function, note that this is done in the interest of the 
if __name__ == '__main__':
    main()



