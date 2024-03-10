import simplegui

# Initialize global variables
WIDTH = 600
HEIGHT = 400
SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 20
PROJECTILE_RADIUS = 3
spaceship_pos = [WIDTH // 2, HEIGHT - 50]
spaceship_vel = 0
projectile_pos = []
projectile_vel = [-5, 0]
projectile_speed = 5
is_firing = True

# Define helper functions
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
    
    # Update and draw spaceship position
    spaceship_pos[0] += spaceship_vel
    
    # Update and draw projectile positions
    update_projectiles()

def update():
    global is_firing
    if is_firing:
        projectile_pos.append([spaceship_pos[0], spaceship_pos[1] - SPACESHIP_HEIGHT // 2])
        is_firing = False

def update_projectiles():
    global projectile_pos, is_firing
    for pos in projectile_pos:
        pos[1] -= projectile_speed
    if projectile_pos and projectile_pos[0][1] < 0:
        projectile_pos.pop(0)
        is_firing = True

def keydown(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['a']:
        spaceship_vel = -5
    elif key == simplegui.KEY_MAP['d']:
        spaceship_vel = 5

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

# Timer to continuously update
timer = simplegui.create_timer(1000 // 60, update)
timer.start()
