import simplegui
import random
import math

# Importing the Vector class
from user305_o32FtUyCKk_0 import Vector

# Initialize global variables
WIDTH = 600
HEIGHT = 900
SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 20
PROJECTILE_RADIUS = 3
LIVES = 3  # Number of lives
SCORE = 0  # Initial score

# Initial position and velocity of the spaceship
spaceship_pos = Vector(WIDTH // 2, HEIGHT - 50)
spaceship_vel = Vector()

# List to store positions of projectiles
projectile_pos = []

# List to store positions of aliens
aliens = []

# Velocity of the projectiles
projectile_speed = 2

# Velocity of the aliens
ALIEN_SPEED = 0.25
alien_vel = Vector(ALIEN_SPEED, 0)  # Adjust the speed as needed

# Timer interval for aliens shooting
ALIEN_SHOOT_INTERVAL = 3000  # In milliseconds

# Define lives position and text position
lives_pos = [Vector(WIDTH - 50 - (i * 30), 20) for i in range(3)]  # Adjusted positions for lives display
text_pos = (WIDTH - 175, 25)  # Position for the "Lives:" text

# Variable to track if the game is over
game_over = False

# Create aliens
def create_aliens():
    global aliens
    for i in range(5):
        for j in range(11):
            alien_x = 50 + j * 50
            alien_y = 50 + i * 50
            aliens.append(Vector(alien_x, alien_y))

# Function to draw lives display
def draw_lives(canvas):
    # Draw "Lives:" text
    canvas.draw_text("Lives:", text_pos, 20, 'White')
    # Draw lives display
    for pos in lives_pos:
        canvas.draw_circle(pos.get_p(), 10, 1, 'Red', 'Red')

# Draw handler to draw the spaceship, projectiles, and aliens
def draw(canvas):
    global spaceship_pos, projectile_pos, aliens, SCORE, game_over

    # Check if the game is over
    if game_over:
        draw_game_over(canvas)
        return

    # Update spaceship position
    update_spaceship()

    # Update projectile positions
    update_projectiles()

    # Update alien positions
    update_aliens()

    # Draw spaceship
    canvas.draw_polygon([(spaceship_pos.x - SPACESHIP_WIDTH // 2, spaceship_pos.y - SPACESHIP_HEIGHT // 2),
                         (spaceship_pos.x + SPACESHIP_WIDTH // 2, spaceship_pos.y - SPACESHIP_HEIGHT // 2),
                         (spaceship_pos.x + SPACESHIP_WIDTH // 2, spaceship_pos.y + SPACESHIP_HEIGHT // 2),
                         (spaceship_pos.x - SPACESHIP_WIDTH // 2, spaceship_pos.y + SPACESHIP_HEIGHT // 2)], 1, 'White', 'White')

    # Draw projectiles
    for pos, is_player_projectile in projectile_pos:
        if is_player_projectile:
            canvas.draw_circle(pos.get_p(), PROJECTILE_RADIUS, 1, 'White', 'White')
        else:
            canvas.draw_circle(pos.get_p(), PROJECTILE_RADIUS, 1, 'Yellow', 'Yellow')

    # Draw aliens
    for pos in aliens:
        canvas.draw_circle(pos.get_p(), 10, 1, 'Red', 'Red')

    # Draw spaceship lives
    draw_lives(canvas)

    # Draw score
    draw_score(canvas)

    # Check for collisions
    check_collisions()

# Function to update the positions of projectiles and check if they have left the frame
def update_projectiles():
    global projectile_pos
    projectiles_to_remove = []  # Create a list to store indices of projectiles to remove
    for i, (pos, is_player_projectile) in enumerate(projectile_pos):
        # Move the projectiles downwards (add to y-coordinate)
        if is_player_projectile:
            pos.y -= projectile_speed
        else:
            pos.y += projectile_speed  # Move alien projectiles downwards
        # Check if projectile is out of bounds
        if pos.y < 0 or pos.y > HEIGHT:
            projectiles_to_remove.append(i)
    # Remove projectiles that have left the frame
    for index in sorted(projectiles_to_remove, reverse=True):
        del projectile_pos[index]

# Function to update the positions of aliens and check if they have hit the walls
def update_aliens():
    global aliens, alien_vel
    for alien in aliens:
        alien.x += alien_vel.x
        if alien.x >= WIDTH - 10 or alien.x <= 10:
            alien_vel.x *= -1
            for a in aliens:
                a.y += 50

# Function to reset aliens to the top of the page
def reset_aliens():
    global aliens
    aliens = [Vector(50 + j * 50, 50) for j in range(11)]

# Function to handle alien shooting
def alien_shoot_handler():
    # Select a random alien from the back row
    if aliens:
        back_row_aliens = [alien for alien in aliens if alien.y == max(alien.y for alien in aliens)]
        selected_alien = random.choice(back_row_aliens)
        # Fire projectile towards the player's spaceship
        projectile_pos.append([selected_alien.copy(), False])  # Third element indicates it's an alien projectile

# Start the alien shooting timer
alien_shoot_timer = simplegui.create_timer(ALIEN_SHOOT_INTERVAL, alien_shoot_handler)
alien_shoot_timer.start()

# Function to update the position of the spaceship
def update_spaceship():
    global spaceship_pos  # Declare spaceship_pos as global
    spaceship_pos.x += spaceship_vel.x

# Function to check for collisions between projectiles and aliens
def check_collisions():
    global LIVES, projectile_pos, aliens, game_over, spaceship_pos, SCORE
    for i, (projectile, is_player_projectile) in enumerate(projectile_pos):
        if is_player_projectile:  # Check collisions only for player projectiles
            for j, alien in enumerate(aliens):
                if abs(alien.x - projectile.x) < 10 and abs(alien.y - projectile.y) < 10:
                    del projectile_pos[i]
                    del aliens[j]
                    SCORE += 10  # Increment the score
                    break
    for i, (projectile, is_player_projectile) in enumerate(projectile_pos):
        if not is_player_projectile:  # Only check collisions with alien projectiles
            if abs(projectile.x - spaceship_pos.x) < SPACESHIP_WIDTH // 2 and abs(projectile.y - spaceship_pos.y) < SPACESHIP_HEIGHT // 2:
                LIVES -= 1
                del projectile_pos[i]
                if LIVES == 0:
                    end_game()  # End the game if the player runs out of lives
                else:
                    spaceship_pos = Vector(WIDTH // 2, HEIGHT - 50)

# Function to draw the current score
def draw_score(canvas):
    canvas.draw_text("Score: " + str(SCORE), (50, 50), 24, 'White')


def keydown(key):
    global spaceship_vel, projectile_pos
    if key == simplegui.KEY_MAP['a']:
        spaceship_vel.x = -5  # Move left
    elif key == simplegui.KEY_MAP['d']:
        spaceship_vel.x = 5   # Move right
    elif key == simplegui.KEY_MAP['space'] and len(projectile_pos) == 0:  # Fire only if no projectile exists
        # Fire projectile from the spaceship's position
        projectile_pos.append([spaceship_pos.copy(), True])  # Third element indicates it's a player projectile

def keyup(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['a'] or key == simplegui.KEY_MAP['d']:
        spaceship_vel.x = 0

def end_game():
    global game_over
    game_over = True
    global spaceship_pos

# Function to draw "GAME OVER" message
def draw_game_over(canvas):
    canvas.draw_text("GAME OVER", (WIDTH // 2 - 100, HEIGHT // 2), 36, 'Red')

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame('Space Invaders', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# Create aliens
create_aliens()

frame.start()
