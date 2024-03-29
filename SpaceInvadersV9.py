import random, math, threading, time
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Preload all images
GAME_OVER_MESSAGE = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/Space_Invaders_GameOver_Screen.png")
DEFENSE_SPRITE = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/DefenseSpriteSheet.png")
GAME_WIN_MESSAGE = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/You_Win_Screen.jpg")
LIVES_COUNTER = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/Lives_Sprite.jpg")
ALIEN_ROW1 = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/Alien_row1.jpg")
ALIEN_ROW2 = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/Alien_row2.jpg")
ALIEN_ROW3 = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/Alien_row3.png")
PLAYER_SPRITE = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/player.png")
RED_ALIEN = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Sprites/RedAlien.png")

# Constants for canvas dimensions, timer, and projectile properties
CW = 800
CH = 600

ALIEN_SPEED = random.randint(10, 50) # affects the speed of the aliens
DEADLINE = CH - 100 - 70

PROJECTILE_RADIUS = 3

# Constants for Alien projectiles
alien_projectiles = []

if ALIEN_SPEED <= 20: #Added varying projectile speed
    ALIEN_PROJECTILE_SPEED = 5
else:
    ALIEN_PROJECTILE_SPEED = 3

# Timer for controlling alien firing
alien_fire_timer = 0
ALIEN_FIRE_INTERVAL = 5 * 30  # 5 seconds (assuming 30 ticks per second)

# Load player sprite image
img = PLAYER_SPRITE
img_dims = (110, 64)
img_centre = (55, 32)

# List to store positions of projectiles
projectile_pos = []

# Velocity of the projectiles
if ALIEN_SPEED >20:
    projectile_speed = 1.2
else:
    projectile_speed = 2.5
end_timer = None

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
spaceship_pos = Vector(CW // 2, CH - 70)
spaceship_vel = Vector()

# Update keydown handler
def keydown(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['left']:
        spaceship_vel.x = -3  # Move left
    elif key == simplegui.KEY_MAP['right']:
        spaceship_vel.x = 3   # Move right
    elif key == simplegui.KEY_MAP['space']:  # Fire projectiles
        if len(projectile_pos) == 0:  # Fire only if no projectile exists
            # Fire projectile from the spaceship's position
            projectile_pos.append(Vector(spaceship_pos.x, spaceship_pos.y - img_dims[1] // 2))

# Update keyup handler
def keyup(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        spaceship_vel.x = 0

# Define the Lives class
class Lives:
    def __init__(self, pos, damaged):
        self.pos = pos
        self.damage = damaged
        self.num_frame = 2
        self.framecount = 0
        self.frame_index = [0, 0]

    def draw(self, canvas):
        lives_img = LIVES_COUNTER
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
        self.frame_index[1] = (self.frame_index[1] + 1) % 2

    def takeDamage(self):
        if self.framecount < self.num_frame:
            self.next_frame()
            self.framecount += 1
            self.damage = True

    def life_gone(self):
        return self.damage

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

        self.frame_index = [0, 0]

        # Define animation parameters
        self.animation_delay = 10  # Adjust as needed
        self.frame_change_counter = 0

    def hit_barrier(self, a):
        return DEADLINE - 10 < a.pos.get_p()[1]

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, "white", "white")
        if self.c < 11:
            self.alien_40_points(canvas)
        elif self.c < 33:
            self.alien_20_points(canvas)
        else:
            self.alien_10_points(canvas)

        canvas.draw_line((0, DEADLINE), (CW, DEADLINE), 3, "#6C0BA9")
        canvas.draw_line((0,CH-45), (CW, CH-45), 5, "#00ff00")

        canvas.draw_text("| Alien's Speed:       |", (200, CH - 10), 20, 'White')
        canvas.draw_text(f"{ALIEN_SPEED}", (330, CH - 10), 20, '#00fc04')

    def alien_10_points(self, canvas):
        alien_10_img = ALIEN_ROW1
        width, height = alien_10_img.get_width(), alien_10_img.get_height()

        frame_width = width / 2
        frame_height = height
        frame_centre_x = frame_width / 2
        frame_centre_y = frame_height / 2

        frame_window = (frame_width * self.frame_index[0] + frame_centre_x,
                        frame_height * self.frame_index[1] + frame_centre_y)
        frame_window_size = (frame_width, frame_height)

        canvas.draw_image(alien_10_img, frame_window, frame_window_size, self.pos.get_p(), (50, 45))

    def alien_20_points(self, canvas):
        alien_20_img = ALIEN_ROW2
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
        alien_40_img = ALIEN_ROW3

        width, height = alien_40_img.get_width(), alien_40_img.get_height()

        frame_width = width / 2
        frame_height = height
        frame_centre_x = frame_width / 2
        frame_centre_y = frame_height / 2

        frame_window = (frame_width * self.frame_index[0] + frame_centre_x,
                        frame_height * self.frame_index[1] + frame_centre_y)
        frame_window_size = (frame_width, frame_height)

        canvas.draw_image(alien_40_img, frame_window, frame_window_size, self.pos.get_p(), (50, 40))

    # def next_frame(self): #Had to remove this as it delays the change perframe
    #     if self.frame_change_counter == self.animation_delay:
    #         self.frame_index[0] = (self.frame_index[0] + 1) % 2
    #         self.frame_change_counter = 0
    #     else:
    #         self.frame_change_counter += 1

    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % 2

    def fire_projectile(self, player_pos):
        alien_pos = Vector(self.pos.x, self.pos.y + self.height / 2)
        return Vector(player_pos.x - alien_pos.x, player_pos.y - alien_pos.y).multiply(0.05)

# Define the Clock class
class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def transition(self, time_duration):
        if self.time % time_duration == 0:
            return True
        
class DefenseSprite:
    def __init__(self, pos):
        self.pos = pos
        self.img = DEFENSE_SPRITE
        # Set the image dimensions to match the actual size of the image
        self.img_dim = (self.img.get_width(), self.img.get_height())
        self.frame_width = self.img_dim[0] / 3  # Divide width by number of frames
        self.frame_height = self.img_dim[1]
        self.hit_counter = 0  # Counter to track hits on the defense

    def draw(self, canvas):
        # Draw the current frame of the defense sprite based on hit counter
        frame_index = min(self.hit_counter // 3, 2)  # Change frame every 3 hits, max index 2
        canvas.draw_image(self.img, (self.frame_width / 2 + frame_index * self.frame_width, self.frame_height / 2),
                          (self.frame_width, self.frame_height), self.pos.get_p(), (100, 80))

    def get_hitbox(self):
        # Adjust the hitbox to create gaps between defense blocks
        hitbox_width = self.frame_width * 0.4  # Reduce hitbox width
        hitbox_height = self.frame_height * 0.5  # Reduce hitbox height
        return (self.pos.x - hitbox_width / 2,  # left
                self.pos.x + hitbox_width / 2,  # right
                self.pos.y - hitbox_height / 2, # top
                self.pos.y + hitbox_height / 2) # bottom
    
class RedAlien:
    def __init__(self, pos):
        self.pos = pos
        self.velocity = Vector(-1.5, 0)  # Red alien moves from right to left
        self.img = RED_ALIEN
        self.img_dim = (self.img.get_width(), self.img.get_height())

    def draw(self, canvas):
        canvas.draw_image(self.img, (self.img_dim[0] // 2, self.img_dim[1] // 2), self.img_dim,
                          self.pos.get_p(), (50, 45))

    def update(self):
        self.pos.add(self.velocity)
        
        # Check if the red alien moves off the left side of the screen
        if self.pos.x + self.img_dim[0] // 2 < 0:
            # Place the red alien off-screen again with a new position
            self.pos.x = CW + 1500  # Place it off-screen again
            self.pos.y = random.randint(0, 100)  # Randomize vertical position

# Define the Integrate class
class Integrate:
    def __init__(self, clock, alien, lives, player):
        self.clock = clock
        self.alien_list = alien
        self.lives = lives
        self.player = player

        self.game_won = False
        self.score = 0
        self.score_written = False
        self.game_over = False
        self.game_over_handlers_removed = False

        self.vel = Vector(0.5, 0)

        self.frame_index = [0, 0]
        self.frame_count = 1

        self.score_colour, self.score_num_colour = 'White', '#00fc04'


    def draw(self, canvas):
        self.clock.tick() #Makes use of the clock in the program.
        global spaceship_pos

        # Update player position based on velocity
        spaceship_pos.add(spaceship_vel)

        # Draw the player sprite
        self.player.draw(canvas)

        # Draw the projectiles
        for pos in projectile_pos:
            canvas.draw_circle(pos.get_p(), PROJECTILE_RADIUS, 2, 'White', 'White')

        # Draw the alien projectiles
        for pos in alien_projectiles:
            canvas.draw_circle(pos.get_p(), PROJECTILE_RADIUS, 2, 'Red', 'Red')

        # Update alien projectile positions
        self.update_alien_projectiles()

        # Draw the red alien only if the game is not over
        if not self.game_over:
            red_alien.draw(canvas)
            red_alien.update()

        # Draw the lives
        for life in player_lives:
            life.draw(canvas)

        # Draw the score
        self.points(canvas)

        # Draw the aliens and handle animation
        for alien in aliens:
            alien.draw(canvas)
            if self.clock.transition(ALIEN_SPEED):
                self.update_alien_movement() #update alien movement to follow the tick
                alien.next_frame()

        # Update the game state
        self.update()

        # Update collisions
        self.handle_collisions()

        # Update alien fire
        self.update_alien_fire(aliens)

        # Draw defense sprites
        for defense in defenses:
            defense.draw(canvas)
        
        # Check for game over condition and display game over screen if necessary
        self.game_over_text(canvas)

    def update_alien_fire(self, aliens):
        global alien_fire_timer, alien_projectiles

        # Increment the timer
        alien_fire_timer += 1
        
        # Check if it's time for an alien to fire
        if alien_fire_timer >= ALIEN_FIRE_INTERVAL:
            # Select aliens from the row closest to the top that are still present on the screen
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
        alien_projectiles_to_remove = []  # Store projectiles to remove to avoid modifying list while iterating
        for pos in alien_projectiles:
            pos.add(Vector(0, ALIEN_PROJECTILE_SPEED))
            
            # Check collision with defense sprites
            for defense in defenses:
                defense_hitbox = defense.get_hitbox()
                
                # Check if the player projectile intersects with the defense hitbox
                if (pos.x >= defense_hitbox[0] and pos.x <= defense_hitbox[1] and
                    pos.y >= defense_hitbox[2] and pos.y <= defense_hitbox[3]):
                    # Remove the player projectile
                    alien_projectiles_to_remove.append(pos)
                    
                    # Increment the hit counter of the defense
                    defense.hit_counter += 1
                    
                    # Check if the defense has been hit 9 times
                    if defense.hit_counter == 9:
                        # Remove the defense from the game
                        defenses.remove(defense)
                    
                    # Break out of the loop since the projectile can only hit one defense at a time
                    break

        # Remove collided projectiles from the list
        alien_projectiles = [pos for pos in alien_projectiles if pos not in alien_projectiles_to_remove]
    
    def handle_collisions(self):
        global alien_projectiles, projectile_pos, red_alien, player_lives_inlist
        projectiles_to_remove = []
        player_projectiles_to_remove = []
        
        # Collision detection function for alien projectiles and player sprite
        for projectile in alien_projectiles:
            distance = math.sqrt((projectile.x - player.pos.x) ** 2 + (projectile.y - player.pos.y) ** 2)
            if distance <= PROJECTILE_RADIUS + img_dims[1] // 2:
                projectiles_to_remove.append(projectile)
                if player_lives: # system makes lives change colour instead of just remove them
                    player_lives_inlist -= 1
                    if player_lives_inlist == 2:
                        player_lives[2].takeDamage()
                    elif player_lives_inlist == 1:
                        player_lives[1].takeDamage()
                    elif player_lives_inlist == 0:
                        player_lives[0].takeDamage()
                    #player_lives.pop()
                if not player_lives:
                    i.game_over = True

        # Remove collided projectiles from the list
        for projectile in projectiles_to_remove:
            alien_projectiles.remove(projectile)
        
        # Collision detection function for player projectiles and red alien
        for pos in projectile_pos[:]:
            distance = math.sqrt((pos.x - red_alien.pos.x) ** 2 + (pos.y - red_alien.pos.y) ** 2)
            if distance <= PROJECTILE_RADIUS + 25:
                player_projectiles_to_remove.append(pos)
                red_alien = RedAlien(Vector(-100, random.randint(0, 100)))
                i.score += 200

        projectile_pos = [proj for proj in projectile_pos if proj not in player_projectiles_to_remove]
        
        # Collision detection function for player projectiles and aliens
        for pos in projectile_pos[:]:
            pos.add(Vector(0, -projectile_speed))
            if pos.y < 0:
                player_projectiles_to_remove.append(pos)
            aliens_copy = list(aliens)
            for alien in aliens_copy:
                hitbox = (alien.pos.x - alien.hitbox_width / 2, alien.pos.x + alien.hitbox_width / 2,
                          alien.pos.y - alien.hitbox_height / 2, alien.pos.y + alien.hitbox_height / 2)
                if (pos.x >= hitbox[0] and pos.x <= hitbox[1] and
                    pos.y >= hitbox[2] and pos.y <= hitbox[3]):
                    projectile_pos.remove(pos)
                    aliens.remove(alien)
                    # Update the score
                    # Fixed the score system on .v7 so it allocated the appropriate amount for an alien in it's respected row
                    if alien.c < 11:
                        i.score += 40
                    elif alien.c < 33:
                        i.score += 20
                    else:
                        i.score += 10

                    # i.score += alien.c #old method on adding score system

                    # Break out of the loop since the projectile can only hit one alien at a time
                    break
            for defense in defenses:
                defense_hitbox = defense.get_hitbox()
                if (pos.x >= defense_hitbox[0] and pos.x <= defense_hitbox[1] and
                    pos.y >= defense_hitbox[2] and pos.y <= defense_hitbox[3]):
                    player_projectiles_to_remove.append(pos)
                    defense.hit_counter += 1
                    if defense.hit_counter == 9:
                        defenses.remove(defense)
                    break

        projectile_pos = [proj for proj in projectile_pos if proj not in player_projectiles_to_remove]

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

    def update_alien_movement(self):  # change name
        if not self.game_over:  # Only update game if it's not over
            for a in range(len(self.alien_list)):
                self.alien_list[a].pos.add(self.vel)
                if self.alien_list[a].pos.get_p()[0] <= 15:
                    self.drop(self.vel.x)
                    self.vel = Vector(0.5, 0)
                elif self.alien_list[a].pos.get_p()[0] > CW - 15:
                    self.drop(self.vel.x)
                    self.vel = Vector(-0.5, 0)
                if self.alien_list[a].hit_barrier(self.alien_list[a]) or self.calc_lives() == 0:
                    self.vel = Vector(0, 0)
                    self.game_over = True

    def update(self):  # Had to seperate updateing the whole game with updating the alien movement above. Therefore the aliens will now move then pause and resume
        global spaceship_pos
        if not self.game_over:  # Only update game if it's not over

            # Update player position based on velocity
            spaceship_pos.add(spaceship_vel)
            # Update player position in the player sprite
            self.player.pos = spaceship_pos.copy()

            # Ensure the player spaceship stays within the canvas boundaries
            if spaceship_pos.x < img_dims[0] // 2:  # Left edge
                spaceship_pos.x = img_dims[0] // 2
            elif spaceship_pos.x > CW - img_dims[0] // 2:  # Right edge
                spaceship_pos.x = CW - img_dims[0] // 2

            # Check collision with red alien
            self.handle_collisions()

        # Check if all aliens are removed
            if not self.alien_list:
                # Check if the player has remaining lives
                if self.calc_lives() > 0:
                    self.game_won = True
                    self.game_over = True
                else:
                    self.game_won = False
                    self.game_over = True

        # Check for game over condition and set game_over attribute
        if self.calc_lives() == 0 or any(alien.hit_barrier(alien) for alien in self.alien_list):
            self.game_over = True
            self.game_won = False
            self.game_over_handlers_removed = True

    def game_over_text(self, canvas):
        global end_timer
        if self.game_over:
            # Write score to file only if it hasn't been written before
            if not self.score_written:
                self.write_to_file()
                self.score_written = True  # Update the flag to indicate that the score has been written

            if self.game_won:
                # Display "GAME OVER, YOU WON" message
                win_img = GAME_WIN_MESSAGE
                self.width_gom, self.height_gom = win_img.get_width(), win_img.get_height()
                # fixes current lives at the end of the game from always being 3 because we do self.lives.clear() below
                if self.clock.transition(ALIEN_SPEED):
                    alien_projectiles.clear()  # Remove projectives from canvas
                    self.alien_list.clear()  # Remove aliens from canvas
                    # self.lives.clear() # 0 lives + remove from canvas
                    defenses.clear()  # removed defensed from canvas
                    self.score_colour, self.score_num_colour = '#000000', '#000000'
                canvas.draw_image(win_img, (self.width_gom / 2, self.height_gom / 2),
                                  (self.width_gom, self.height_gom), (CW / 2, CH / 2),
                                  (CW * 3 / 4, CH * 1 / 2))
                canvas.draw_text("Score:", (0, 30), 30, 'White')
                canvas.draw_text(f"{self.score}", (80, 31), 30, '#00fc04')
                canvas.draw_text("Lives:", (CW - 100, 30), 30, 'White')
                canvas.draw_text(f"{self.calc_lives()}", (CW - 20, 31), 30, '#00fc04')
                canvas.draw_text("ALIEN'S SPEED:", (CW // 2 - 120, 30), 25, 'White')
                canvas.draw_text(f"{ALIEN_SPEED}", (CW // 2 + 65, 31), 25, '#00fc04')

                end_timer = threading.Timer(10, end_game) #Final screen display time
                end_timer.start()
            else:
                # Display "GAME OVER" message
                go_img = GAME_OVER_MESSAGE
                self.width_gom, self.height_gom = go_img.get_width(), go_img.get_height()
                if self.clock.transition(ALIEN_SPEED):
                    alien_projectiles.clear()  # Remove projectives from canvas
                    self.alien_list.clear()  # Remove aliens from canvas
                    self.lives.clear()  # 0 lives + remove from canvas
                    defenses.clear()  # removed defensed from canvas
                    self.score_colour, self.score_num_colour = '#000000', '#000000'
                canvas.draw_image(go_img, (self.width_gom / 2, self.height_gom / 2),
                                  (self.width_gom, self.height_gom), (CW / 2, CH / 2),
                                  (CW * 3 / 4, CH * 1 / 2))
                canvas.draw_text("Score:", (0, 30), 30, 'White')
                canvas.draw_text(str(self.score), (80, 31), 30, '#00fc04')
                canvas.draw_text("Lives:", (CW - 100, 30), 30, 'White')
                canvas.draw_text("0", (CW - 20, 31), 30, '#ff0000')
                canvas.draw_text("ALIEN'S SPEED:", (CW//2 - 120, 30), 25, 'White')
                canvas.draw_text(f"{ALIEN_SPEED}", (CW//2 + 65, 31), 25, '#00fc04')
                end_timer = threading.Timer(7, end_game) #Final screen display time
                end_timer.start()



    def write_to_file(self):
        # Write player name and score to a text file
        with open("scores.txt", "a") as file:
            file.write(f"\n{self.score}")

def end_game():
    global end_timer
    # Check if the timer is active before stopping it
    if end_timer and end_timer.is_alive():
        end_timer.cancel()
    frame.stop()

# List to store instances of aliens
aliens = []
j_d = 15
count = 0
for i in range(5):
    for j in range(11):
        aliens.append(Alien(Vector(20 + (j * 50), j_d), count))
        count += 1
    j_d += 50

# List to store instances of lives
player_lives = []
player_lives_inlist = 3
for i in range(3):
    player_lives.append(Lives((CW - 50 - (i * 100), CH - 20), False))

# List to store instances of defense sprites
defenses = []

# Initialize defense sprites and add them to the list
defenses.append(DefenseSprite(Vector(150, 470)))
defenses.append(DefenseSprite(Vector(CW//2, 470)))
defenses.append(DefenseSprite(Vector(CW-150, 470)))

# Create a frame
frame = simplegui.create_frame("Space Invaders v8", CW, CH)
clock = Clock()

# Initialize the player sprite
player = PlayerSprite(spaceship_pos)

# Instantiate the red alien
red_alien = RedAlien(Vector(-100, random.randint(0, 100)))

# Integrate everything into the game
i = Integrate(clock, aliens, player_lives, player)

# Set event handlers
if not i.game_over_handlers_removed:
    frame.set_draw_handler(i.draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)

# Start the frame
frame.start()
