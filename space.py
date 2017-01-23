# implementation of Spaceship - program template for RiceRocks

# bonuses - multiple rock, explosion and missile images
# rock and explosion choise is based on random, missiles changes in order
# another fancy feature - EXPLOSIONS in the end

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.f2014.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")
missile_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
missile_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/brown.png.png")
asteroid_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
explosion_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")
explosion_image4 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

#creating tuple of asteroid images

asteroid_images = (asteroid_image1, asteroid_image2, asteroid_image3)
missile_images = [missile_image1, missile_image2, missile_image3]
explosion_images = (explosion_image1, explosion_image2, explosion_image3, explosion_image4)

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.shoot_count = 0 # fancy variable to change missile image
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .15
            self.vel[1] += acc[1] * .15
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def shoot(self):
        if self.shoot_count > 2:
            self.shoot_count = 0
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0,
                                 missile_images[self.shoot_count], missile_info, missile_sound))
        self.shoot_count += 1
    
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        self.age += 1
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # should missile die or fly more
        if self.age > self.lifespan:
            return True
        else:
            return False

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, another_object):
        if dist(self.pos, another_object.pos) <= self.get_radius() + another_object.get_radius():
            return True
        else:
            return False

# helper functions for processing sprite groups and other stuff
def process_sprite_group(sprite_set, canvas):
    for sprite in set(sprite_set):
        if sprite.update():
            sprite_set.remove(sprite)
        else:
            sprite.draw(canvas)

def group_collide(sprite_group, another_object):
    collide = False
    for sprite in set(sprite_group):
        if sprite.collide(another_object):
            sprite_group.remove(sprite)
            explosion_group.add(Sprite(sprite.get_position(), [0,0], 0, 0, 
                                       random.choice(explosion_images), explosion_info, explosion_sound))
            collide = True
    return collide

def group_group_collide(first_group, second_group):
    score_change = 0
    for sprite in set(first_group):
        if group_collide(second_group, sprite):
            first_group.discard(sprite)
            score_change += 1
    return score_change

# key handlers to control ship
# if I'll get time at some point to add multiplayer, I should use dictionaries for controls 
# and iterate through them in key handlers

def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    global lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        timer.start()

def draw(canvas):
    global time, started
    global lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and missiles
    my_ship.draw(canvas)
    # update ship and missiles
    my_ship.update()
    
    score += group_group_collide(rock_group, missile_group)
    if group_collide(rock_group, my_ship):
        lives -= 1
    if lives == 0:
        started = False
        for rock in set(rock_group):
            rock_group.discard(rock)
            explosion_group.add(Sprite(rock.get_position(), [0,0], 0, 0, 
                                       random.choice(explosion_images), explosion_info, explosion_sound))
        for missile in set(missile_group):
            missile_group.discard(missile)
        timer.stop()
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    global score
    score_multiplier = 1 + score * .25
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [(random.random() * .6 - .3) * score_multiplier, (random.random() * .6 - .3) * score_multiplier]
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, random.choice(asteroid_images), asteroid_info)
    if len(rock_group) < 12 and dist(my_ship.get_position(), rock_pos) > my_ship.get_radius() + asteroid_info.get_radius() + 20:
        rock_group.add(a_rock)
            
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
