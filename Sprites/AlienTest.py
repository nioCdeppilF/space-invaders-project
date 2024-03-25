#AlienCode by bbksleazy
import math
try:
    import simplegui
    from user305_o32FtUyCKk_0 import Vector
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    class Vector:

        # Initialiser
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        # Returns a string representation of the vector
        def __str__(self):
            return "(" + str(self.x) + "," + str(self.y) + ")"

        # Tests the equality of this vector and another
        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

        # Tests the inequality of this vector and another
        def __ne__(self, other):
            return not self.__eq__(other)

        # Returns a tuple with the point corresponding to the vector
        def get_p(self):
            return (self.x, self.y)

        # Returns a copy of the vector
        def copy(self):
            return Vector(self.x, self.y)

        # Adds another vector to this vector
        def add(self, other):
            self.x += other.x
            self.y += other.y
            return self

        def __add__(self, other):
            return self.copy().add(other)

        # Negates the vector (makes it point in the opposite direction)
        def negate(self):
            return self.multiply(-1)

        def __neg__(self):
            return self.copy().negate()

        # Subtracts another vector from this vector
        def subtract(self, other):
            return self.add(-other)

        def __sub__(self, other):
            return self.copy().subtract(other)

        # Multiplies the vector by a scalar
        def multiply(self, k):
            self.x *= k
            self.y *= k
            return self

        def __mul__(self, k):
            return self.copy().multiply(k)

        def __rmul__(self, k):
            return self.copy().multiply(k)

        # Divides the vector by a scalar
        def divide(self, k):
            return self.multiply(1 / k)

        def __truediv__(self, k):
            return self.copy().divide(k)

        # Normalizes the vector
        def normalize(self):
            return self.divide(self.length())

        # Returns a normalized version of the vector
        def get_normalized(self):
            return self.copy().normalize()

        # Returns the dot product of this vector with another one
        def dot(self, other):
            return self.x * other.x + self.y * other.y

        # Returns the length of the vector
        def length(self):
            return math.sqrt(self.x ** 2 + self.y ** 2)

        # Returns the squared length of the vector
        def length_squared(self):
            return self.x ** 2 + self.y ** 2

        # Reflect this vector on a normal
        def reflect(self, normal):
            n = normal.copy()
            n.multiply(2 * self.dot(normal))
            self.subtract(n)
            return self

        # Returns the angle between this vector and another one
        def angle(self, other):
            return math.acos(self.dot(other) / (self.length() * other.length()))

        # Rotates the vector 90 degrees anticlockwise
        def rotate_anti(self):
            self.x, self.y = -self.y, self.x
            return self

        # Rotates the vector according to an angle theta given in radians
        def rotate_rad(self, theta):
            rx = self.x * math.cos(theta) - self.y * math.sin(theta)
            ry = self.x * math.sin(theta) + self.y * math.cos(theta)
            self.x, self.y = rx, ry
            return self

        # Rotates the vector according to an angle theta given in degrees
        def rotate(self, theta):
            theta_rad = theta / 180 * math.pi
            return self.rotate_rad(theta_rad)

        # project the vector onto a given vector
        def get_proj(self, vec):
            unit = vec.get_normalized()
            return unit.multiply(self.dot(unit))
import random

GAME_OVER_MESSAGE = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Space_Invaders_GameOver_Screen.png"
LIVES_COUNTER = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Lives_Sprite.jpg"

ALIEN_ROW1 = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Alien_row1.jpg"
ALIEN_ROW2 = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Alien_row2.jpg"
ALIEN_ROW3 = "https://raw.githubusercontent.com/nioCdeppilF/space-invaders-project/main/Alien_row3.png"


CW = 800
CH = 600
TIMER = 30 *2
GAME_OVER_BARRIER = CH - 100 - 50

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


class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def transition(self, time_duration):
        if self.time % time_duration == 0:
            return True

class Integrate:
    def __init__(self, clock, alien, lives):
        self.clock = clock
        self.alien_list = alien
        self.lives = lives
        self.score = 0

        self.vel = Vector(0.5, 0)
        self.game_over = False
        self.frame_index = [0, 0]
        self.frame_count = 1
        self.score_colour, self.score_num_colour = 'White', '#00fc04'


    def calc_lives(self):
        local_counter = 3
        if len(self.lives) > 0:
            for i in range(3):
                if self.lives[i].life_gone() == True:
                    local_counter -= 1
        return local_counter

    def draw(self, canvas):
        self.clock.tick()
        self.game_over_text(canvas)

        [l.draw(canvas) for l in self.lives]
        if len(self.lives) > 0: #Make it so if hit then starts to lose a life, just respawn dont end game till all lives gone
            self.lives[0].takeDamage()
            self.lives[1].takeDamage()
            #self.lives[2].takeDamage()

        #self.calc_lives()
        self.points(canvas)

        for a in range(len(self.alien_list)):
            self.alien_list[a].draw(canvas)
            if self.clock.transition(TIMER):
                self.update()
                self.alien_list[a].next_frame()

    def points(self, canvas):
        canvas.draw_text(f"Score:", (0, CH - 10), 40, self.score_colour)
        canvas.draw_text(f"{self.score}", (105, CH - 8), 40, self.score_num_colour)


    def drop(self, x):
        for a in range(len(self.alien_list)):
            self.alien_list[a].pos.add(Vector(x, 20))

    def update(self):
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






aliens = []
j_d = 15
point = 40
count = 0
for i in range(5):
    for j in range(11):
        aliens.append(Alien(Vector(20 + (j * 50), j_d), count))
        count += 1
    j_d += 50

player_lives = []
for i in range(3):
    player_lives.append(Lives((CW - 50 - (i * 100), CH - 20), False))


frame = simplegui.create_frame("Aliens", CW, CH)
clock = Clock()

i = Integrate(clock, aliens, player_lives)

frame.set_draw_handler(i.draw)
#frame.set_canvas_background("#b0b0b0")
frame.start()
#AlienCode by bbksleazy
