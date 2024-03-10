import simplegui

# Initialize global variables
WIDTH = 600
HEIGHT = 400
SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 20
PROJECTILE_RADIUS = 3

# Initial position and velocity of the spaceship
spaceship_pos = [WIDTH // 2, HEIGHT - 50]
spaceship_vel = 0

# List to store positions of projectiles
projectile_pos = []

# Velocity of the projectiles
projectile_vel = [5, 0]

# Speed of the projectiles
projectile_speed = 2

# Define helper functions

# Draw handler to draw the spaceship and projectiles
def draw(canvas):
    global spaceship_pos, projectile_pos
    
    # Draw spaceship
    canvas.draw_polygon([(spaceship_pos[0] - SPACESHIP_WIDTH // 2, spaceship_pos[1] - SPACESHIP_HEIGHT // 2),
                         (spaceship_pos[0] + SPACESHIP_WIDTH // 2, spaceship_pos[1] - SPACESHIP_HEIGHT // 2),
                         (spaceship_pos[0] + SPACESHIP_WIDTH // 2, spaceship_pos[1] + SPACESHIP_HEIGHT // 2),
                         (spaceship_pos[0] - SPACESHIP_WIDTH // 2, spaceship_pos[1] + SPACESHIP_HEIGHT // 2)], 1, 'White', 'White')
    
    # Draw projectiles
    for pos in projectile_pos:
        canvas.draw_circle(pos, PROJECTILE_RADIUS, 1, 'White', 'White')

    # Update projectile positions
    update_projectiles()
    
    # Update and draw spaceship position
    spaceship_pos[0] += spaceship_vel

# Function to update the game state and initiate firing of projectiles
def update():
    pass

# Function to update the positions of projectiles and check if they have left the frame
def update_projectiles():
    global projectile_pos
    for pos in projectile_pos:
        # Move the projectiles upwards (subtract from y-coordinate)
        pos[1] -= projectile_speed
    # Remove projectiles that have left the frame
    projectile_pos = [pos for pos in projectile_pos if pos[1] > 0]

# Keydown handler to control the movement of the spaceship and fire projectiles
def keydown(key):
    global spaceship_vel, projectile_pos
    if key == simplegui.KEY_MAP['a']:
        spaceship_vel = -5  # Move left
    elif key == simplegui.KEY_MAP['d']:
        spaceship_vel = 5   # Move right
    elif key == simplegui.KEY_MAP['space']:
        # Fire projectile from the spaceship's position
        projectile_pos.append([spaceship_pos[0], spaceship_pos[1] - SPACESHIP_HEIGHT // 2])

# Keyup handler to stop the movement of the spaceship when the key is released
def keyup(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['a'] or key == simplegui.KEY_MAP['d']:
        spaceship_vel = 0

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame('Space Invaders', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.start()

# Timer to continuously update the game state
timer = simplegui.create_timer(1000 // 60, update)
timer.start()
