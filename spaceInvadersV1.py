import random
import math
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# URLs for game assets
GAME_OVER_MESSAGE = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Space_Invaders_GameOver_Screen.png"
LIVES_COUNTER = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Lives_Sprite.jpg"
ALIEN_ROW1 = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Alien_row1.jpg"
ALIEN_ROW2 = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Alien_row2.jpg"
ALIEN_ROW3 = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Alien_row3.png"
PLAYER_SPRITE = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/player.png"

# Constants for canvas dimensions, timer, and projectile properties
CW = 800
CH = 600
TIMER = 30 * 2
GAME_OVER_BARRIER = CH - 100 - 50
PROJECTILE_RADIUS = 3

# Load player sprite image
img = simplegui.load_image(PLAYER_SPRITE)
img_dims = (110, 64)
img_centre = (55, 32)

# List to store positions of projectiles
projectile_pos = []

# Velocity of the projectiles
projectile_speed = 2

# Define the Vector class for handling positions and velocities
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    def get_p(self):
        return (self.x, self.y)

    def copy(self):
        return Vector(self.x, self.y)

    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

# Initial position and velocity of the spaceship (as vectors)
spaceship_pos = Vector(CW // 2, CH - 150)
spaceship_vel = Vector()

# Define the PlayerSprite class
class PlayerSprite:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector()  # Add velocity attribute
        self.img_dim = (55,32)

    def draw(self, canvas):
        # Draw the player sprite on the canvas at the position self.pos
        canvas.draw_image(img, img_centre, img_dims, self.pos.get_p(), self.img_dim)

    def update(self):
        # Update the position based on the velocity
        self.pos.add(self.vel)

# Function to update projectile positions and handle collisions
def update_projectiles():
    global projectile_pos, aliens, i
    
    # Iterate over projectiles
    for pos in projectile_pos:
        pos.add(Vector(0, -projectile_speed))
        
        # Create a copy of the aliens list to avoid modifying it while iterating
        aliens_copy = list(aliens)
        
        # Iterate over aliens
        for alien in aliens_copy:
            # Check for collision between projectile and alien
            if (pos.x > alien.pos.x - alien.radius and
                pos.x < alien.pos.x + alien.radius and
                pos.y > alien.pos.y - alien.radius and
                pos.y < alien.pos.y + alien.radius):
                
                # Remove the collided projectile and alien
                projectile_pos.remove(pos)
                aliens.remove(alien)
                
                # Update the score
                i.score += alien.c
                
                # Break out of the loop since the projectile can only hit one alien at a time
                break
    
    # Remove projectiles that have left the frame
    projectile_pos = [pos for pos in projectile_pos if pos.y > 0]

# Update keydown handler
def keydown(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['left']:
        spaceship_vel.x = -5  # Move left
    elif key == simplegui.KEY_MAP['right']:
        spaceship_vel.x = 5   # Move right
    elif key == simplegui.KEY_MAP['space']:  # Fire projectiles
        if len(projectile_pos) == 0:  # Fire only if no projectile exists
            # Fire projectile from the spaceship's position
            projectile_pos.append(Vector(spaceship_pos.x, spaceship_pos.y - img_dims[1] // 2))

# Update keyup handler
def keyup(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        spaceship_vel.x = 0


# Define the Alien class
class Alien:
    def __init__(self, pos, count):
        self.pos = pos
        self.radius = 5
        self.c = count

        self.num_frame = 2
        self.framecount = 0
        self.frame_index = [0, 0]

    def hit_barrier(self, a):
        return GAME_OVER_BARRIER-15 <= a.pos.get_p()[1]

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, "white", "white")
        if self.c < 11:
            self.alien_40_points(canvas)
        elif self.c < 33:
            self.alien_20_points(canvas)
        else:
            self.alien_10_points(canvas)

        canvas.draw_line((0, GAME_OVER_BARRIER), (CW, GAME_OVER_BARRIER), 2, "#42f5c8")
        canvas.draw_line((0,CH-45), (CW, CH-45), 5, "#00ff00")

    def alien_10_points(self, canvas):
        alien_10_img = simplegui.load_image(ALIEN_ROW1)
        width, height = alien_10_img.get_width(), alien_10_img.get_height()

        frame_width = width / 2
        frame_height = height
        frame_centre_x = frame_width
        frame_centre_x = frame_width / 2
        frame_centre_y = frame_height / 2

        frame_window = (frame_width * self.frame_index[0] + frame_centre_x,
                        frame_height * self.frame_index[1] + frame_centre_y)
        frame_window_size = (frame_width, frame_height)

        canvas.draw_image(alien_10_img, frame_window, frame_window_size, self.pos.get_p(), (50, 45))

    def alien_20_points(self, canvas):
        alien_20_img = simplegui.load_image(ALIEN_ROW2)
        width, height = alien_20_img.get_width(), alien_20_img.get_height()

        frame_width = width / 2
        frame_height = height
        frame_centre_x = frame_width / 2
        frame_centre_y = frame_height / 2

        frame_window = (frame_width * self.frame_index[0] + frame_centre_x,
                        frame_height * self.frame_index[1] + frame_centre_y)
        frame_window_size = (frame_width, frame_height)

        canvas.draw_image(alien_20_img, frame_window, frame_window_size, self.pos.get_p(), (50, 45))

    def alien_40_points(self, canvas):
        alien_40_img = simplegui.load_image(ALIEN_ROW3)

        width, height = alien_40_img.get_width(), alien_40_img.get_height()

        frame_width = width / 2
        frame_height = height
        frame_centre_x = frame_width / 2
        frame_centre_y = frame_height / 2

        frame_window = (frame_width * self.frame_index[0] + frame_centre_x,
                        frame_height * self.frame_index[1] + frame_centre_y)
        frame_window_size = (frame_width, frame_height)

        canvas.draw_image(alien_40_img, frame_window, frame_window_size, self.pos.get_p(), (50, 40))

    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % 2

# Define the Lives class
class Lives:
    def __init__(self, pos, damaged):
        self.pos = pos
        self.damage = damaged
        self.num_frame = 2
        self.framecount = 0
        self.frame_index = [0, 0]

    def draw(self, canvas):
        lives_img = simplegui.load_image(LIVES_COUNTER)
        self.width_ls, self.height_ls = lives_img.get_width(), lives_img.get_height()
        self.dimensionLivesSprite()

        frame_window = (self.width_ls * self.frame_index[0] + self.frame_centre_x,
                        self.frame_height * self.frame_index[1] + self.frame_centre_y)
        frame_window_size = (self.frame_width, self.frame_height)

        canvas.draw_image(lives_img, frame_window, frame_window_size, self.pos, (100, 50))
        canvas.draw_text(f"Lives: ",(CW - 405, CH - 8), 40, '#00ff00')

    def dimensionLivesSprite(self):
        self.frame_width = self.width_ls
        self.frame_height = self.height_ls / 2
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % 2
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % 2

    def takeDamage(self):
        if self.framecount < self.num_frame:
            self.next_frame()
            self.framecount += 1
            self.damage = True

    def life_gone(self):
        return self.damage

# Define the Clock class
class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def transition(self, time_duration):
        if self.time % time_duration == 0:
            return True

# Define the Integrate class
class Integrate:
    def __init__(self, clock, alien, lives, player):
        self.clock = clock
        self.alien_list = alien
        self.lives = lives
        self.player = player
        self.score = 0

        self.vel = Vector(0.5, 0)
        self.game_over = False
        self.frame_index = [0, 0]
        self.frame_count = 1
        self.score_colour, self.score_num_colour = 'White', '#00fc04'

    def draw(self, canvas):
        self.clock.tick()
        self.game_over_text(canvas)

        # Draw the player sprite
        self.player.draw(canvas)

        # Draw the projectiles
        for pos in projectile_pos:
            canvas.draw_circle(pos.get_p(), PROJECTILE_RADIUS, 1, 'White', 'White')

        # Update projectile positions
        update_projectiles()

        # Draw the lives
        [l.draw(canvas) for l in self.lives]

        # Handle alien drawing
        if len(self.lives) > 0:
            self.lives[0].takeDamage()
            self.lives[1].takeDamage()

        # Draw the score
        self.points(canvas)

        for a in range(len(self.alien_list)):
            self.alien_list[a].draw(canvas)
            if self.clock.transition(TIMER):
                self.update()
                self.alien_list[a].next_frame()
        
        self.update()

    def calc_lives(self):
        local_counter = 3
        if len(self.lives) > 0:
            for i in range(3):
                if self.lives[i].life_gone() == True:
                    local_counter -= 1
        return local_counter

    def points(self, canvas):
        canvas.draw_text(f"Score:", (0, CH - 10), 40, self.score_colour)
        canvas.draw_text(f"{self.score}", (105, CH - 8), 40, self.score_num_colour)

    def drop(self, x):
        for a in range(len(self.alien_list)):
            self.alien_list[a].pos.add(Vector(x, 20))

    def update(self):
        global spaceship_pos

        for a in range(len(self.alien_list)):
            self.alien_list[a].pos.add(self.vel)
            if self.alien_list[a].pos.get_p()[0] <= 15:
                self.drop(self.vel.x)
                self.vel = Vector(0.5, 0)
            elif self.alien_list[a].pos.get_p()[0] > CW-15:
                self.drop(self.vel.x)
                self.vel = Vector(-0.5, 0)
            if self.alien_list[a].hit_barrier(self.alien_list[a]) or self.calc_lives() == 0:
                self.vel = Vector(0, 0)
                self.game_over = True

        # Update player position based on velocity
        spaceship_pos.add(spaceship_vel)
        # Update player position in the player sprite
        self.player.pos = spaceship_pos.copy()

    def game_over_text(self, canvas):
        if self.game_over == True:
            go_img = simplegui.load_image(GAME_OVER_MESSAGE)
            self.width_gom, self.height_gom = go_img.get_width(), go_img.get_height()
            if self.clock.transition(TIMER):
                self.alien_list.clear()
                self.lives.clear()
                self.score_colour, self.score_num_colour = '#000000', '#000000'
            canvas.draw_image(go_img, (self.width_gom / 2, self.height_gom / 2),
                              (self.width_gom, self.height_gom), (CW / 2, CH / 2),
                              (CW * 3 / 4, CH * 1 / 2))
            canvas.draw_text(f"Score:", (0, 30), 30, 'White')
            canvas.draw_text(f"{self.score}", (80, 31), 30, '#00fc04')
            canvas.draw_text(f"Lives:", (CW-100, 30), 30, 'White')
            canvas.draw_text(f"0", (CW - 20, 31), 30, '#ff0000')


# List to store instances of aliens
aliens = []
j_d = 15
point = 40
count = 0
for i in range(5):
    for j in range(11):
        aliens.append(Alien(Vector(20 + (j * 50), j_d), count))
        count += 1
    j_d += 50

# List to store instances of lives
player_lives = []
for i in range(3):
    player_lives.append(Lives((CW - 50 - (i * 100), CH - 20), False))

# Create a frame
frame = simplegui.create_frame("Aliens", CW, CH)
clock = Clock()

# Initialize the player sprite
player = PlayerSprite(spaceship_pos)

# Integrate everything into the game
i = Integrate(clock, aliens, player_lives, player)

# Set event handlers
frame.set_draw_handler(i.draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# Start the frame
frame.start()
