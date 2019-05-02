import pygame

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
def print_in_screen(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_life_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 200
    BAR_HEIGHT = 20
    fill = (pct / 200) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


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
        # List of sprites we can bump against
        self.level = None
        self.life = 200
        self.dano_delay = False
        self.attack_delay = False
        self.spike = pygame.mixer.Sound('sfx/spike_hit.wav')
        self.heart = pygame.mixer.Sound('sfx/heart.wav')

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

    def delay_attack(self):
        self.attack_delay = True
        pygame.time.set_timer(pygame.USEREVENT+5, 1000)

    def delay_dano(self):
        self.dano_delay = True
        pygame.time.set_timer(pygame.USEREVENT+2, 500)

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
        heart_hit_list = pygame.sprite.spritecollide(self, self.level.heart_list, True)
        spike_hit_list = pygame.sprite.spritecollide(self, self.level.spike_list, False)

        for heart in heart_hit_list:
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

        # Move up/down
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

        for block2 in spike_hit_list:
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
            self.change_y = -10
        if len(enemy_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def shoot(self):
        if self.attacking and not self.attack_delay:
            if self.facing == 'right':
                bullet = Bullet(self.rect.right, self.rect.centery)
                self.level.bullet_list.add(bullet)
                self.delay_attack()
                bullet.speed = 10
            else:
                bullet = Bullet(self.rect.left, self.rect.centery)
                self.level.bullet_list.add(bullet)
                self.delay_attack()
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


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('img/heart.png').convert_alpha(), (60, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0
        self.grav = 0

    def update(self):
        self.speed = self.speed * 0.99
        self.rect.x += self.speed
        self.grav += 0.15
        self.rect.y += self.grav


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


class Spike(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        # self.image.fill(RED)

        self.rect = self.image.get_rect()


class Aranha(pygame.sprite.Sprite):
    def __init__(self, x, y, min_y, max_y):
        pygame.sprite.Sprite.__init__(self)

        # self.load_img()
        self.image = pygame.transform.scale(pygame.image.load('img/aranha.png').convert_alpha(), (100, 100))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.facing = 'right'
        self.pos_y = self.rect.y
        self.change_y = 5
        self.min_y = min_y
        self.max_y = max_y
        self.min_x = 0
        self.max_x = 0
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
        if self.rect.top < self.min_y:
            self.change_y = 5
        if self.rect.bottom > self.max_y:
            self.change_y = -3


class Escaravelho(pygame.sprite.Sprite):
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
        self.image = pygame.image.load('img/level 1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.heart_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.spike_list = pygame.sprite.Group()
        self.player = player

        # How far this world has been scrolled left/right
        self.world_shift = 0

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.heart_list.update()
        self.platform_list.update()
        self.enemy_list.update()
        self.bullet_list.update()
        self.spike_list.update()
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
        self.spike_list.draw(screen)
        screen.blit(self.image, [self.rect.x, 0])
        self.enemy_list.draw(screen)
        self.bullet_list.draw(screen)
        draw_life_bar(screen, 50, 50, self.player.life)
        self.heart_list.draw(screen)
        # Draw text on the screen
        print_in_screen(screen, 'Level 1', 100, SCREEN_WIDTH / 2, 50)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x
        self.rect.x += shift_x
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
                [ 120, 1360,  215,   0],
                [3200,   60,    0, 710],
                [ 512,  130,  512, 580],
                [ 260,   60, 1150, 452],
                [ 257,   60, 1792, 516],
                [ 257,   60, 2305, 516],
                [ 120, 1360, 2600,   0]
                # [ 120, 1360,12100,   0],
                ]

        spikes = [
                 [380, 64, 1985, 700]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        for spike in spikes:
            block2 = Spike(spike[0], spike[1])
            block2.rect.x = spike[2]
            block2.rect.y = spike[3]
            self.spike_list.add(block2)

        #Enemies in the level
        self.enemy_list.add(Escaravelho(800, 535, 600, 1000))
        self.enemy_list.add(Escaravelho(1300, 405, 1130, 1400))
        self.enemy_list.add(Aranha(1300, 0, 0, 405))

        self.heart_list.add(Heart(1900, 630))


# Create platforms for the level
class Level_02(Level):
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
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        self.enemy_list.add(Escaravelho(400, 550, 200, 450))


# Initiallize joystick
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
                        running_menu = False
                        pygame.mixer_music.stop()
                    if pos_light == 3:
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
        # Print_in_screen(screen, 'Aperte "i" para iniciar ou "Esc" para sair', 20, SCREEN_WIDTH / 2, 730)
        # Update the screen with what we've drawn.
        pygame.display.flip()


menu()


def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d and player.change_x > 0:
                    player.stop()

            # Joystick buttons:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0 or event.button == 1:
                    player.jump()
                if event.button == 2 or event.button == 3:
                    player.attacking = True
                    pygame.time.set_timer(pygame.USEREVENT+1, 500)
                    player.shoot()

            if event.type == pygame.USEREVENT + 1:
                player.attacking = False

            if event.type == pygame.USEREVENT+2:
                player.dano_delay = False

            if event.type == pygame.USEREVENT+5:
                player.attack_delay = False


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
        if player.rect.right >= 680:
            diff = player.rect.right - 680
            player.rect.right = 680
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 340:
            diff = 340 - player.rect.left
            player.rect.left = 340
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
