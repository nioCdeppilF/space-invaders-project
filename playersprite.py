import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Initialize global variables
WIDTH = 600
HEIGHT = 400
SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 20
PROJECTILE_RADIUS = 3
img = simplegui.load_image("https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/player.png")
img_dims  = (110,64)
img_centre = (55,32)
# Initial position and velocity of the spaceship
spaceship_pos = [WIDTH // 2, HEIGHT - 50]
spaceship_vel = 0
# List to store positions of projectiles
projectile_pos = []

# Velocity of the projectiles
projectile_vel = [5, 0]

# Speed of the projectiles
projectile_speed = 2


class playerSprite:
    def __init__(self, pos):
        self.pos = pos
        self.img_dim = (55,32)
    def draw(self,canvas):
        canvas.draw_image(img, img_centre,img_dims, self.pos,self.img_dim)

def update_projectiles():
    global projectile_pos
    for pos in projectile_pos:
    # Move the projectiles upwards (subtract from y-coordinate)
        pos[1] -= projectile_speed
# Remove projectiles that have left the frame
    projectile_pos = [pos for pos in projectile_pos if pos[1] > 0]
def keydown(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['a']:
        spaceship_vel = -5  # Move left
    elif key == simplegui.KEY_MAP['d']:
        spaceship_vel = 5   # Move right
    elif key == simplegui.KEY_MAP['space'] and len(projectile_pos) == 0:  # Fire only if no projectile exists
    # Fire projectile from the spaceship's position
         projectile_pos.append([spaceship_pos[0], spaceship_pos[1] - SPACESHIP_HEIGHT // 2])
# Keyup handler to stop the movement of the spaceship when the key is released
def keyup(key):
    global spaceship_vel
    if key == simplegui.KEY_MAP['a'] or key == simplegui.KEY_MAP['d']:
        spaceship_vel = 0

player=playerSprite(spaceship_pos)
def draw(canvas):
    global spaceship_pos
    
    # Draw spaceship
    canvas.draw_polygon([(spaceship_pos[0] - SPACESHIP_WIDTH // 2, spaceship_pos[1] - SPACESHIP_HEIGHT // 2),
                         (spaceship_pos[0] + SPACESHIP_WIDTH // 2, spaceship_pos[1] - SPACESHIP_HEIGHT // 2),
                         (spaceship_pos[0] + SPACESHIP_WIDTH // 2, spaceship_pos[1] + SPACESHIP_HEIGHT // 2),
                         (spaceship_pos[0] - SPACESHIP_WIDTH // 2, spaceship_pos[1] + SPACESHIP_HEIGHT // 2)], 1, 'Black', 'Black')
    # Draw projectiles
    for pos in projectile_pos:
        canvas.draw_circle(pos, PROJECTILE_RADIUS, 1, 'White', 'White')
    
    # Update projectile positions
    update_projectiles()
    
    # Update and draw spaceship position
    spaceship_pos[0] += spaceship_vel
    player.draw(canvas)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame('Space Invaders', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.start()
