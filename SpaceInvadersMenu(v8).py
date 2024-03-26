import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import subprocess

#Initalising the logo properties
logo_img = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/logo.png")
logo_dims = [249,176]
logo_centre =[125,88]
logo_newdims = [249,176]
logo_pos = [400,75]

#Initalising the high score text properties
score_img = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/highScore%20.png")
score_dims = (141,33)
score_centre =(70,16)
score_newdims = [141,33]
score_pos = [75,575]

#Initalising the start button properties
start_img = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/startButton.png")
start_dims = [827,291]
start_centre =[413,145]
start_newdims = [200,100]
start_pos = [400,300]

#Initalising the exit button properties
exit_img = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/exitButton.png")
exit_dims = [543,277]
exit_centre =[271,138]
exit_newdims = [225,100]
exit_pos = [400,400]
#Dimensions of the game screen
WIDTH = 800
HEIGHT = 600

def mouse_handler(pos):
    global highScore
    #Check if click position is within the start button
    if (pos[0] >= (WIDTH-start_newdims[0]) / 2 and pos[0]<= (WIDTH + start_newdims[0]) / 2 and pos[1] >= (HEIGHT - start_newdims[1]) / 2 and pos[1] <= (HEIGHT + start_newdims[1]) / 2):
        # Start the game by running SpaceInvadersV1.py
        subprocess.run(["python", "SpaceInvadersV8.py"])
        pos = None
    elif (pos[0] >= (WIDTH-exit_newdims[0]) / 2 and pos[0]<= (WIDTH + exit_newdims[0]) / 2 and pos[1] >= (HEIGHT - exit_newdims[1]+200) / 2 and pos[1] <= (HEIGHT + exit_newdims[1]+200) / 2):
        #Exit the game by stopping frame animation
        frame.stop()
        print("Thank you for playing!!!")
                                                             
def draw(canvas):
    #Displays all the images onto the canvas
    canvas.draw_image(logo_img, logo_centre, logo_dims, logo_pos, logo_newdims)
    canvas.draw_image(score_img, score_centre, score_dims, score_pos, score_newdims)
    canvas.draw_image(start_img, start_centre, start_dims, start_pos, start_newdims)
    canvas.draw_image(exit_img, exit_centre, exit_dims, exit_pos, exit_newdims)
    highScore = set_highscore()
    #Score text is displayed on the bottom left
    canvas.draw_text(f"{highScore}", (150, HEIGHT - 8), 40, '#FFFFFF')

##Sorts the array into the ascending order.
def bubble_sort(array):
    n = len(array)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break
    return array

def set_highscore():
    #Opens the score text file in read mode
    file = open("scores.txt","r")
    data = file.read()
    #Replaces the new line with a comma.
    array = data.replace('\n', ",").split(",")
    file.close()

    #Changes string elements into integer.
    for i in range(0,len(array)):
        array[i]=int(array[i])

    array = bubble_sort(array)
    #The high score is the last element on the sorted array
    hs = array[len(array)-1]
    return hs

# Creating a frame
frame = simplegui.create_frame("Space Invaders Menu (v8)", WIDTH, HEIGHT)
frame.set_canvas_background('Black')
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_handler)
# Start the frame animation
frame.start()
