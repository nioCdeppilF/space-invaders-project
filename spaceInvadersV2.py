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

# Constants for Alien projectiles
alien_projectiles = []
ALIEN_PROJECTILE_SPEED = 3

# Timer for controlling alien firing
alien_fire_timer = 0
ALIEN_FIRE_INTERVAL = 5 * 30  # 5 seconds (assuming 30 ticks per second)

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

# Update function for projectile collisions with aliens
def update_projectiles():
    global projectile_pos, aliens, i
    
    # Iterate over projectiles
    for pos in projectile_pos:
        pos.add(Vector(0, -projectile_speed))
        
        # Create a copy of the aliens list to avoid modifying it while iterating
        aliens_copy = list(aliens)
        
        # Iterate over aliens
        for alien in aliens_copy:
            # Calculate the actual hitbox for the alien sprite
            hitbox = (alien.pos.x - alien.hitbox_width / 2,  # left
                      alien.pos.x + alien.hitbox_width / 2,  # right
                      alien.pos.y - alien.hitbox_height / 2, # top
                      alien.pos.y + alien.hitbox_height / 2) # bottom
            
            # Check if the projectile intersects with the hitbox
            if (pos.x >= hitbox[0] and pos.x <= hitbox[1] and
                pos.y >= hitbox[2] and pos.y <= hitbox[3]):
                
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

# Collision detection function for alien projectiles and player sprite
def check_collision_with_player():
    global alien_projectiles, player_lives
    
    # Iterate over alien projectiles
    projectiles_to_remove = []  # Store projectiles to remove to avoid modifying list while iterating
    for projectile in alien_projectiles:
        # Calculate the distance between projectile and player sprite center
        distance = math.sqrt((projectile.x - player.pos.x) ** 2 + (projectile.y - player.pos.y) ** 2)
        
        # If the distance is less than the sum of radii, it's a collision
        if distance <= PROJECTILE_RADIUS + img_dims[1] // 2:
            # Remove the projectile
            projectiles_to_remove.append(projectile)
            
            # Reduce player lives count
            if player_lives:
                player_lives.pop()
                
            # Check if player has run out of lives
            if not player_lives:
                i.game_over = True

    # Remove collided projectiles from the list
    for projectile in projectiles_to_remove:
        alien_projectiles.remove(projectile)

# Update function for collisions
def update_collisions():
    check_collision_with_player()

# Define the Alien class
class Alien:
    def __init__(self, pos, count):
        self.pos = pos
        self.radius = 5
        self.c = count

        # Alien sprite dimensions
        self.width = 50
        self.height = 45
        
        # Hitbox dimensions
        self.hitbox_width = self.width
        self.hitbox_height = self.height

        self.num_frame = 2
        self.framecount = 0
        self.frame_index = [0, 0]

        # Define animation parameters
        self.animation_delay = 10  # Adjust as needed
        self.frame_change_counter = 0

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
        if self.frame_change_counter == self.animation_delay:
            self.frame_index[0] = (self.frame_index[0] + 1) % 2
            self.frame_change_counter = 0
        else:
            self.frame_change_counter += 1

    def fire_projectile(self, player_pos):
        alien_pos = Vector(self.pos.x, self.pos.y + self.height / 2)
        return Vector(player_pos.x - alien_pos.x, player_pos.y - alien_pos.y).multiply(0.05)

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
        self.game_won = False
        self.score = 0

        self.vel = Vector(0.5, 0)
        self.game_over = False
        self.frame_index = [0, 0]
        self.frame_count = 1
        self.score_colour, self.score_num_colour = 'White', '#00fc04'

    def draw(self, canvas):
        global spaceship_pos

        # Update player position based on velocity
        spaceship_pos.add(spaceship_vel)

        # Draw the player sprite
        player.draw(canvas)

        # Draw the projectiles
        for pos in projectile_pos:
            canvas.draw_circle(pos.get_p(), PROJECTILE_RADIUS, 1, 'White', 'White')

        # Draw the alien projectiles
        for pos in alien_projectiles:
            canvas.draw_circle(pos.get_p(), PROJECTILE_RADIUS, 1, 'Red', 'Red')

        # Update projectile positions
        update_projectiles()

        # Update alien projectile positions
        self.update_alien_projectiles()

        # Draw the lives
        for life in player_lives:
            life.draw(canvas)

        # Draw the score
        i.points(canvas)

        # Draw the aliens and handle animation
        for alien in aliens:
            alien.draw(canvas)
            if clock.transition(TIMER):
                alien.next_frame()

        # Update the game state
        self.update()

        # Update collisions
        update_collisions()

        # Update alien actions
        self.update_aliens()

        # Update alien fire
        self.update_alien_fire(aliens)
        
        # Check for game over condition and display game over screen if necessary
        i.game_over_text(canvas)
    
    def update_aliens(self):
        global alien_fire_timer, aliens, alien_projectiles

        # Update the alien fire timer
        alien_fire_timer += 1

        # Check if it's time for an alien to fire
        if alien_fire_timer >= ALIEN_FIRE_INTERVAL:
            # Select aliens from the back row for firing
            back_row_aliens = [alien for alien in self.alien_list if alien.pos.y == 185]
            if back_row_aliens:
                alien_to_fire = random.choice(back_row_aliens)
                # Fire projectile from the selected alien
                alien_projectiles.append(Vector(alien_to_fire.pos.x, alien_to_fire.pos.y + 20))
            # Reset the timer
            alien_fire_timer = 0
    
    def update_alien_fire(self, aliens):
        global alien_fire_timer, alien_projectiles

        # Increment the timer
        alien_fire_timer += 1
        
        # Check if it's time for an alien to fire
        if alien_fire_timer >= ALIEN_FIRE_INTERVAL:
            # Select aliens from the row closest to the bottom that are still present on the screen
            available_rows = set(alien.pos.y for alien in aliens)
            available_rows = sorted(available_rows)
            for row in available_rows:
                row_aliens = [alien for alien in aliens if alien.pos.y == row]
                if row_aliens:
                    # Select a random alien from this row to fire
                    alien_to_fire = random.choice(row_aliens)
                    # Fire projectile from the selected alien
                    alien_projectiles.append(Vector(alien_to_fire.pos.x, alien_to_fire.pos.y + 20))
                    # Reset the timer
                    alien_fire_timer = 0
                    break

    def update_alien_projectiles(self):
        global alien_projectiles

        # Iterate over alien projectiles
        for pos in alien_projectiles:
            pos.add(Vector(0, ALIEN_PROJECTILE_SPEED))

        # Remove projectiles that have left the frame
        alien_projectiles = [pos for pos in alien_projectiles if pos.y < CH]

    def calc_lives(self):
        local_counter = 3
        for life in self.lives:
            if life.life_gone():
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

        # Ensure the player spaceship stays within the canvas boundaries
        if spaceship_pos.x < img_dims[0] // 2:  # Left edge
            spaceship_pos.x = img_dims[0] // 2
        elif spaceship_pos.x > CW - img_dims[0] // 2:  # Right edge
            spaceship_pos.x = CW - img_dims[0] // 2

        # Check for game over condition and set game_over attribute
        if self.calc_lives() == 0:
            self.game_over = True
            self.game_won = False

        # Check if all aliens are removed
        if not self.alien_list:
            self.game_won = True
            self.game_over = True

    def game_over_text(self, canvas):
        if self.game_over:
            if self.game_won:
                # Display "GAME OVER, YOU WON" message
                canvas.draw_text("GAME OVER, YOU WON", (CW / 2 - 200, CH / 2), 40, 'White')
            else:
                # Display "GAME OVER" message
                go_img = simplegui.load_image(GAME_OVER_MESSAGE)
                self.width_gom, self.height_gom = go_img.get_width(), go_img.get_height()
                if self.clock.transition(TIMER):
                    alien_projectiles.clear()
                    self.alien_list.clear()
                    self.lives.clear()
                    self.score_colour, self.score_num_colour = '#000000', '#000000'
                canvas.draw_image(go_img, (self.width_gom / 2, self.height_gom / 2),
                                (self.width_gom, self.height_gom), (CW / 2, CH / 2),
                                (CW * 3 / 4, CH * 1 / 2))
                canvas.draw_text("Score:", (0, 30), 30, 'White')
                canvas.draw_text(str(self.score), (80, 31), 30, '#00fc04')
                canvas.draw_text("Lives:", (CW - 100, 30), 30, 'White')
                canvas.draw_text(str(self.calc_lives()), (CW - 20, 31), 30, '#ff0000')

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
