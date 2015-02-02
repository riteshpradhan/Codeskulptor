########
# author: Ritesh Pradhan
# Codeskulptor project
# Asteroids
########

############@TODO:
# 1.  Spawning - never on the top of each other
# 2.  Rocks velocity to increase with score
#
# Input arguments and flags:
# Ouput:
# Assumptions: 
#   1. 
# Known issues:
#  1. Mixed kinda coding - e.g. Class-definitions, helper functions and key-handlers are not grouped together
#### Classes:
#  1. ImageInfo             : Information about the image - like size, radius etc.
#  3. Sprite                : Could be A. Missile, and B. Rock
#  3. Ship                  : Contains Missiles (missile group, a list of missiles)
#  4. Goodies               : A type of Sprite
###
###Helper functions:
# 0. main                   : Control the program's flow
# 1. angle_to_vector        : Returns a list of 2 elements giving cos(x), sin(x)
# 2. distance               : Distance between 2 points
# 3. group_collide          : Whether any member of this group (a Sprite) collided with an object (Ship)
# 4. group_group_collide    : Well...group to group collision - betwen two sprites.
# 5. process_sprite         : 
# 5. process_sprite_group   : Update position and draws the members of a Sprite list.

# 7. goodies_spawner           : Spawns rocks, randomly
#### Event Handlers:
# 1. draw_main_canvas       :
# 2. mute_unmute            : ...yeah, work in the offic too
# 3. reset_game             : Initialize the things, reset the game
# 4. get_rocks              : How many rocks at a time you want to see on screen?
# 5. get_missiles           : How many missiles you can fire (see on screen) simultaneously
# 6. keydown                :
# 7. keyup                  :
# 8. mouse_click            : To start the game
###Change History:
# DATE     PRG  REASON
############################################################################################
# 20130608 YM   First release
#
############################################################################################
# Imported/external modules:
import simplegui
import random
import math
###GlobalVariables
TOP_MARGIN=70
BOTTOM_MARGIN=60
RIGHT_MARGIN=20
LEFT_MARGIN=20
DRAW_AREA_WIDTH=800
DRAW_AREA_HEIGHT=500
#
CANVAS_HEIGHT=TOP_MARGIN+DRAW_AREA_HEIGHT+BOTTOM_MARGIN
CANVAS_WIDTH=LEFT_MARGIN+DRAW_AREA_WIDTH+RIGHT_MARGIN
NUMBER_OF_ROCKS_DEFAULT=12
NUMBER_OF_ROCKS=NUMBER_OF_ROCKS_DEFAULT
Total_number_of_Rocks=0
NUMBER_OF_GOODIES=1
GOODIE_VEL=2
Total_number_of_Goodies=0
NUMBER_OF_MISSILES_DEFAULT=10
NUMBER_OF_MISSILES=NUMBER_OF_MISSILES_DEFAULT
MISSILE_VEL=[4,4]
SNIPER_VEL=3
MAX_LIVES=3
strMessage=""
#
FRICTION=0.05
ACCELERATION=0.5
ACCELERATION_REVERSE=ACCELERATION * 0.05
ACCELERATION_VELOCITY=0.05
#
fGameIsOn=False
# globals for user interface
score = 0
lives = 3
fTime = 0.5
#
bMute=None
bReset=None
fMute=False
#
my_ship=None
rocks_set=set([])
explosion_set=set([])
#
enemy_ship=None
goodie=None
#
GOODIES=["Lazer", "Life","Protected","Long Range Missile","Death"]
LAZER=0
LIFE=1
PROTECTED=2
LONG_RANGE=3
DEATH=4
#
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
#
    def get_center(self):
        return self.center
#
    def get_size(self):
        return self.size
#
    def get_radius(self):
        return self.radius
#
    def get_lifespan(self):
        return self.lifespan
#
    def get_animated(self):
        return self.animated
###Images:
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png\
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
###Drawn using http://pixlr.com/editor/
enemy_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/59193937/SpaceShip.png?dl=1")
enemy_ship_info = ImageInfo([108, 80], [216, 161], 100, CANVAS_HEIGHT, False)
#enemy_ship_info=ImageInfo([enemy_image.get_width()/2,enemy_image.get_height()/2], [enemy_image.get_width(),enemy_image.get_height()], (enemy_image.get_width()+enemy_image.get_height())/2, CANVAS_WIDTH, True)
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
##
goodies_image= simplegui.load_image("http://images4.wikia.nocookie.net/__cb20121202223241/gltas/images/thumb/d/d1/FA-star.png/45px-FA-star.png")
goodies_info = ImageInfo([goodies_image.get_width()/2,goodies_image.get_height()/2],[goodies_image.get_width(),goodies_image.get_height()],goodies_image.get_width(),CANVAS_WIDTH)

###Sounds:
# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
        
###Helper functions to handle transformations
def angle_to_vector(ang):
#########################################################################################################
# Returns a list of cos(x) and sin(x) components ... breaks angular vectors into X and Y components
#########################################################################################################
    return [math.cos(ang), math.sin(ang)]
####
def distance(p,q):
#########################################################################################################
# Returns distance between two points
#########################################################################################################
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)
####
def group_collide(sprite_set, other_object, flgRemove=True):
############################################################################################
# See if other_object collided with any member of sprite_set 
############################################################################################
    for each_member in sprite_set:
         if (each_member.collide(other_object)):
             if (flgRemove == True):
                 each_member.set_dead()
                 sprite_set.remove(each_member)
             return True
    return False
###
def group_group_collide(sprite_set1, sprite_set2, flgRemove1=True, flgRemove2=True, flgExplode=True):
############################################################################################
# 1. Dont' ever-ever collide to your own, you know what -backside- just skip that part of test
# 2. Check if other object has come too near to you
# 3. If indicated - remove object from list  / explode etc.
############################################################################################
    if ( sprite_set1 == sprite_set2 ):
       for mem_g1 in sprite_set1:
           for mem_g2 in sprite_set2:
            if (mem_g1 == mem_g2):
                pass
            elif( mem_g1.collide(mem_g2) ):
                mem_g1.vel, mem_g2.vel = mem_g2.vel, mem_g1.vel
    else:
       for mem_g1 in sprite_set1:
           for mem_g2 in sprite_set2:
              if( mem_g1.collide(mem_g2) ):
                  if (flgExplode):
                       explode(mem_g1.get_position(), mem_g1.get_vel())
                  if (flgRemove1):
                      mem_g2.set_dead()
                      sprite_set2.remove(mem_g2)
                  if (flgRemove2):
                      mem_g1.set_dead()
                      sprite_set1.remove(mem_g1)
                  return True
    return False
###
def process_sprite(sprite, canvas):
############################################################################################
# Process the information of sprite group
############################################################################################
###
    if sprite.is_alive():
        sprite.draw(canvas)
        sprite.update()
#
def process_sprite_group(sprite_set, canvas):
############################################################################################
# Process the information of sprite group
############################################################################################
###
    for each_member in sprite_set:
        if each_member.is_alive():
            process_sprite(each_member,canvas)
        else:
            sprite_set.remove(each_member)
#
    return
def explode(position,vel=[0,0]):
#########################################################################################################
# Boom!
#########################################################################################################
    an_explosion =  Sprite(position, vel,0,0, explosion_image, explosion_info, explosion_sound)
    explosion_set.add(an_explosion)
#
    return
###
def encounter_with_enemy_ship(my_ship, enemy_ship):
#########################################################################################################
# Collide, shoot, get-shot by an enemy ship
#########################################################################################################
    if (group_collide(my_ship.missiles_set, enemy_ship)):
        my_ship.set_score_increment(20)
        explode(enemy_ship.get_position(), enemy_ship.get_vel())
        enemy_ship.set_dead()            

    if ( enemy_ship.collide(my_ship) or group_collide(enemy_ship.missiles_set, my_ship) ):
        if (my_ship.loose_a_life()):
            my_ship.set_super_power(GOODIES [PROTECTED])
            explode(my_ship.get_position(), my_ship.get_vel())
    if (enemy_ship.collide(my_ship)):
        enemy_ship.set_dead()
#
    return
###

##Handler functions:
def mute_unmute():
############################################################################################
# Mute / unmute
############################################################################################
###
    global fMute, bMute
    fMute = not fMute
    if  fMute:
        bMute.set_text("<]")
    else:
         bMute.set_text("<X]")
#
    return
###
def reset_game(canvas=None):
############################################################################################
# new / reset game
############################################################################################
    global my_ship, enemy_ship, NUMBER_OF_MISSILES, NUMBER_OF_ROCKS, fGameIsOn, goodie
    my_ship = Ship([CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    enemy_ship=None
    goodie=None
    NUMBER_OF_MISSILES=NUMBER_OF_MISSILES_DEFAULT
    NUMBER_OF_ROCKS=NUMBER_OF_ROCKS_DEFAULT
    fGameIsOn=False
#
    return
###
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos            = [pos[0],pos[1]]
        self.vel            = [vel[0],vel[1]]
        self.angle          = angle
        self.angle_vel      = 0
        self.image          = image
        self.image_center   = info.get_center()
        self.image_size     = info.get_size()
        self.radius         = info.get_radius()
        self.thrusters      = False
        self.rotators       = False
        self.reverse        = False
        self.thrust_sound   = ship_thrust_sound
        self.sound_is_on    = False
        self.missiles_set = set([])
        self.shooting       = False
        self.lives          = MAX_LIVES
        self.score          = 0
        self.age = 0
#
        self.power_duration  = 60*5 #approx 5 seconds
        ##self.super_power     = False
        self.set_super_power(GOODIES [PROTECTED])
#
    def get_radius(self):
        return self.radius
#
    def get_position(self):
        return self.pos
#
    def get_vel(self):
        return self.vel
#
    def get_score(self):
        return self.score
#
    def set_score_increment(self, iSomeNumber ):
        self.score += iSomeNumber
#
    def set_super_power(self, super_power ):
        if ( not super_power == None ):
            self.age = 0
            self.super_power = super_power
#
    def get_super_power(self):
        if (self.super_power == None):
            return ""
        else:
            return str(self.super_power)
#
    def am_i_safe(self):
        if ( self.age <= self.power_duration and self.get_super_power() == GOODIES[PROTECTED]):
            return True
        else:
            return False
#
    def get_age(self):
        return self.age
#
    def set_age(self, number):
        self.age = number
#
    def get_lives(self):
        return self.lives
#
    def loose_a_life(self):
        if (self.am_i_safe()):
            return False
        else:
            self.lives -= 1
            self.age = 0
            return True
#
    def give_lives(self, life):
        self.lives += life
        return True
#
    def draw(self,canvas):
        if (self.am_i_safe()):
            if (self.age % 3 == 0):
              canvas.draw_circle( self.pos,  self.get_radius(), 1, "#FFFFFF")
            elif ((self.age+1) % 3 == 0):
              canvas.draw_circle( self.pos,  self.get_radius(), 1, "#FF0000")
 #
        if ( self.thrusters ):
             canvas.draw_image( self.image, 
                               [self.image_center[0] + self.image_size[0],self.image_center[1] ],  self.image_size,
                               self.pos, self.image_size, self.angle)
             if (not fMute and self.thrust_sound):
                 if (not self.sound_is_on):
                    self.thrust_sound.rewind()
                 self.thrust_sound.play()
                 self.sound_is_on = True
        else:
             canvas.draw_image( self.image, 
                               self.image_center,  self.image_size,
                               self.pos, self.image_size, self.angle)
             if (not fMute and self.thrust_sound):
                 if (not self.sound_is_on):
                     self.thrust_sound.rewind()
                 self.sound_is_on = False
#
        if ( self.shooting ):
           self.shoot()
           if ( not (self.get_age()<self.power_duration and self.get_super_power() == GOODIES[LAZER])):
                self.shooting  = False
#
        process_sprite_group( self.missiles_set, canvas )
#
##    
    def update(self):
        if ( self.thrusters):
            self.vel[0] =  self.vel[0] + ACCELERATION * angle_to_vector(self.angle)[0]
            self.vel[1] =  self.vel[1] + ACCELERATION * angle_to_vector(self.angle)[1]
        else:
            self.vel[0] *=  ( 1 - FRICTION )
            self.vel[1] *=  ( 1 - FRICTION )
#
        if ( self.reverse):
            self.vel[0] =  self.vel[0] - ACCELERATION_REVERSE * angle_to_vector(self.angle)[0]
            self.vel[1] =  self.vel[1] - ACCELERATION_REVERSE * angle_to_vector(self.angle)[1]

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if ( self.rotators ): 
            self.angle  += self.angle_vel    
        else:
            self.angle_vel *= ( 1 - FRICTION )
#
        self.age += 1
        if ( self.age > self.power_duration ):
            self.super_power=None
#
###Wrap around:
        if ( self.pos[0]   < LEFT_MARGIN ): 
             self.pos[0] = CANVAS_WIDTH - RIGHT_MARGIN
        elif ( self.pos[0]  > CANVAS_WIDTH - RIGHT_MARGIN ): 
             self.pos[0] = LEFT_MARGIN
#
        if ( self.pos[1] <= TOP_MARGIN ): 
             self.pos[1] = CANVAS_HEIGHT - TOP_MARGIN
        elif ( self.pos[1] > CANVAS_HEIGHT - TOP_MARGIN ): 
             self.pos[1] = TOP_MARGIN
#
    def shoot(self):
        X_VEL=self.vel[0]+MISSILE_VEL[0]*angle_to_vector(self.angle)[0]
        Y_VEL=self.vel[1]+MISSILE_VEL[1]*angle_to_vector(self.angle)[1]
        if (self.get_super_power() == GOODIES[LONG_RANGE]):
            X_VEL=SNIPER_VEL*X_VEL
            Y_VEL=SNIPER_VEL*Y_VEL
        if (len(self.missiles_set) < NUMBER_OF_MISSILES): 
            a_missile  = Sprite( [self.pos[0]+self.image.get_width()*angle_to_vector(self.angle)[0]*1/4, 
                                  self.pos[1]+self.image.get_height()*angle_to_vector(self.angle)[1]/2], 
                                 [X_VEL,Y_VEL],
                                 0, 0, missile_image, missile_info, missile_sound)
            self.missiles_set.add(a_missile)
            return
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
        self.alive = True
        if ( not fMute and sound):
            sound.rewind()
            sound.play()
#
    def get_radius(self):
        return self.radius
#
    def get_position(self):
        return self.pos
#
    def get_vel(self):
        return self.vel
#
    def is_alive(self):
        return self.alive
#
    def set_dead(self):
        self.alive=False
        self.pos=[-999,-999]
#
    def draw(self, canvas):
        if (self.is_alive()):
            if (self.animated):
                canvas.draw_image( self.image, 
                                   [self.image_center[0]+self.image_size[0]*self.age ,self.image_center[0]],  self.image_size,
                                   self.pos, self.image_size, self.angle)
            else:
                canvas.draw_image( self.image, 
                                   self.image_center,  self.image_size,
                                   self.pos, self.image_size, self.angle)
#
    def update(self):
        if (self.alive and self.age < self.lifespan):
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]   
            self.angle  += self.angle_vel
            self.age += 1
        else:
            self.set_dead()
    ###Fallen off the edge?
        if ( self.pos[0] - self.get_radius() < LEFT_MARGIN or self.pos[0] + self.get_radius() > CANVAS_WIDTH - RIGHT_MARGIN 
              or self.pos[1] - self.get_radius() < TOP_MARGIN or self.pos[1] + self.get_radius() > CANVAS_HEIGHT - TOP_MARGIN ):
            self.set_dead()
###
    def collide(self, other_object):
        if (distance(self.pos, other_object.pos)) <= (self.get_radius() + other_object.get_radius()):
           return True
        else:
           return False
class Gooodie (Sprite):
    def __init__(self, goodie_type, pos, vel, ang, ang_vel, image, info, sound = None):
        self.goodie_type = goodie_type
        Sprite.__init__(self, pos, [GOODIE_VEL*vel[0],GOODIE_VEL*vel[1]], ang, ang_vel, image, info, sound = None)
#
    def get_goodie_type(self):
        return self.goodie_type
#
    def update(self):
        if (self.is_alive() and self.age < self.lifespan):
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]   
            self.angle  +=self.angle_vel
            self.age += 1
        else:
            self.set_dead()
    ###Bounce along the edge:
        if ( self.pos[0] - self.get_radius() < LEFT_MARGIN or self.pos[0] + self.get_radius() > CANVAS_WIDTH - RIGHT_MARGIN ):
             self.vel[0] = -self.vel[0] 
        if ( self.pos[1] - self.get_radius() < TOP_MARGIN or self.pos[1] + self.get_radius() > CANVAS_HEIGHT - TOP_MARGIN ):
             self.vel[1] = -self.vel[1] 
###
    def draw(self, canvas):
        canvas.draw_image( self.image, 
                            self.image_center,  self.image_size,
                             self.pos, self.image_size, self.angle)
#
        canvas.draw_text( str(self.get_goodie_type()), self.pos, 20, "#ffffff","serif")
#
class EnemyShip(Ship, Sprite):
    def __init__(self, pos, vel, angle, image, info):
        Ship.__init__(self, pos, vel, angle, image, info)
        Sprite.__init__(self, pos, vel, angle, angle/100, image, info, sound = None )
#
    def update(self, pos2):
        if (self.is_alive() and self.age < self.lifespan):
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]   
            self.angle   = math.pi + math.atan2 ( (self.pos[1] - pos2[1] ), ( self.pos[0] - pos2[0] ))
            self.age += 1
            if ( self.age % 50 == 0  and self.is_alive()):
               self.shooting  = True
               self.missiles_set=set([])
               self.shoot()
        else:
            self.set_dead()
    ###Bounce along the edge:
        if ( self.pos[0] - self.get_radius() < LEFT_MARGIN or self.pos[0] + self.get_radius() > CANVAS_WIDTH - RIGHT_MARGIN ):
             self.vel[0] = -self.vel[0] 
             self.angle =-self.angle 
        if ( self.pos[1] - self.get_radius() < TOP_MARGIN or self.pos[1] + self.get_radius() > CANVAS_HEIGHT - TOP_MARGIN ):
             self.vel[1] = -self.vel[1] 
             self.angle =-self.angle 
###
    def draw(self, canvas):
        canvas.draw_image( self.image, 
                           self.image_center,  self.image_size,
                           self.pos, self.image_size, self.angle)
#
        canvas.draw_text( "ENEMY", self.pos, 20, "#ffffff","serif")

def draw_main_canvas(canvas):
#########################################################################################################
#1.  Print Animiate background
#########################################################################################################
    global fTime, fGameIsOn, enemy_ship
#  
    fTime += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (fTime / 8) % center[0]
    canvas.draw_image( nebula_image, 
                       nebula_info.get_center(), nebula_info.get_size(), 
                       [ CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2], [DRAW_AREA_WIDTH, DRAW_AREA_HEIGHT])
    canvas.draw_image( debris_image, 
                       [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                       [ CANVAS_WIDTH / 2 + 1.25 * wtime, CANVAS_HEIGHT / 2], [( LEFT_MARGIN + DRAW_AREA_WIDTH) - 2.5 * wtime, CANVAS_HEIGHT])
    canvas.draw_image( debris_image, 
                       [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, DRAW_AREA_HEIGHT / 2], [2.5 * wtime, DRAW_AREA_HEIGHT])
###
    if ( not fGameIsOn ):
        canvas.draw_image( splash_image, 
                       splash_info.get_center(), splash_info.get_size(), 
                       [ CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2], [DRAW_AREA_WIDTH, DRAW_AREA_HEIGHT])
        return
##
# Draw ship and sprites
    my_ship.draw(canvas)
# Update ship and sprites
    my_ship.update()
#
    process_sprite_group( rocks_set, canvas )
    if (not goodie == None): 
        process_sprite( goodie, canvas)
        if (goodie.collide(my_ship)):
            goodie_type = goodie.get_goodie_type()
            if (goodie_type == GOODIES [LAZER]):
                 my_ship.set_super_power(GOODIES [LAZER])
            elif (goodie_type == GOODIES [LIFE]):
                 my_ship.give_lives(1)                       #Incidently...LIFE is 1!
            elif (goodie_type == GOODIES [PROTECTED]):
                 my_ship.set_super_power(GOODIES [PROTECTED])
            elif (goodie_type == GOODIES [LONG_RANGE]):
                 my_ship.set_super_power(GOODIES [LONG_RANGE])
            elif (goodie_type == GOODIES [DEATH]):
                  my_ship.give_lives(-1)
            goodie.set_dead()        
# Did I hit something...?
    if (group_collide(rocks_set, my_ship)):
        if (my_ship.loose_a_life()):
            my_ship.set_super_power(GOODIES [PROTECTED])
        explode(my_ship.get_position(), my_ship.get_vel())
#
            
    if (my_ship.get_lives() <= 0): 
           fGameIsOn = False
# Did I shot something...?
    if (group_group_collide(my_ship.missiles_set, rocks_set, True, True, True)):
        my_ship.set_score_increment(10)
    process_sprite_group( my_ship.missiles_set, canvas )
    process_sprite_group(explosion_set, canvas)
    


#
    if ( not enemy_ship == None ):
        enemy_ship.draw(canvas)
        enemy_ship.update(my_ship.pos)
        process_sprite_group( enemy_ship.missiles_set, canvas )
        encounter_with_enemy_ship(my_ship, enemy_ship)
#

####Stupid rocks...!
    group_group_collide(rocks_set, rocks_set)
####Just beautify the draw area!
    canvas.draw_polygon([[0,0],[CANVAS_WIDTH,0],[CANVAS_WIDTH,TOP_MARGIN],[0,TOP_MARGIN]]
                        , 1, "Red","Grey")
    canvas.draw_polygon([[0,CANVAS_HEIGHT],[CANVAS_WIDTH,CANVAS_HEIGHT],[CANVAS_WIDTH,CANVAS_HEIGHT - BOTTOM_MARGIN],[0,CANVAS_HEIGHT - BOTTOM_MARGIN]]
                        , 1, "black","black")
    canvas.draw_polygon([[0,TOP_MARGIN],[LEFT_MARGIN,TOP_MARGIN],[LEFT_MARGIN,CANVAS_HEIGHT-BOTTOM_MARGIN],[0,CANVAS_HEIGHT-BOTTOM_MARGIN]]
                        , 1, "black","black")
    canvas.draw_polygon([[CANVAS_WIDTH-RIGHT_MARGIN,TOP_MARGIN],[CANVAS_WIDTH,TOP_MARGIN],[CANVAS_WIDTH,CANVAS_HEIGHT - BOTTOM_MARGIN],[CANVAS_WIDTH-RIGHT_MARGIN,CANVAS_HEIGHT - BOTTOM_MARGIN]]
                        , 1, "black","black")
    canvas.draw_text("RiceRocks!", [CANVAS_WIDTH/2-100, 30], TOP_MARGIN/2, "#00ffff ","sans-serif")
    canvas.draw_text("Lives:" + str(my_ship.get_lives()), [LEFT_MARGIN, TOP_MARGIN/4], TOP_MARGIN/4, "#110000","monospace")
    canvas.draw_text("Score:" + str(my_ship.get_score()), [CANVAS_WIDTH - 10*RIGHT_MARGIN, TOP_MARGIN/4], TOP_MARGIN/4, "#110000","sans-serif")
    if (fMute):
        canvas.draw_text("Game sounds muted", [LEFT_MARGIN, TOP_MARGIN],TOP_MARGIN/4, "#FF0000","sans-serif")
#
    canvas.draw_text("Rocks: " + str(NUMBER_OF_ROCKS), [LEFT_MARGIN, TOP_MARGIN/2+10], TOP_MARGIN/4, "#F0F0F0","serif")
    #canvas.draw_text("Shots(simultaneous):" + str(NUMBER_OF_MISSILES), [CANVAS_WIDTH - 10*RIGHT_MARGIN, TOP_MARGIN/2+10], TOP_MARGIN/4, "#F0F0F0","serif")
    canvas.draw_text(my_ship.get_super_power(), [CANVAS_WIDTH- 10*RIGHT_MARGIN , TOP_MARGIN],TOP_MARGIN/4, "#FF0000","sans-serif")

    canvas.draw_text("Ship-velocity, X:" + str(round(my_ship.vel[0],2)) + ", Y:" + str(round(my_ship.vel[1],2)), [LEFT_MARGIN, CANVAS_HEIGHT - BOTTOM_MARGIN +10], 10, "#FF00FF")
#
    canvas.draw_text(str(strMessage) ,[LEFT_MARGIN/2, CANVAS_HEIGHT-30], 18, "#FFDDEE", "sans-serif")
#   

#
#Time / Event handlers:
# timer handler that spawns a rock    
def rock_spawner():
############################################################################################
# Timer - spawns rocks
############################################################################################
        global Total_number_of_Rocks
        X_DIR= 1 if ( random.random() > 0.5) else -1
        Y_DIR= 1 if ( random.random() > 0.5) else -1
        CLK = 1 if ( random.random() > 0.5) else -1
        pos=[X_DIR*my_ship.get_score()*random.random()/100, Y_DIR*my_ship.get_score()*random.random()/100]
       
        if ( (len(rocks_set) < NUMBER_OF_ROCKS) and not (pos == my_ship.get_position())): 
            a_rock =  Sprite([CANVAS_WIDTH * random.random(), CANVAS_HEIGHT * random.random()],
                              pos,
                              random.random(), random.random()*0.1*CLK , asteroid_image, asteroid_info)
#
            if ( (not a_rock.collide(my_ship)) and (not group_collide( rocks_set, a_rock, False))):
                rocks_set.add(a_rock)
                Total_number_of_Rocks +=1
            else:
               a_rock.set_dead()
#

        return
###
def goodies_spawner():
############################################################################################
# Timer - spawns goodies
############################################################################################
        global goodie, enemy_ship
        global Total_number_of_Goodies
        X_DIR= 1 if ( random.random() > 0.5) else -1
        Y_DIR= 1 if ( random.random() > 0.5) else -1
        goodie_number = random.randint(0,5)
        if (goodie_number == 5):
            enemy_ship = EnemyShip([random.randint(LEFT_MARGIN, CANVAS_WIDTH-RIGHT_MARGIN), random.randint(TOP_MARGIN, CANVAS_HEIGHT-BOTTOM_MARGIN)],
                              [random.random()*X_DIR, random.random()*Y_DIR],
                              random.random(), ship_image, ship_info)

        else:
            goodie =  Gooodie(GOODIES[goodie_number],[random.randint(LEFT_MARGIN, CANVAS_WIDTH-RIGHT_MARGIN), random.randint(TOP_MARGIN, CANVAS_HEIGHT-BOTTOM_MARGIN)],
                              [random.random()*X_DIR, random.random()*Y_DIR],
                              0,0, goodies_image, goodies_info)
#
            Total_number_of_Goodies +=1
#
        return
###
def get_rocks(rocks):
############################################################################################
# How many rocks you can handle on screen at a time?
############################################################################################
    global NUMBER_OF_ROCKS
    if rocks.isdigit():
       NUMBER_OF_ROCKS=int(rocks)
    if NUMBER_OF_ROCKS < 1:
       NUMBER_OF_ROCKS = 1
###
def get_missiles(missiles):
############################################################################################
# How many shots you can fire at a time?
############################################################################################
    global NUMBER_OF_MISSILES
    if missiles.isdigit():
       NUMBER_OF_MISSILES=int(missiles)
    if NUMBER_OF_MISSILES < 1:
       NUMBER_OF_MISSILES = 1


###
    
def keydown(key):
############################################################################################
#
############################################################################################
    ##global a_bubble, firing_angle_vel, bubble_stuck
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel = -1 * ACCELERATION_VELOCITY
        my_ship.rotators = True
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel =  ACCELERATION_VELOCITY
        my_ship.rotators = True
###
    elif simplegui.KEY_MAP["up"] == key:
            my_ship.thrusters=True
    elif simplegui.KEY_MAP["down"] == key:
            my_ship.reverse = True
###
    elif simplegui.KEY_MAP["space"] == key:
                 my_ship.shooting=True
###
def keyup(key):
############################################################################################
#
############################################################################################
    global firing_angle_vel
    ##global a_bubble, firing_angle_vel, bubble_stuck
    if simplegui.KEY_MAP["left"] == key:
        my_ship.rotators = False
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.rotators = False
###
    elif simplegui.KEY_MAP["up"] == key:
             my_ship.thrusters=False
    elif simplegui.KEY_MAP["down"] == key:
             my_ship.reverse = False
###
    elif simplegui.KEY_MAP["space"] == key:
             my_ship.shooting=False

###
def mouse_click(position):
############################################################################################
#
############################################################################################
    global fGameIsOn
    if (not fGameIsOn):
        reset_game()
        fGameIsOn = True
    return
####
def main():
############################################################################################
#Control the program-flow
#1. Create frame
#2. Add/register controls
#3. Start the frame
############################################################################################
    global my_ship, bMute, bReset
# initialization frame
    frameRiceRocks = simplegui.create_frame("Asteroids", CANVAS_WIDTH, CANVAS_HEIGHT)
#
    bMute = frameRiceRocks.add_button("<X]]",  mute_unmute, 30)
    bReset = frameRiceRocks.add_button("Reset",  reset_game, 100)
    frameRiceRocks.add_input("No.of Rocks:", get_rocks, 100)
    #frameRiceRocks.add_input("No.of Shots:", get_missiles, 100)

# register handlers
    frameRiceRocks.set_draw_handler(draw_main_canvas)
    frameRiceRocks.set_keydown_handler(keydown)
    frameRiceRocks.set_keyup_handler(keyup)
    frameRiceRocks.set_mouseclick_handler(mouse_click)
#
    rock_timer = simplegui.create_timer(1000.0, rock_spawner)
    goodies_timer = simplegui.create_timer(10000.0, goodies_spawner)
#
    # get things rolling
    rock_timer.start()
    goodies_timer.start()
    frameRiceRocks.start()
    # initialize ship and two sprites
    reset_game()
#
###
###Finally - don't run if this program is 'imported''
if __name__ == "__main__":
     main()
#
###End Of Program 