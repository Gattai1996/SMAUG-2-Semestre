import pygame
import pytmx
from os import path
from random import *


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
# Set the height and width of the screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# pygame.font.match_font() search a font based in input received, typed correctly or not
font_name = pygame.font.match_font('princeofpersia')


# Function used to manage texts
def print_in_screen(surf, text, tamanho, x, y):
    font = pygame.font.Font(font_name, tamanho)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_life_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 200
    bar_height = 20
    fill = (pct / 200) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


def draw_HUD_bar(surf, x, y):
    HUD_length = SCREEN_WIDTH
    HUD_height = 60
    HUD = pygame.Rect(x, y, HUD_length, HUD_height)
    pygame.draw.rect(surf, BLACK, HUD)


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
        self.melee_right = []
        self.melee_left = []
        self.idle_left = []
        self.attacking_left = []
        self.jump_left = []
        self.walking_left = []
        self.attacking_right = []
        self.jump_right = []
        self.falling_right = []
        self.falling_left = []
        self.walking_right = []
        self.idle_right = []
        self.dashing_right = []
        self.dashing_left = []

        self.load_img()
        self.image = self.idle_right[0]
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        self.radius = 25
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
        self.melee_atk = False
        self.dash = False

        self.dash_limit = False

        self.level = None
        self.life = 200
        self.dano_delay = False
        self.attack_delay = False
        self.melee_delay = False
        self.dash_delay = 0

        self.dash_change_x = 0
        self.pos_init_dash = 0
        self.dash_right = 0
        self.dash_left = 0

        self.spike = pygame.mixer.Sound('sfx/spike_hit.wav')
        self.heart = pygame.mixer.Sound('sfx/heart.wav')
        self.faca_1 = pygame.mixer.Sound('sfx/faca_1.wav')
        self.faca_2 = pygame.mixer.Sound('sfx/faca_2.wav')
        self.ataque_1 = pygame.mixer.Sound('sfx/ataque_1.wav')
        self.ataque_2 = pygame.mixer.Sound('sfx/ataque_2.wav')


    def load_img(self):
        for frame in range(0, 10):
            img = pygame.image.load('img/player_dash_00{}.png'.format(frame)).convert_alpha()
            self.dashing_right.append(img)

        for frame in range(0, 10):
            img = pygame.image.load('img/player_melee_00{}.png'.format(frame)).convert_alpha()
            self.melee_right.append(img)
        for frame in range(0, 5):
            img = pygame.image.load('img/player_melee_01{}.png'.format(frame)).convert_alpha()
            self.melee_right.append(img)

        for frame in range(0, 10):
            img = pygame.image.load('img/player_idle_00{}.png'.format(frame)).convert_alpha()
            self.idle_right.append(img)
        for frame in range(0, 5):
            img = pygame.image.load('img/player_idle_01{}.png'.format(frame)).convert_alpha()
            self.idle_right.append(img)

        for frame in range(0, 10):
            img = pygame.image.load('img/player_00{}.png'.format(frame)).convert_alpha()
            self.walking_right.append(img)
        for frame in range(0, 5):
            img = pygame.image.load('img/player_01{}.png'.format(frame)).convert_alpha()
            self.walking_right.append(img)

        for frame in range(0, 10):
            img = pygame.image.load('img/player_jump_00{}.png'.format(frame)).convert_alpha()
            self.jump_right.append(img)
        for frame in range(0, 5):
            img = pygame.image.load('img/player_jump_01{}.png'.format(frame)).convert_alpha()
            self.jump_right.append(img)

        for frame in range(0, 10):
            img = pygame.image.load('img/player_falling_00{}.png'.format(frame)).convert_alpha()
            self.falling_right.append(img)

        for frame in self.dashing_right:
            self.dashing_left.append(pygame.transform.flip(frame, True, False))

        for frame in self.melee_right:
            self.melee_left.append(pygame.transform.flip(frame, True, False))

        for frame in range(0, 8):
            img = pygame.image.load('img/player_attacking_00{}.png'.format(frame)).convert_alpha()
            self.attacking_right.append(img)

        for frame in self.walking_right:
            self.walking_left.append(pygame.transform.flip(frame, True, False))

        for frame in self.idle_right:
            self.idle_left.append(pygame.transform.flip(frame, True, False))

        for frame in self.jump_right:
            self.jump_left.append(pygame.transform.flip(frame, True, False))

        for frame in self.falling_right:
            self.falling_left.append(pygame.transform.flip(frame, True, False))

        for frame in self.attacking_right:
            self.attacking_left.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        now = pygame.time.get_ticks()

        if self.dash:
            if now - self.last_update > 25:
                self.last_update = now
                if self.facing == 'right':
                    self.current_frame = (self.current_frame + 1) % len(self.dashing_right)
                    if self.current_frame < len(self.dashing_right):
                        self.image = self.dashing_right[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.dashing_left)
                    self.image = self.dashing_left[self.current_frame]

        if self.melee_atk:
            if now - self.last_update > 25:
                self.last_update = now
                if self.facing == 'right':
                    self.current_frame = (self.current_frame + 1) % len(self.melee_right)
                    if self.current_frame < len(self.melee_right):
                        self.image = self.melee_right[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.melee_left)
                    self.image = self.melee_left[self.current_frame]

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

        if self.jumping and self.change_y < 0:
            if now - self.last_update > 100:
                self.last_update = now
                if self.facing == 'right':
                    self.current_frame = (self.current_frame + 1) % len(self.jump_right)
                    self.image = self.jump_right[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.jump_left)
                    self.image = self.jump_left[self.current_frame]

        if self.jumping and self.change_y > 0:
            if now - self.last_update > 100:
                self.last_update = now
                if self.facing == 'right':
                    self.current_frame = (self.current_frame + 1) % len(self.falling_right)
                    self.image = self.falling_right[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.falling_left)
                    self.image = self.falling_left[self.current_frame]

        if self.walking and not self.jumping:
            if now - self.last_update > 50:
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

    def delay_dash(self):
        self.dash_delay = True
        pygame.time.set_timer(pygame.USEREVENT+6, 500)

    def delay_attack(self):
        self.attack_delay = True
        pygame.time.set_timer(pygame.USEREVENT+3, 1000)

    def delay_melee(self):
        self.melee_delay = True
        pygame.time.set_timer(pygame.USEREVENT+4, 500)

    def delay_dano(self):
        self.dano_delay = True
        pygame.time.set_timer(pygame.USEREVENT+2, 500)

    def update(self):
        # used to hitbox position update in level class
        self.dash_change_x = self.dash_change_x * 0.95
        self.level.dash_changes_x = self.dash_change_x
        self.level.changes_x = self.change_x
        self.level.changes_y = self.change_y
        self.level.player_pos_x = self.rect.centerx
        self.level.player_pos_y = self.rect.centery
        self.rect.x += self.dash_change_x

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

        if not self.jumping:
            self.dash_limit = False

        self.animate()
        # Gravity
        self.calc_grav()

        # Move left/right
        if not self.dash:
            self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        block_hit_list_enemy = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        heart_hit_list = pygame.sprite.spritecollide(self, self.level.heart_list, True)
        spike_hit_list = pygame.sprite.spritecollide(self, self.level.spike_list, False)

        if not self.melee_delay:
            self.level.melee_hitbox_list.empty()

        for _ in heart_hit_list:
            self.life += 100
            if self.life > 200:
                self.life = 200
                self.heart.play()

        for block1 in block_hit_list_enemy:
            if not self.dano_delay:
                self.life -= 40

            if self.change_x == 0:
                if self.rect.x < block1.rect.x:
                    self.rect.right = block1.rect.left - 1
                    if not self.dano_delay:
                        self.delay_dano()
                else:
                    self.rect.left = block1.rect.right + 1
                    if not self.dano_delay:
                        self.delay_dano()
            if self.change_x > 0:
                self.rect.right = block1.rect.left
                if not self.dano_delay:
                    self.delay_dano()
            if self.change_x < 0:
                self.rect.left = block1.rect.right
                if not self.dano_delay:
                    self.delay_dano()


        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left

            if self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

            if self.dash_change_x > 0:
                self.rect.right = block.rect.left

            if self.dash_change_x < 0:
                self.rect.left = block.rect.right

        # Move up/down
        if not self.dash:
            self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        block_hit_list_enemy = pygame.sprite.spritecollide(self, self.level.enemy_list, False)

        # Check and see if we hit anything
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        for block1 in block_hit_list_enemy:
            if block1.type == 2:
                # Reset our position based on the top/bottom of the object.
                # if self.change_y > 0:
                #     self.rect.bottom = block.rect.top
                if self.change_y < 0:
                    self.rect.top = block1.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        for _ in spike_hit_list:
            if not self.dano_delay:
                self.life -= 60
                self.delay_dano()
                self.spike.play()

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
            self.change_y = -12
        if len(enemy_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -12

    def shoot(self):
        if self.attacking and not self.attack_delay:
            self.faca_2.play()
            if self.facing == 'right':
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.level.bullet_list.add(bullet)
                self.delay_attack()
                bullet.speed = 15
                bullet.facing = 'right'
            else:
                bullet = Bullet(self.rect.left, self.rect.top)
                self.level.bullet_list.add(bullet)
                self.delay_attack()
                bullet.speed = -15
                bullet.facing = 'left'

    def melee(self):
        if self.melee_atk and not self.melee_delay:
            self.ataque_1.play()
            if self.facing == 'right':
                hitbox = MeleeHitbox(self.rect.right, self.rect.y)
                self.level.melee_hitbox_list.add(hitbox)
                self.delay_melee()
            else:
                hitbox = MeleeHitbox((self.rect.left - 50), self.rect.y)
                self.level.melee_hitbox_list.add(hitbox)
                self.delay_melee()

    def do_dash(self):
        if self.jumping:
            self.dash_limit = True
        pygame.time.set_timer(pygame.USEREVENT+5, 400)
        if self.dash:
            if self.facing == 'right':
                self.dash_change_x = 20
            else:
                self.dash_change_x = -20

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


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('img/heart.png').convert_alpha(), (60, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MeleeHitbox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 80))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 30
        self.image = pygame.transform.scale(pygame.image.load('img/faca_hitbox.png').convert_alpha(), (100, 100))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0
        self.grav = -2
        self.last_update = 0
        self.current_frame = 0
        self.right = []
        self.left = []
        self.load_img()
        self.facing = 'right'

    def load_img(self):
        for frame in range(0, 10):

            right = pygame.transform.scale(pygame.image.load('img/faca_00{}.png'.format(frame)).convert_alpha(),
                                           (100, 100))
            self.right.append(right)

        for frame in self.right:
            self.left.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        now = pygame.time.get_ticks()
        if self.facing == 'right':
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.right)
                self.image = self.right[self.current_frame]
        else:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.left)
                self.image = self.left[self.current_frame]

    def update(self):
        self.animate()
        self.speed = self.speed * 0.99
        self.rect.x += self.speed
        self.grav += 0.20
        self.rect.y += self.grav


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = pygame.Surface([width, height])
        # self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Obstacle(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, x, y, w, h):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # self.rect = pygame.Rect(x, y, w, h)
        # self.rect.x = x
        # self.rect.y = y


class Limitador(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Espinhos(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spike(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        # self.image.fill(RED)

        self.rect = self.image.get_rect()


class Aranha(pygame.sprite.Sprite):
    def __init__(self, x, y, min_y, max_y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 30
        self.pos_y_inicial = y
        # self.load_img()
        self.type = 2
        self.image = pygame.transform.scale(pygame.image.load('img/aranha.png').convert_alpha(), (100, 100))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        # self.facing = 'right'
        self.pos_y = self.rect.y
        self.change_y = 1
        self.min_y = min_y
        self.max_y = max_y
        self.min_x = 0
        self.max_x = 0
        self.action = False
        self.player_y = 0
        # self.current_frame = 0
        # self.last_update = 0

    # def load_img(self):
    #     self.walking_left = []
    #     for frame in range(0, 10):
    #         img = pygame.image.load('img/enemy_walking_00{}.png'.format(frame))
    #         self.walking_left.append(img)
    #
    #     self.walking_right = []
    #     for frame in self.walking_left:
    #         self.walking_right.append(pygame.transform.flip(frame, True, False))

    # def animate(self):
    #     now = pygame.time.get_ticks()
    #     if self.facing == 'left':
    #         if now - self.last_update > 50:
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.walking_left)
    #             self.image = self.walking_left[self.current_frame]
    #     else:
    #         if now - self.last_update > 50:
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.walking_right)
    #             self.image = self.walking_right[self.current_frame]

    def update(self):
        # self.animate()

        self.rect.y += self.change_y
        if self.action:

            # if self.rect.top < self.min_y:
            self.change_y += 0.5
            if self.rect.bottom > self.player_y:
                self.change_y = -5
        else:
            if self.rect.top > 0:
                self.change_y -= 0.2
            else:
                self.change_y = 0


class Escaravelho(pygame.sprite.Sprite):
    def __init__(self, x, y, min_x, max_x):
        super().__init__()
        self.radius = 20
        self.type = 1
        self.walking_right = []
        self.walking_left = []
        self.load_img()
        self.image = pygame.image.load('img/enemy_walking_000.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.facing = 'right'
        self.pos_x = self.rect.x
        self.change_x = 1
        self.min_x = x - 180
        self.max_x = x + 180
        self.current_frame = 0
        self.last_update = 0
        self.action = None
        self.player_x = 0
        self.player_y = 0
        self.change_y = 0

    def load_img(self):
        for frame in range(0, 10):
            img = pygame.image.load('img/enemy_walking_00{}.png'.format(frame))
            self.walking_left.append(img)

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
        self.action = None
        self.animate()
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.change_x == 1:
            self.facing = 'right'
        else:
            self.facing = 'left'


class Tocha(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('img/tocha_0.png').convert_alpha(), (20, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = 0
        self.current_frame = 0
        self.imagens = []
        self.carregar_imagens()

    def carregar_imagens(self):
        for n in range(0, 4):
            img = pygame.transform.scale(pygame.image.load('img/tocha_{}.png'.format(n)), (20, 60))
            self.imagens.append(img)

    def animacao(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.imagens)
            self.image = self.imagens[self.current_frame]

    def update(self):
        self.animacao()


class Luz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('img/luz.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Poder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('img/poder_000.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = 0
        self.current_frame = 0
        self.imagens = []
        self.carregar_imagens()

    def carregar_imagens(self):
        for n in range(0, 10):
            img = pygame.transform.scale(pygame.image.load('img/poder_00{}.png'.format(n)).convert_alpha(), (50, 50))
            self.imagens.append(img)
        for n in range(0, 10):
            img = pygame.transform.scale(pygame.image.load('img/poder_01{}.png'.format(n)).convert_alpha(), (50, 50))
            self.imagens.append(img)

    def animacao(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.imagens)
            self.image = self.imagens[self.current_frame]

    def update(self):
        self.animacao()


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tileheight
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        # self.map = TiledMap('maps/level1.tmx')
        # self.map_img = self.map.map.make_map()
        # self.map_rect = self.map_img.get_rect()

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Level(pygame.sprite.Sprite):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        pygame.sprite.Sprite.__init__(self)

        self.platform_list = pygame.sprite.Group()
        self.spike_list = pygame.sprite.Group()
        self.tocha_lista = pygame.sprite.Group()
        self.luz_lista = pygame.sprite.Group()
        self.poder_lista = pygame.sprite.Group()

        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.enemy_list = pygame.sprite.Group()
        self.limitador1_lista = pygame.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "plataforma":
                self.platform_list.add(Obstacle(tile_object.x, tile_object.y,
                                                tile_object.width, tile_object.height))
            if tile_object.name == "espinhos":
                self.spike_list.add(Espinhos(tile_object.x, tile_object.y,
                                             tile_object.width, tile_object.height))
            if tile_object.name == "escaravelho":
                self.enemy_list.add(Escaravelho(tile_object.x, tile_object.y,
                                                tile_object.width, tile_object.height))
            if tile_object.name == "limitador1":
                self.limitador1_lista.add(Limitador(tile_object.x, tile_object.y,
                                                    tile_object.width, tile_object.height))
            if tile_object.name == "aranha":
                self.enemy_list.add(Aranha(tile_object.x, tile_object.y,
                                           tile_object.width, tile_object.height))
            if tile_object.name == "tocha":
                self.tocha_lista.add(Tocha(tile_object.x, tile_object.y))

        for tocha in self.tocha_lista:
            self.luz_lista.add(Luz(tocha.rect.x - 110, tocha.rect.y - 100))

        self.image = pygame.image.load('maps/level1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.image2 = pygame.image.load('maps/level1-2.png').convert_alpha()
        self.rect2 = self.image2.get_rect()
        self.rect2.x = -2000
        self.rect2.y = 0

        self.image3 = pygame.image.load('maps/level1-3.png').convert_alpha()
        self.rect3 = self.image3.get_rect()
        self.rect3.x = -2000
        self.rect3.y = 0

        self.image4 = pygame.image.load('maps/level1-4.png').convert_alpha()
        self.rect4 = self.image4.get_rect()
        self.rect4.x = -2000
        self.rect4.y = 0

        self.enemy_hit_platform = []
        self.hits_enemy = []
        self.hits_platform = []
        self.hitbox_in_enemy = []
        self.enemy_hit_limitador = []

        self.heart_list = pygame.sprite.Group()

        self.bullet_list = pygame.sprite.Group()
        self.melee_hitbox_list = pygame.sprite.Group()

        self.player = player
        self.last_update = 0
        self.changes_x, self.changes_y = 0, 0
        self.player_pos_x, self.player_pos_y = 0, 0
        # How far this world has been scrolled left/right
        self.world_shift = 0

        self.faca_3 = pygame.mixer.Sound('sfx/faca_3.wav')
        self.faca_4 = pygame.mixer.Sound('sfx/faca_4.wav')

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.heart_list.update()
        self.platform_list.update()
        self.enemy_list.update()
        self.bullet_list.update()
        self.melee_hitbox_list.update()
        self.spike_list.update()
        self.limitador1_lista.update()

        self.tocha_lista.update()
        self.poder_lista.update()

        for bullet in self.bullet_list:
            if bullet.rect.x > SCREEN_WIDTH or bullet.rect.x < -20:
                self.bullet_list.remove(bullet)

        # hitbox get the position of the player
        for hitbox in self.melee_hitbox_list:
            hitbox.rect.x += self.changes_x
            hitbox.rect.y += self.changes_y

        self.hits_enemy = pygame.sprite.groupcollide(self.bullet_list, self.enemy_list, True, True,
                                                     pygame.sprite.collide_circle)
        self.hits_platform = pygame.sprite.groupcollide(self.platform_list, self.bullet_list, False, True)
        self.hitbox_in_enemy = pygame.sprite.groupcollide(self.melee_hitbox_list, self.enemy_list, False, True)
        self.enemy_hit_platform = pygame.sprite.groupcollide(self.enemy_list, self.platform_list, False, False)
        self.enemy_hit_limitador = pygame.sprite.groupcollide(self.enemy_list, self.limitador1_lista, False, False)

        # Se alguma faca bater em algo, toca o som
        for hit in self.hits_enemy or self.hits_platform:
            self.faca_3.play()

        # Física dos escaravelhos
        for escaravelho in self.enemy_hit_limitador:
            if escaravelho.type == 1:
                escaravelho.change_x = escaravelho.change_x * -1

        for escaravelho in self.enemy_hit_platform:
            if escaravelho.type == 1:
                escaravelho.rect.y -= 1

        # Se a aranha bate em uma plataforma, para seu movimento
        for aranha in self.enemy_hit_platform:
            if aranha.type == 2:
                aranha.change_y = -5

        for aranha in self.enemy_list:
            if aranha.type == 2:
                aranha.player_y = self.player_pos_y
                if aranha.rect.x - self.player_pos_x < 200 and self.player_pos_x < aranha.rect.x + 200:
                    aranha.action = True
                else:
                    aranha.action = False

    def draw(self, screen):
        """ Draw everything on this level. """
        # Draw the background
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.melee_hitbox_list.draw(screen)
        self.spike_list.draw(screen)
        screen.fill(BLACK)

        screen.blit(self.image4, [self.rect4.x, 0])
        screen.blit(self.image3, [self.rect3.x, 0])
        screen.blit(self.image2, [self.rect2.x, 0])
        screen.blit(self.image, [self.rect.x, 0])

        # Desenha a teia da aranha
        for aranha in self.enemy_list:
            if aranha.type == 2:
                pygame.draw.line(screen, WHITE, (aranha.rect.centerx, -500),
                                 (aranha.rect.centerx, aranha.rect.centery), 5)

        self.enemy_list.draw(screen)
        self.bullet_list.draw(screen)

        draw_HUD_bar(screen, 0, 0)
        draw_life_bar(screen, 50, 20, self.player.life)
        self.heart_list.draw(screen)
        self.poder_lista.draw(screen)

        # Draw text on the screen
        print_in_screen(screen, 'Level   1-1', 20, SCREEN_WIDTH / 2, 10)
        print_in_screen(screen, str(self.world_shift), 20, SCREEN_WIDTH - 50, 10)

        # Teste de hitbox com círculos
        # for bullet in self.bullet_list:
        #     pygame.draw.circle(screen, RED, bullet.rect.center, bullet.radius)
        # for enemy in self.enemy_list:
        #     pygame.draw.circle(screen, RED, enemy.rect.center, enemy.radius)

        self.tocha_lista.draw(screen)
        self.luz_lista.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x
        self.rect.x += shift_x
        self.rect2.x += shift_x * 0.8
        self.rect3.x += shift_x * 0.6
        self.rect4.x += shift_x * 0.4

        # Go through all the sprite lists and shift
        for heart in self.heart_list:
            heart.rect.x += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            enemy.min_x += shift_x
            enemy.max_x += shift_x
        for bullet in self.bullet_list:
            bullet.rect.x += shift_x
        for spike in self.spike_list:
            spike.rect.x += shift_x
        for hitbox in self.melee_hitbox_list:
            hitbox.rect.x += shift_x
        for limitador in self.limitador1_lista:
            limitador.rect.x += shift_x
        for tocha in self.tocha_lista:
            tocha.rect.x += shift_x
        for luz in self.luz_lista:
            luz.rect.x += shift_x
        for poder in self.poder_lista:
            poder.rect.x += shift_x

# Create platforms for the level
class Level01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)
        self.level_limit = -300

        # Array with width, height, x, and y of platform
        level = [
                [ 120, 1360,  215,   0],
                [3200,   60,    0, 705],
                [ 512,  130,  512, 577],
                [ 260,   60, 1150, 449],
                [ 257,   60, 1792, 513],
                [ 257,   60, 2305, 513],
                [ 120, 1360, 2600,   0]
                # [ 120, 1360,12100,   0],
                ]

        spikes = [
                 [360, 64, 1995, 700]
                 ]

        # Go through the array above and add platforms
        # for platform in level:
        #     block = Platform(platform[0], platform[1])
        #     block.rect.x = platform[2]
        #     block.rect.y = platform[3]
        #     block.player = self.player
        #     self.platform_list.add(block)
        #
        # for spike in spikes:
        #     block2 = Spike(spike[0], spike[1])
        #     block2.rect.x = spike[2]
        #     block2.rect.y = spike[3]
        #     self.spike_list.add(block2)

        # Enemies in the level
        # self.enemy_list.add(Escaravelho(800, 535, 600, 1000))
        # self.enemy_list.add(Escaravelho(1300, 405, 1130, 1400))
        # self.enemy_list.add(Aranha(1300, 0, 0, 405))
        # self.enemy_list.add(Aranha(1600, 0, 0, 405))

        self.heart_list.add(Heart(1900, 630))

        self.poder_lista.add(Poder(1800, 630))

# Create platforms for the level
class Level02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -200

        # Array with type of platform, and x, y location of the platform.
        level = [
                [120, 800,-200,   0],
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
                [ 10, 300,1080,-240]
                ]

        # Go through the array above and add platforms
        # for platform in level:
        #     block = Platform(platform[0], platform[1])
        #     block.rect.x = platform[2]
        #     block.rect.y = platform[3]
        #     block.player = self.player
        #     self.platform_list.add(block)

        self.enemy_list.add(Escaravelho(400, 550, 200, 450))


# Initialize joystick
pygame.joystick.init()
joysticks = []
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()


def marca():
    show_marca = True
    pygame.init()
    pygame.mouse.set_visible(False)
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    marca1 = pygame.image.load('img/marca.png').convert_alpha()
    pygame.time.set_timer(pygame.USEREVENT + 3, 2000)

    while show_marca:
        screen.blit(marca1, [0, 0])
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT+3:
                show_marca = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_marca = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    show_marca = False


marca()


def menu():
    running_menu = True

    pygame.init()
    pygame.mouse.set_visible(False)
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    pygame.mixer.music.load('msc/menu.ogg')
    pygame.mixer.music.set_volume(0.4)
    select = pygame.mixer.Sound('sfx/select1.wav')
    confirm = pygame.mixer.Sound('sfx/confirmation.wav')
    image = pygame.transform.scale(pygame.image.load('img/menu.png').convert_alpha(), (1360, 768))
    pygame.display.set_caption("Menu")

    pos_play = [272, 512]
    pos_config = [544, 512]
    pos_off = [816, 512]
    pos_light = 1
    pos_light1 = (pos_play[0] - 8, pos_play[1] - 8)
    pos_light2 = (pos_config[0] - 8, pos_config[1] - 8)
    pos_light3 = (pos_off[0] - 8, pos_off[1] - 8)

    play = pygame.transform.scale(pygame.image.load('img/play.png').convert_alpha(), (150, 150))
    config = pygame.transform.scale(pygame.image.load('img/config.png').convert_alpha(), (150, 150))
    turn_off = pygame.transform.scale(pygame.image.load('img/quit.png').convert_alpha(), (150, 150))
    light = pygame.transform.scale(pygame.image.load('img/light.png').convert_alpha(), (170, 170))

    pygame.mixer.music.play(loops=-1)

    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    running_menu = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if pos_light > 1:
                        pos_light -= 1
                        select.play()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if pos_light < 3:
                        pos_light += 1
                        select.play()
                if event.key == pygame.K_SPACE:
                    if pos_light == 1:
                        confirm.play()
                        running_menu = False
                        pygame.mixer_music.stop()
                    if pos_light == 3:
                        confirm.play()
                        pygame.quit()
                        quit()

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if pos_light == 1:
                        confirm.play()
                        running_menu = False
                        pygame.mixer_music.stop()
                    if pos_light == 3:
                        confirm.play()
                        pygame.quit()
                        quit()

        # Joystick analog:
        joystick_count = pygame.joystick.get_count()
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            for i in range(2):
                axis = joystick.get_axis(i)
                if i == 0 and axis > 0.2:
                    if pos_light < 3:
                        pos_light += 1
                        select.play()
                if i == 0 and axis < -0.2:
                    if pos_light > 1:
                        pos_light -= 1
                        select.play()

            # Joystick arrows:
            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            # First one: 1 for right and -1 for left
            # Second one: 1 for up and -1 for down
            hats = joystick.get_numhats()

            for i in range(hats):
                hat = joystick.get_hat(i)
                if hat == (1, 0):
                    if pos_light < 3:
                        pos_light += 1
                        select.play()
                if hat == (-1, 0):
                    if pos_light > 1:
                        pos_light -= 1
                        select.play()

        screen.blit(image, [0, 0])
        screen.blit(play, pos_play)
        screen.blit(config, pos_config)
        screen.blit(turn_off, pos_off)

        if pos_light == 1:
            screen.blit(light, pos_light1)
        elif pos_light == 2:
            screen.blit(light, pos_light2)
        elif pos_light == 3:
            screen.blit(light, pos_light3)

        clock.tick(10)

        pygame.display.flip()


menu()


def main():
    """ Main Program """
    pygame.init()


    # screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Super Hero Mummy: Ramsés")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = [Level01(player), Level02(player)]

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()

    player.level = current_level
    player.rect.x = 628
    player.rect.y = 600

    active_sprite_list.add(player)

    pygame.mouse.set_visible(False)

    # Loop until the user clicks the close button.
    done = False

    pygame.mixer.music.load('msc/stage.ogg')
    pygame.mixer.music.play(loops=-1)

    # -------- Main Program Loop -----------
    while not done:
        if player.life <= 0:
            done = True

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
                if event.key == pygame.K_e and not player.dash:
                    player.melee_atk = True
                    player.melee()
                if event.key == pygame.K_r and not player.melee_atk:
                    if player.dash_change_x == 0:
                        player.dash = True
                        player.do_dash()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d and player.change_x > 0:
                    player.stop()

            # Joystick buttons:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    player.jump()
                if event.button == 1 and not player.melee_atk and not player.dash_delay and not player.dash_limit:
                    player.dash = True
                    player.do_dash()
                    player.delay_dash()
                if event.button == 2 and not player.dash:
                    player.melee_atk = True
                    player.melee()
                if event.button == 3:
                    player.attacking = True
                    pygame.time.set_timer(pygame.USEREVENT + 1, 500)
                    player.shoot()

            if event.type == pygame.USEREVENT+1:
                player.attacking = False
            if event.type == pygame.USEREVENT+2:
                player.dano_delay = False
            if event.type == pygame.USEREVENT+3:
                player.attack_delay = False
            if event.type == pygame.USEREVENT+4:
                player.melee_atk = False
                player.melee_delay = False
            if event.type == pygame.USEREVENT+5:
                player.dash = False
                player.dash_change_x = 0
            if event.type == pygame.USEREVENT+6:
                player.dash_delay = False

        # Joystick analog:
        joystick_count = pygame.joystick.get_count()
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            for i in range(2):
                axis = joystick.get_axis(i)
                if i == 0 and -0.4 < axis < 0.4:
                    player.stop()
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
        if player.rect.right >= 906:
            diff = player.rect.right - 906
            player.rect.right = 906
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 453:
            diff = 453 - player.rect.left
            player.rect.left = 453
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

    pygame.quit()


main()
