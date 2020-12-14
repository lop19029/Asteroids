
"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import math
import arcade
import random
from abc import ABC
from abc import abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 650
BACKGROUND_IMAGE = "images/background.jpg"
LEVEL_UP_SOUND = "sounds/level_up.wav"

BULLET_IMAGE = "images/laser.png"
BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60
BULLET_ANGLE = 90
BULLET_SOUND = "sounds/laser_sound.wav"

SHIP_IMAGE = "images/ship.png"
SHIP_IMAGE_DMG = "images/ship8.png"
SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30
SHIP_CRACK_SOUND = "sounds/explosion.wav"

INITIAL_ROCK_COUNT = 5
ROCK_CRACK_SOUND = "sounds/asteroid_crash.wav"

BIG_ROCK_IMAGE = "images/big_rock.png"
BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_IMAGE = "images/mid_rock.png"
MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_IMAGE = "images/small_rock.png"
SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2


class Point:
    """
    Creates a point with (x,y) coordinates
    """
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y
    
class Velocity:
    """
    creates the values that increases (x,y) coordinates
    to move the object
    """
    def __init__(self, dx = 0.0, dy = 0.0):
        self.dx = dx
        self.dy = dy

class Flying_Object(Point, Velocity):
    """
    An object that appears and move on the screen
    """
    def __init__(self, radius = 0.0, alive = True):
        super().__init__()
        self.radius = radius
        self.alive = alive
    
    def advance(self):
        """
        Moves the object forward by the velocity
        """
        self.x += self.dx
        self.y += self.dy 
    
    def is_off_screen(self,SCREEN_WIDTH, SCREEN_HEIGHT):
        """Checks if the object is out of the screen limits"""
        if self.x < 0 or self.x > SCREEN_WIDTH:
            return True
        elif self.y < 0 or self.y > SCREEN_HEIGHT:
            return True
        else:
            return False
    
    def put_it_back(self):
        """Wraps the object around the screen"""
        #Checks when it goes off to the right, left, up or down. And put the object in the opposite side.
        if self.x > SCREEN_WIDTH + (self.radius*2.7):
            self.x = 0 - (self.radius*2.7)
        elif self.x < 0 - (self.radius*2.7):
            self.x = SCREEN_WIDTH + (self.radius*2.7)
        if self.y > SCREEN_HEIGHT + (self.radius*2.7):
            self.y = 0 - (self.radius*2.7)
        elif self.y < 0 - (self.radius*2.7):
            self.y = SCREEN_HEIGHT + (self.radius*2.7)

class Ship(arcade.Sprite, Flying_Object):
    """Users ship that shoots bullets to destroy asteroids"""
    def __init__(self):
        super().__init__()
        self.x = SCREEN_WIDTH//2
        self.y = SCREEN_HEIGHT//2
        self.dx = 0
        self.dy = 0
        self.alive = True
        
        self.radius = SHIP_RADIUS
    def draw(self,texture):
        #Use an image to draw the object
        width = texture.width
        height = texture.height
        alpha = 255
        x = self.x
        y = self.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
    def turn_right(self):
        #turns the ship 3 degrees to the right
        self.angle-=3
    def turn_left(self):
        #turns the ship 3 degrees to the left
        self.angle+=3   
    def thrust_up(self):
        self.dx += math.cos(math.radians(self.angle+90)) * SHIP_THRUST_AMOUNT
        self.dy += math.sin(math.radians(self.angle+90)) * SHIP_THRUST_AMOUNT
    def thrust_down(self):
        self.dx -= math.cos(math.radians(self.angle+90)) * SHIP_THRUST_AMOUNT
        self.dy -= math.sin(math.radians(self.angle+90)) * SHIP_THRUST_AMOUNT
    def crash(self):
        pass
        
class Laser(Flying_Object):
    def __init__(self, x = 0, y = 0, dx = 0, dy = 0, angle = 0.0):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = BULLET_RADIUS
        self.life = BULLET_LIFE
        self.angle = angle
        self.angle_fire = BULLET_ANGLE
        self.alive = True
    def draw(self,texture):
        #Use an image to draw the object
        width = texture.width
        height = texture.height
        alpha = 255

        x = self.x
        y = self.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        
    def fire(self,angle_fire):
        self.dx += math.cos(math.radians(angle_fire)) * BULLET_SPEED
        self.dy += math.sin(math.radians(angle_fire)) * BULLET_SPEED

    
class Asteroid(ABC, Flying_Object):
    """Object that moves and rotates on the screen
    waiting to be hit or to crash your ship
    """
    def __init__(self, radius = 0):
        super().__init__()
        self.radius = radius
        
    @abstractmethod
    def draw(self):
        """Draws the target using polymorphism"""
        raise NotImplementedError
    @abstractmethod
    def rotate(self):
        """Rotates the object using polymorphism"""
        raise NotImplementedError
    
    @abstractmethod
    def hit(self):
        """Using polymorphism, changes target status after a collision with a bullet."""
        raise NotImplementedError

class Big_Rock(arcade.Sprite, Asteroid):
    def __init__(self):
        super().__init__()
        x1 = random.uniform(0,((SCREEN_WIDTH//2)-100))
        x2 = random.uniform(((SCREEN_WIDTH//2)+100),SCREEN_WIDTH)
        choosex = [x1,x2]
        self.x = random.choice(choosex)
        y1 = random.uniform(0,((SCREEN_HEIGHT//2)-100))
        y2 = random.uniform(((SCREEN_HEIGHT//2)+100),SCREEN_HEIGHT)
        choosey = [y1,y2]
        self.y = random.choice(choosey)
        velocities = [-1*BIG_ROCK_SPEED, BIG_ROCK_SPEED]
        self.dx = random.choice(velocities)
        self.dy = random.choice(velocities)
        self.radius = BIG_ROCK_RADIUS
        self.alive = True
    
    def rotate(self):
        self.angle+= BIG_ROCK_SPIN
    
    def draw(self,texture):
        #Use an image to draw the object
        width = texture.width
        height = texture.height
        alpha = 255

        x = self.x
        y = self.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
          
    def hit(self):
        return 1      

class Mid_Rock(arcade.Sprite, Asteroid):
    def __init__(self, x = 0, y = 0, dx = 0, dy = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = MEDIUM_ROCK_RADIUS
        self.alive = True
    
    def rotate(self):
        self.angle+=MEDIUM_ROCK_SPIN
    
    def draw(self,texture):
        #Use an image to draw the object
        width = texture.width
        height = texture.height
        alpha = 255

        x = self.x
        y = self.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
          
    def hit(self):
        return 2
    
class Small_Rock(arcade.Sprite, Asteroid):
    def __init__(self, x = 0, y = 0, dx = 0, dy = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = SMALL_ROCK_RADIUS
        self.alive = True
        
    def rotate(self):
        self.angle+=SMALL_ROCK_SPIN
        
    def draw(self,texture):
        #Use an image to draw the object
        width = texture.width
        height = texture.height
        alpha = 255

        x = self.x
        y = self.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
              
    def hit(self):
        return 3
    
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        
        self.score = 0
        self.level = 1
        self.rocks_count = 5
        self.over = False

        self.held_keys = set()
        self.background = arcade.load_texture(BACKGROUND_IMAGE)
        self.ship_img = arcade.load_texture(SHIP_IMAGE)
        self.laser_img = arcade.load_texture(BULLET_IMAGE)
        self.big_rock_img = arcade.load_texture(BIG_ROCK_IMAGE)
        self.mid_rock_img = arcade.load_texture(MEDIUM_ROCK_IMAGE)
        self.small_rock_img = arcade.load_texture(SMALL_ROCK_IMAGE)
        
        self.laser_sound = arcade.load_sound(BULLET_SOUND)
        self.crash_sound = arcade.load_sound(SHIP_CRACK_SOUND)
        self.rock_crash = arcade.load_sound(ROCK_CRACK_SOUND)
        self.level_sound = arcade.load_sound(LEVEL_UP_SOUND)
        

        # TODO: declare anything here you need the game class to track
        self.lasers = []
        self.rocks = []
        self.ship = Ship()
        for item in range(1,self.rocks_count+1):
            item = Big_Rock()
            self.rocks.append(item)
        
    def check_wrapping(self):
        """checks if the object is off screen, and put it back in the game"""
        for rock in self.rocks:
            if rock.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                rock.put_it_back()
        if self.ship.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
            self.ship.put_it_back()
        for laser in self.lasers:
            if laser.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                laser.put_it_back()
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # TODO: draw each object
        self.draw_score()
        self.draw_level()
        self.ship.draw(self.ship_img)
        for rock in self.rocks:
            if type(rock) == Big_Rock:
                rock.draw(self.big_rock_img)
            elif type(rock) == Mid_Rock:
                rock.draw(self.mid_rock_img)
            else:
                rock.draw(self.small_rock_img)
        for laser in self.lasers:
            laser.draw(self.laser_img)
        if self.over:
            self.game_over()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_wrapping()
        self.cleanup_zombies()
        self.check_level()
       

        # TODO: Tell everything to advance or move forward one step in time
        self.ship.advance()
            
        for rock in self.rocks:
            rock.advance()
            rock.rotate()
        for laser in self.lasers:
            laser.advance()
            laser.life-=1
        # TODO: Check for collisions
        self.check_collisions()
    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)
    
    def draw_level(self):
        """
        Puts the current level on the screen
        """
        score_text = "Level {}".format(self.level)
        start_x = SCREEN_WIDTH//2
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)
        
    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        for rock in self.rocks:
            for laser in self.lasers:

                # Make sure they are both alive before checking for a collision
                if laser.alive and rock.alive:
                    too_close = laser.radius + rock.radius

                    if (abs(laser.x - rock.x) < too_close and
                                abs(laser.y - rock.y) < too_close):
                        # its a hit!
                        arcade.play_sound(self.rock_crash)
                        laser.alive = False
                        self.score += rock.hit()
                        if type(rock) == Big_Rock:
                            x = rock.x
                            y = rock.y
                            velx = rock.dx
                            vely = rock.dy
                            mid1 = Mid_Rock(x,y,velx,vely+2)
                            mid2 = Mid_Rock(x,y,velx,vely-2)
                            add = [mid1,mid2]
                            self.rocks.extend(add)
                        elif type(rock) == Mid_Rock:
                            x = rock.x
                            y = rock.y
                            velx = rock.dx
                            vely = rock.dy
                            small1 = Small_Rock(x,y,velx+1.5,vely+1.5)
                            small2 = Small_Rock(x,y,velx-1.5,vely-1.5)
                            add = [small1,small2]
                            self.rocks.extend(add)
                        rock.alive = False
                        
        for rock in self.rocks:
            # Make sure they are both alive before checking for a collision
            if rock.alive and self.ship.alive:
                too_close = rock.radius + self.ship.radius
                if (abs(rock.x - self.ship.x) < too_close and abs(rock.y - self.ship.y) < too_close):
                    # Collision alert! Ship got serious damage!
                    arcade.play_sound(self.crash_sound)
                    self.ship_img = arcade.load_texture(SHIP_IMAGE_DMG)
                    self.ship.alive = False
                    self.over = True
    def setup(self):
        self.score = 0
        self.level = 1
        self.rocks_count = 5
        self.over = False

        self.held_keys = set()
        self.background = arcade.load_texture(BACKGROUND_IMAGE)
        self.ship_img = arcade.load_texture(SHIP_IMAGE)
        self.laser_img = arcade.load_texture(BULLET_IMAGE)
        self.big_rock_img = arcade.load_texture(BIG_ROCK_IMAGE)
        self.mid_rock_img = arcade.load_texture(MEDIUM_ROCK_IMAGE)
        self.small_rock_img = arcade.load_texture(SMALL_ROCK_IMAGE)
        

        # TODO: declare anything here you need the game class to track
        self.lasers = []
        self.rocks = []
        self.ship = Ship()
        for item in range(1,self.rocks_count+1):
            item = Big_Rock()
            self.rocks.append(item)
    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for rock in self.rocks:
            if not rock.alive:
                self.rocks.remove(rock)

        for laser in self.lasers:
            if not laser.alive or laser.life <= 0:
                self.lasers.remove(laser)
                
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if self.ship.alive:
            if arcade.key.LEFT in self.held_keys:
                self.ship.turn_left()

            if arcade.key.RIGHT in self.held_keys:
                self.ship.turn_right()

            if arcade.key.UP in self.held_keys:
                self.ship.thrust_up()

            if arcade.key.DOWN in self.held_keys:
                self.ship.thrust_down()
    
        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass
        if arcade.key.SPACE in self.held_keys:
            pass

    
    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                x = self.ship.x
                y = self.ship.y
                dx = self.ship.dx
                dy = self.ship.dy
                angle = self.ship.angle + 90
                laser = Laser(x,y,dx,dy,angle)
                laser.fire(angle)
                self.lasers.append(laser)
                arcade.play_sound(self.laser_sound)
        
        self.held_keys.add(key)    
        if key == arcade.key.R:
            self.setup()
            

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
    def check_level(self):
        if len(self.rocks) <= 0:
            arcade.play_sound(self.level_sound)
            self.rocks_count+=1
            for item in range(1,self.rocks_count+1):
                item = Big_Rock()
                self.rocks.append(item)
            self.level += 1
            
            
    def game_over(self):
        arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("You scored {} points".format(self.score), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press R to restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.WHITE, font_size=25, anchor_x="center")
    
# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()

    
    
    