import pygame
import math
import random
import time

# Colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = (  0, 255,   0)
RED    = (255,   0,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)

# Screen dimensions
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# pygame.font.match_font() search a font based in input received, typed correctly or not
font_name = pygame.font.match_font('arial')

# Funtion used to manage texts
def Print_in_screen(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # width = 40
        # height = 60
        # self.image = pygame.Surface([width, height])
        # self.image.fill(BLACK)
        self.load_img()
        self.image = self.idle_right[0]
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        self.current_frame = 0
        self.last_update = 0
        self.facing = 'right'
        self.idle = True
        self.walking = False
        self.jumping = False
        self.attacking = False
        # List of sprites we can bump against
        self.level = None

    def load_img(self):
        self.idle_right = []
        for frame in range(0, 10):
            img = pygame.image.load('img/player_idle_00{}.png'.format(frame)).convert_alpha()
            self.idle_right.append(img)
        for frame in range(0, 5):
            img = pygame.image.load('img/player_idle_01{}.png'.format(frame)).convert_alpha()
            self.idle_right.append(img)

        self.walking_right = []
        for frame in range(0, 10):
            img = pygame.image.load('img/player_00{}.png'.format(frame)).convert_alpha()
            self.walking_right.append(img)
        for frame in range(0, 5):
            img = pygame.image.load('img/player_01{}.png'.format(frame)).convert_alpha()
            self.walking_right.append(img)

        self.jump_right = []
        for frame in range(0, 10):
            img = pygame.image.load('img/player_jump_00{}.png'.format(frame)).convert_alpha()
            self.jump_right.append(img)
        for frame in range(0, 5):
            img = pygame.image.load('img/player_jump_01{}.png'.format(frame)).convert_alpha()
            self.jump_right.append(img)

        self.attacking_right = []
        for frame in range(0, 10):
            img = pygame.image.load('img/player_attacking_00{}.png'.format(frame)).convert_alpha()
            self.attacking_right.append(img)
        for frame in range(0, 5):
            img = pygame.image.load('img/player_attacking_01{}.png'.format(frame)).convert_alpha()
            self.attacking_right.append(img)

        self.walking_left = []
        for frame in self.walking_right:
            self.walking_left.append(pygame.transform.flip(frame, True, False))

        self.idle_left = []
        for frame in self.idle_right:
            self.idle_left.append(pygame.transform.flip(frame, True, False))

        self.jump_left = []
        for frame in self.jump_right:
            self.jump_left.append(pygame.transform.flip(frame, True, False))

        self.attacking_left = []
        for frame in self.attacking_right:
            self.attacking_left.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        now = pygame.time.get_ticks()

        if self.attacking:
            if now - self.last_update > 50:
                self.last_update = now
                if self.facing == 'right':
                    self.current_frame = (self.current_frame + 1) % len(self.attacking_right)
                    if self.current_frame < len(self.attacking_right):
                        self.image = self.attacking_right[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.attacking_left)
                    self.image = self.attacking_left[self.current_frame]

        if self.jumping:
            if now - self.last_update > 100:
                self.last_update = now
                if self.facing == 'right':
                    self.current_frame = (self.current_frame + 1) % len(self.jump_right)
                    self.image = self.jump_right[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.jump_left)
                    self.image = self.jump_left[self.current_frame]

        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                if self.change_x > 0:
                    self.current_frame = (self.current_frame + 1) % len(self.walking_right)
                    self.image = self.walking_right[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.walking_left)
                    self.image = self.walking_left[self.current_frame]

        if not self.jumping and not self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                if self.facing == 'right':
                    self.current_frame = (self.current_frame + 1) % len(self.idle_right)
                    self.image = self.idle_right[self.current_frame]

                else:
                    self.current_frame = (self.current_frame + 1) % len(self.idle_left)
                    self.image = self.idle_left[self.current_frame]

    def update(self):
        """ Move the player. """
        if self.change_y != 0:
            self.jumping = True
            self.walking = False
        else:
            self.jumping = False

        if self.change_x != 0:
            self.walking = True
        else:
            self.walking = False

        self.animate()
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        block_hit_list_enemy = pygame.sprite.spritecollide(self, self.level.enemy_list, False)

        for block1 in block_hit_list_enemy:
            if self.change_x > 0:
                self.rect.right = block1.rect.left
            if self.change_x < 0:
                self.rect.left = block1.rect.right

        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left

            if self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        block_hit_list_enemy = pygame.sprite.spritecollide(self, self.level.enemy_list, False)

        for block1 in block_hit_list_enemy:
            if self.change_y > 0:
                self.rect.bottom = block1.rect.top
            if self.change_y < 0:
                self.rect.top = block1.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        # Check and see if we hit anything
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        self.rect.y -= 2
        self.jumping = True

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
        if len(enemy_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def shoot(self):
        if self.attacking:
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            self.level.bullet_list.add(bullet)
            if self.facing == 'right':
                bullet.speed = 10
            if self.facing == 'left':
                bullet.speed = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 0

    def update(self):
        self.rect.x += self.speed


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = pygame.Surface([width, height])
        #self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, min_x, max_x):
        super().__init__()

        self.load_img()
        self.image = pygame.image.load('img/enemy_walking_000.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.facing = 'right'
        self.pos_x = self.rect.x
        self.change_x = 1
        self.min_x = min_x
        self.max_x = max_x
        self.current_frame = 0
        self.last_update = 0

    def load_img(self):
        self.walking_left = []
        for frame in range(0, 10):
            img = pygame.image.load('img/enemy_walking_00{}.png'.format(frame))
            self.walking_left.append(img)


        self.walking_right = []
        for frame in self.walking_left:
            self.walking_right.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        now = pygame.time.get_ticks()
        if self.facing == 'left':
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_left)
                self.image = self.walking_left[self.current_frame]
        else:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_right)
                self.image = self.walking_right[self.current_frame]

    def update(self):
        self.animate()
        self.rect.x += self.change_x
        if self.rect.left < self.min_x:
            self.change_x = 1
            self.facing = 'right'
        if self.rect.right > self.max_x:
            self.change_x = -1
            self.facing = 'left'


class Level(pygame.sprite.Sprite):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/level 1.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.player = player

        # How far this world has been scrolled left/right
        self.world_shift = 0
    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.bullet_list.update()
        for bullet in self.bullet_list:
            if bullet.rect.x > SCREEN_WIDTH or bullet.rect.x < -20:
                self.bullet_list.remove(bullet)
        self.hits_enemy = pygame.sprite.groupcollide(self.bullet_list, self.enemy_list, True, True)
        self.hits_platform = pygame.sprite.groupcollide(self.platform_list, self.bullet_list, False, True)

    def draw(self, screen):
        """ Draw everything on this level. """
        # Draw the background
        #screen.fill(BLACK)


        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        screen.blit(self.image, [self.rect.x, 0])
        self.enemy_list.draw(screen)
        self.bullet_list.draw(screen)

        # Draw text on the screen
        Print_in_screen(screen, 'Teste', 100, SCREEN_WIDTH / 2, 50)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x
        self.rect.x += shift_x
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            enemy.min_x += shift_x
            enemy.max_x += shift_x

        for bullet in self.bullet_list:
            bullet.rect.x += shift_x


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)
        self.level_limit = -300

        # Array with width, height, x, and y of platform
        level = [
                [ 120, 1360,    0,   0],
                [3200,   60,    0, 710],
                [ 512,  130,  512, 580],
                [ 260,   20, 1150, 452],
                [ 257,   20, 1792, 516],
                [ 257,   20, 2305, 516],
                [ 120, 1360, 3200,   0],
                ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        #Enemies in the level
        self.enemy_list.add(Enemy(800, 535, 600, 1000))
        self.enemy_list.add(Enemy(1300, 405, 1130, 1400))


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [
                [120, 800,-200,  0],
                [100,  10, 450, 600],
                [ 10, 100, 540, 500],
                [100,  10, 540, 500],
                [ 10, 100, 630, 410],
                [100,  10, 630, 410],
                [ 10, 100, 720, 320],
                [100,  10, 720, 320],
                [ 10, 100, 810, 230],
                [100,  10, 810, 230],
                [ 10, 100, 900, 140],
                [100,  10, 900, 140],
                [ 10, 100, 990,  50],
                [100,  10, 990,  50],
                [ 10, 300, 1080,-240]
                ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        self.enemy_list.add(Enemy(400, 550, 200, 450))


def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    #screen = pygame.display.set_mode((size), pygame.FULLSCREEN)

    pygame.display.set_caption("Side-scrolling Platformer")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()

    player.level = current_level
    player.rect.x = 340
    player.rect.y = 600

    active_sprite_list.add(player)

    pygame.mouse.set_visible(False)

    pygame.joystick.init()

    joysticks = []
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()


    # Loop until the user clicks the close button.
    done = False

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_left()
                    player.facing = 'left'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_right()
                    player.facing = 'right'
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    player.attacking = True
                    pygame.time.set_timer(pygame.USEREVENT+1, 500)
                    player.shoot()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d and player.change_x > 0:
                    player.stop()


            #Joysick buttons:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0 or event.button == 1:
                    player.jump()
                if event.button == 2 or event.button == 3:
                    player.attacking = True
                    pygame.time.set_timer(pygame.USEREVENT+1, 500)
                    player.shoot()

            if event.type == pygame.USEREVENT + 1:
                player.attacking = False


        # Joystick analog:
        joystick_count = pygame.joystick.get_count()
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            for i in range(2):
                axis = joystick.get_axis(i)
                # if i == 0 and -0.2 < axis < 0.2:
                #     player.stop()
                if i == 0 and axis > 0.2:
                    player.go_right()
                    player.facing = 'right'
                if i == 0 and axis < -0.2:
                    player.go_left()
                    player.facing = 'left'

            # Joystick arrows:
            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            # First one: 1 for right and -1 for left
            # Second one: 1 for up and -1 for down
            hats = joystick.get_numhats()

            for i in range(hats):
                hat = joystick.get_hat(i)
                if hat == (1, 0):
                    player.go_right()
                    player.facing = 'right'
                if hat == (-1, 0):
                    player.go_left()
                    player.facing = 'left'

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 600:
            diff = player.rect.right - 600
            player.rect.right = 600
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        # current_position = player.rect.x + current_level.world_shift
        # if current_position < current_level.level_limit:
        #     player.rect.x = 120
        #     if current_level_no < len(level_list) - 1:
        #         current_level_no += 1
        #         current_level = level_list[current_level_no]
        #         player.level = current_level

        # Draw the sprites
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # Limit to 60 frames per second
        clock.tick(60)

        # Update the screen with what we've drawn.
        pygame.display.flip()
        print(player.attacking)
    pygame.quit()


main()
