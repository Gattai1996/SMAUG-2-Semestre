import pygame
import pytmx
from os import path
from random import *

BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = (  0, 255,   0)
RED    = (255,   0,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)
GRAY   = (125, 125, 125)
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
font_name = pygame.font.match_font('princeofpersia')
load_game = True


def print_in_screen(surf, text, tamanho, x, y, color):
    font = pygame.font.Font(font_name, tamanho)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_life_bar(surf, x, y, width, height, color, life):
    if life < 0:
        life = 0
    bar_length = width
    bar_height = height
    fill = (life / width) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, GRAY, outline_rect)
    pygame.draw.rect(surf, color, fill_rect)


def draw_HUD_bar(surf, x, y):
    HUD_length = SCREEN_WIDTH
    HUD_height = 60
    HUD = pygame.Rect(x, y, HUD_length, HUD_height)
    pygame.draw.rect(surf, BLACK, HUD)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Listas de imagens
        self.enemy_hit_list = []
        self.enemy_hit_list = []
        self.heart_hit_list = []
        self.spike_hit_list = []
        self.platform_hit_list = []
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
        self.tocando_porta = []
        self.load_img()
        self.image = self.idle_right[0]
        self.rect = self.image.get_rect()
        self.pos_ini_x = 0
        self.pos_ini_y = 0
        self.radius = 25
        self.change_x = 0
        self.change_y = 0
        self.change_x2 = 0
        self.change_y2 = 0
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
        self.porta = False
        self.apertando_cima = False
        self.apertando_baixo = False
        self.wall_jump_direita = False
        self.wall_jump_esquerda = False
        self.life = 200
        self.power = 10
        self.item = 'faca'
        self.dano_delay = False
        self.attack_delay = False
        self.melee_delay = False
        self.tomando_dano = False
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

        if self.attacking and self.power > 0 and not self.attack_delay:
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
        if self.tomando_dano:
            self.stop()
        self.change_x2 = self.change_x2 * 0.95
        self.change_y2 = self.change_y2 * 0.95
        self.dash_change_x = self.dash_change_x * 0.95
        self.level.dash_changes_x = self.dash_change_x
        self.level.changes_x = self.change_x
        self.level.changes_y = self.change_y
        self.level.player_pos_x = self.rect.centerx
        self.level.player_pos_y = self.rect.centery
        self.rect.x += self.dash_change_x

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

        self.calc_grav()

        self.rect.x += self.change_x2
        self.rect.x += self.change_x

        self.platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False,
                                                          pygame.sprite.collide_circle)
        self.heart_hit_list = pygame.sprite.spritecollide(self, self.level.heart_list, True)
        self.poder_hit_list = pygame.sprite.spritecollide(self, self.level.poder_lista, True)
        self.spike_hit_list = pygame.sprite.spritecollide(self, self.level.spike_list, False)
        self.hitbox_enemy = pygame.sprite.spritecollide(self, self.level.hitbox_attack_inimigo, False,
                                                        pygame.sprite.collide_circle)
        self.tocando_porta = pygame.sprite.spritecollide(self, self.level.porta_lista, False)

        for porta in self.tocando_porta:
            self.porta = True

        if not self.melee_delay:
            self.level.melee_hitbox_list.empty()

        for heart in self.heart_hit_list:
            self.heart.play()
            self.life += 100
            if self.life > 200:
                self.life = 200

        for poder in self.poder_hit_list:
            self.heart.play()
            self.power += 3
            if self.power > 10:
                self.power = 10

        for enemy in self.enemy_hit_list:
            if enemy.ativo:
                if self.dash_change_x > 0:
                    self.dash_delay = False
                    self.dash = False
                    self.dash_change_x = 0
                    self.rect.right = enemy.rect.left
                elif self.dash_change_x < 0:
                    self.dash_delay = False
                    self.dash = False
                    self.dash_change_x = 0
                    self.rect.right = enemy.rect.right
                if not self.dano_delay:
                    self.stop()
                    self.dano()
                    self.delay_dano()
                    self.life -= 40

                if not self.dano_delay:
                    self.life -= 40

                if self.change_x == 0:
                    if self.rect.x < enemy.rect.x:
                        # self.rect.right = block1.rect.left - 1
                        if not self.dano_delay:
                            self.dano()
                            self.delay_dano()
                    else:
                        # self.rect.left = block1.rect.right + 1
                        if not self.dano_delay:
                            self.dano()
                            self.delay_dano()
                if self.change_x > 0:
                    # self.rect.right = block1.rect.left
                    if not self.dano_delay:
                        self.dano()
                        self.delay_dano()
                if self.change_x < 0:
                    # self.rect.left = block1.rect.right
                    if not self.dano_delay:
                        self.dano()
                        self.delay_dano()

        # Wall jump
        for platform in self.platform_hit_list:
            if platform.type == 1:
                if self.change_x > 0:
                    self.rect.right = platform.rect.left

                    if self.change_y < 0:
                        if self.facing == 'right' and not self.wall_jump_direita:
                            self.facing = 'left'
                            self.change_y = -20
                            self.wall_jump_direita = True
                            self.wall_jump_esquerda = False

                elif self.change_x < 0:
                    self.rect.left = platform.rect.right

                    if self.change_y < 0:
                        if self.facing == 'left' and not self.wall_jump_esquerda:
                            self.facing = 'right'
                            self.change_y = -20
                            self.wall_jump_esquerda = True
                            self.wall_jump_direita = False

                if self.dash_change_x > 0:
                    self.rect.right = platform.rect.left
                elif self.dash_change_x < 0:
                    self.rect.left = platform.rect.right

                if self.change_x2 > 0:
                    self.rect.right = platform.rect.left
                elif self.change_x2 < 0:
                    self.rect.left = platform.rect.right

        if self.change_y >= 0 and not self.jumping:
            self.wall_jump_direita = False
            self.wall_jump_esquerda = False

        if not self.dash:
            self.rect.y += self.change_y
            self.rect.y += self.change_y2
        self.platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # block_hit_list_enemy = pygame.sprite.spritecollide(self, self.level.enemy_list, False)

        for platform in self.platform_hit_list:
            if platform.type == 1:
                if self.change_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.jumping = False
                elif self.change_y < 0:
                    self.rect.top = platform.rect.bottom

                if self.change_y2 > 0:
                    self.rect.bottom = platform.rect.top
                    self.jumping = False

                self.change_y = 0
                self.jumping = False

            elif platform.type == 2 and not self.apertando_baixo:
                if self.rect.y + 126 < platform.rect.y + 50 and self.change_y > 0:
                    if self.change_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.jumping = False
                    # elif self.change_y < 0:
                    #     self.rect.top = platform.rect.bottom
                    if self.change_y2 > 0:
                        self.rect.bottom = platform.rect.top
                        self.jumping = False

                    self.change_y = 0
                    self.jumping = False

        for spike in self.spike_hit_list:
            if not self.dano_delay:
                # self.life -= 60
                self.delay_dano()
                self.spike.play()
                self.life -= 40

        for hitbox in self.hitbox_enemy:
            if not self.dano_delay:
                # self.life -= 60
                self.delay_dano()
                self.dano()

    def dano(self):
        self.tomando_dano = True
        self.change_y = 0
        self.change_x = 0
        if self.facing == 'right':
            self.change_x2 += -8
            self.change_y2 += -6
        else:
            self.change_x2 += 8
            self.change_y2 += -6

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 4
        else:
            self.change_y += 1.3

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 4
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        self.rect.y -= 4
        self.jumping = True

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -24

        if len(enemy_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -24

    def shoot(self):
        if not self.attack_delay:
            if self.item == 'faca':
                if self.power > 0 and self.attacking:
                    self.power -= 1
                    self.faca_2.play()
                    if self.facing == 'right':
                        faca = Faca(self.rect.centerx, self.rect.top)
                        self.level.faca_lista.add(faca)
                        self.delay_attack()
                        faca.speed = 20
                        faca.facing = 'right'
                    else:
                        faca = Faca(self.rect.left, self.rect.top)
                        self.level.faca_lista.add(faca)
                        self.delay_attack()
                        faca.speed = -20
                        faca.facing = 'left'

    def melee(self):
        if self.melee_atk and not self.melee_delay:
            self.ataque_1.play()
            if self.facing == 'right':
                hitbox = Hit_Box(self.rect.centerx, self.rect.y, 60, 80, self)
                self.level.melee_hitbox_list.add(hitbox)
                self.delay_melee()
            else:
                hitbox = Hit_Box((self.rect.centerx - 30), self.rect.y, 60, 80, self)
                self.level.melee_hitbox_list.add(hitbox)
                self.delay_melee()

    def do_dash(self):
        if self.jumping:
            self.dash_limit = True
        pygame.time.set_timer(pygame.USEREVENT+5, 400)
        if self.dash:
            self.change_x = 0
            if self.facing == 'right':
                self.dash_change_x += 40
            else:
                self.dash_change_x += -40

    def go_left(self):
        if not self.wall_jump_esquerda:
            self.facing = 'left'
            self.change_x = -12

    def go_right(self):
        if not self.wall_jump_direita:
            self.facing = 'right'
            self.change_x = 12

    def stop(self):
        self.change_x = 0

    def cima(self):
        self.apertando_cima = True
        pygame.time.set_timer(pygame.USEREVENT - 2, 100)

    def baixo(self):
        self.apertando_baixo = True
        pygame.time.set_timer(pygame.USEREVENT - 3, 500)


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, h, w):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('img/heart.png').convert_alpha(), (60, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Poder(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
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


class Hit_Box(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, dono):
        pygame.sprite.Sprite.__init__(self)
        self.dono = dono
        self.radius = 40
        self.image = pygame.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.life = 0


class Hit_Box_Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, dono):
        pygame.sprite.Sprite.__init__(self)
        self.dono = dono
        self.radius = 30
        self.image = pygame.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.life = 0


class Faca(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 30
        self.image = pygame.transform.scale(pygame.image.load('img/faca_hitbox.png').convert_alpha(), (100, 100))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0
        self.grav = -6
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
        self.grav += 0.8
        self.rect.y += self.grav


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.type = 0
        self.image = pygame.Surface([width, height])
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = w
        self.height = h


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
        self.life = 1
        self.delay_dano = False
        self.radius = 40
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
        self.player_x = 0
        # self.current_frame = 0
        # self.last_update = 0
        self.die = False
        self.frame = 0
        self.ativo = True

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
        if self.player_x - self.rect.x < SCREEN_WIDTH:
            # self.animate()
            self.rect.y += self.change_y
            if self.action:
                self.change_y += 2
                if self.rect.bottom > self.player_y + 100:
                    self.change_y = -10
            else:
                if self.rect.top > 0:
                    self.change_y -= 0.8
                else:
                    self.change_y = 0
            if self.rect.y > SCREEN_HEIGHT:
                self.rect.y = SCREEN_HEIGHT

        if self.die:
            self.kill()

    def dano_delay(self):
        pass


class Escaravelho(pygame.sprite.Sprite):
    def __init__(self, x, y, min_x, max_x):
        super().__init__()
        self.life = 1
        self.delay_dano = False
        self.radius = 25
        self.type = 1
        self.walking_right = []
        self.walking_left = []
        self.die_right = []
        self.die_left =  []
        self.load_img()
        self.image = pygame.image.load('img/enemy_walking_000.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.facing = 'right'
        self.pos_x = self.rect.x
        self.change_x = 2
        self.min_x = x - 180
        self.max_x = x + 180
        self.current_frame = 0
        self.last_update = 0
        self.action = None
        self.player_x = 0
        self.player_y = 0
        self.change_y = 0
        self.die = False
        self.frame = 0
        self.ativo = True

    def load_img(self):
        for frame in range(0, 10):
            img = pygame.image.load('img/enemy_walking_00{}.png'.format(frame))
            self.walking_left.append(img)

        for frame in self.walking_left:
            self.walking_right.append(pygame.transform.flip(frame, True, False))

        for frame in range(0, 7):
            img = pygame.image.load('img/enemy_die_00{}.png'.format(frame))
            self.die_left.append(img)

        for frame in self.die_left:
            self.die_right.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        if self.ativo:
            now = pygame.time.get_ticks()
            if not self.die:
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
            else:
                self.rect.y += 2
                if self.facing == 'left':
                    if now - self.last_update > 25:
                        self.last_update = now
                        self.frame += 1
                        if self.frame == len(self.die_left):
                            self.ativo = False

                        else:
                            if self.last_update > 25:
                                self.image = self.die_left[self.frame]
                else:
                    if now - self.last_update > 25:
                        self.last_update = now
                        self.frame += 1
                        if self.frame == len(self.die_right):
                            self.ativo = False

                        else:
                            if self.last_update > 25:
                                self.image = self.die_right[self.frame]

    def update(self):
        if not self.ativo and self.player_x - self.rect.x > SCREEN_WIDTH\
                or not self.ativo and self.rect.x - self.player_x > SCREEN_WIDTH:
            self.kill()
        self.animate()
        if not self.die and self.player_x - self.rect.x < SCREEN_WIDTH:
            self.action = None

            self.rect.x += self.change_x
            self.rect.y += self.change_y
            if self.change_x == 2:
                self.facing = 'right'
            else:
                self.facing = 'left'

    def dano_delay(self):
        pass


class Esqueleto(pygame.sprite.Sprite):
    def __init__(self, x, y, min_x, max_x):
        super().__init__()
        self.idle_right = []
        self.idle_left = []
        self.walking_right = []
        self.walking_left = []
        self.attack_right = []
        self.attack_left = []
        self.hit_right = []
        self.hit_left = []
        self.die_right = []
        self.die_left = []
        self.idle = True
        self.walking = False
        self.attack = False
        self.hit = False
        self.die = False
        self.delay_attack = False
        self.delay_dano = False
        self.radius = 30
        self.type = 3
        self.life = 100
        self.load_img()
        self.image = pygame.transform.scale(pygame.image.load('img/skeleton_idle_000.png').convert(), (80, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.facing = 'left'
        self.pos_x = self.rect.x
        self.change_x = 0
        self.change_y = 0
        self.player_x = 0
        self.player_y = 0
        self.min_x = 0
        self.max_x = 0
        self.current_frame = 0
        self.last_update = 0
        self.action = False
        self.mostrar_barra = False
        self.ativo = True
        self.frame = 0

    def load_img(self):
        for frame in range(0, 10):
            img = pygame.transform.scale(pygame.image.load('img/skeleton_idle_00{}.png'.format(frame)). convert_alpha(), (80, 105))
            self.idle_right.append(img)
        for frame in range(0, 5):
            img = pygame.transform.scale(pygame.image.load('img/skeleton_idle_01{}.png'.format(frame)). convert_alpha(), (80, 105))
            self.idle_right.append(img)
        for frame in self.idle_right:
            self.idle_left.append(pygame.transform.flip(frame, True, False))

        for frame in range(0, 10):
            img = pygame.transform.scale(pygame.image.load('img/skeleton_walking_00{}.png'.format(frame)). convert_alpha(), (100, 105))
            self.walking_right.append(img)
        for frame in range(0, 5):
            img = pygame.transform.scale(pygame.image.load('img/skeleton_walking_01{}.png'.format(frame)). convert_alpha(), (100, 105))
            self.walking_right.append(img)
        for frame in self.walking_right:
            self.walking_left.append(pygame.transform.flip(frame, True, False))

        for frame in range(0, 8):
            img = pygame.transform.scale(pygame.image.load('img/skeleton_attack_00{}.png'.format(frame)). convert_alpha(), (140, 115))
            self.attack_right.append(img)
        for frame in self.attack_right:
            self.attack_left.append(pygame.transform.flip(frame, True, False))

        for frame in range(0, 10):
            img = pygame.transform.scale(pygame.image.load('img/skeleton_hit_00{}.png'.format(frame)). convert_alpha(), (120, 100))
            self.hit_right.append(img)
        for frame in range(0, 5):
            img = pygame.transform.scale(pygame.image.load('img/skeleton_hit_01{}.png'.format(frame)). convert_alpha(), (120, 100))
            self.hit_right.append(img)
        for frame in self.hit_right:
            self.hit_left.append(pygame.transform.flip(frame, True, False))

        for frame in range(0, 10):
            img = pygame.transform.scale(pygame.image.load('img/skeleton_die_00{}.png'.format(frame)). convert_alpha(), (140, 115))
            self.die_right.append(img)
        for frame in self.die_right:
            self.die_left.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        if self.ativo:
            now = pygame.time.get_ticks()
            if self.idle:
                if self.facing == 'left':
                    if now - self.last_update > 50:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.idle_left)
                        self.image = self.idle_left[self.current_frame]
                else:
                    if now - self.last_update > 50:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.idle_right)
                        self.image = self.idle_right[self.current_frame]
            if self.walking:
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
            if self.attack:
                if self.facing == 'left':
                    if now - self.last_update > 80:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.attack_left)
                        self.image = self.attack_left[self.current_frame]
                else:
                    if now - self.last_update > 80:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.attack_right)
                        self.image = self.attack_right[self.current_frame]
            if self.hit:
                if self.facing == 'left':
                    if now - self.last_update > 30:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.hit_left)
                        self.image = self.hit_left[self.current_frame]
                else:
                    if now - self.last_update > 50:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.hit_right)
                        self.image = self.hit_right[self.current_frame]
            if self.die:
                if self.facing == 'left':
                    if now - self.last_update > 50:
                        self.last_update = now
                        self.frame += 1
                        if self.frame == len(self.die_left):
                            self.ativo = False
                        else:
                            if self.last_update > 50:
                                self.image = self.die_left[self.frame]
                else:
                    if now - self.last_update > 50:
                        self.last_update = now
                        self.frame += 1
                        if self.frame == len(self.die_right):
                            self.ativo = False
                        else:
                            if self.last_update > 50:
                                self.image = self.die_right[self.frame]

    def update(self):
        if self.ativo and self.player_x - self.rect.x < SCREEN_WIDTH:
            self.animate()
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            if not self.delay_attack and not self.delay_dano:
                if self.action:
                    self.idle = False
                    self.walking = True
                    if self.facing == 'right':
                        self.change_x = 2
                    else:
                        self.change_x = -2
                else:
                    self.walking = False
                    self.idle = True
                    self.change_x = 0
            else:
                self.walking = False
                self.change_x = 0

    def dano_delay(self):
        self.idle = False
        self.hit = True
        self.walking = False
        self.attack = False
        self.delay_dano = True
        self.mostrar_barra = True
        pygame.time.set_timer(pygame.USEREVENT + 7, 500)

    def attack_delay(self):
        self.idle = False
        self.walking = False
        self.attack = True
        self.delay_attack = True
        pygame.time.set_timer(pygame.USEREVENT - 1, 500)


class HighLight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('img/high_light_000.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = 0
        self.current_frame = 0
        self.imagens = []
        self.carregar_imagens()

    def carregar_imagens(self):
        for n in range(0, 10):
            img = pygame.transform.scale(pygame.image.load('img/high_light_00{}.png'.format(n)), (100, 100))
            self.imagens.append(img)
        for n in range(0, 5):
            img = pygame.transform.scale(pygame.image.load('img/high_light_00{}.png'.format(n)), (100, 100))
            self.imagens.append(img)

    def animacao(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.imagens)
            self.image = self.imagens[self.current_frame]

    def update(self):
        self.animacao()


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


class Porta(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.rect.x = x
        self.rect.y = y


class Level(pygame.sprite.DirtySprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        # Adiciona os grupos de sprites em listas
        self.platform_list = pygame.sprite.Group()
        self.spike_list = pygame.sprite.Group()
        self.heart_list = pygame.sprite.Group()
        self.faca_lista = pygame.sprite.Group()
        self.melee_hitbox_list = pygame.sprite.Group()
        self.hitbox_attack_inimigo = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.limitador1_lista = pygame.sprite.Group()
        self.tocha_lista = pygame.sprite.Group()
        self.luz_lista = pygame.sprite.Group()
        self.poder_lista = pygame.sprite.Group()
        self.porta_lista = pygame.sprite.Group()
        self.enemy_hit_platform = []
        self.hits_enemy = []
        self.hits_platform = []
        self.hitbox_in_enemy = []
        self.enemy_hit_limitador = []
        self.player = player
        self.last_update = 0
        self.changes_x, self.changes_y = 0, 0
        self.player_pos_x, self.player_pos_y = 0, 0
        self.world_shift = 0
        self.faca_3 = pygame.mixer.Sound('sfx/faca_3.wav')
        self.faca_4 = pygame.mixer.Sound('sfx/faca_4.wav')
        self.level_no = 0

    def update(self):
        self.heart_list.update()
        self.platform_list.update()
        self.enemy_list.update()
        self.faca_lista.update()
        self.melee_hitbox_list.update()
        self.hitbox_attack_inimigo.update()
        self.spike_list.update()
        self.limitador1_lista.update()
        self.tocha_lista.update()
        self.luz_lista.update()
        self.poder_lista.update()
        self.porta_lista.update()

        for faca in self.faca_lista:
            if faca.rect.x > SCREEN_WIDTH or faca.rect.x < -20:
                self.faca_lista.remove(faca)
            if faca.rect.y > SCREEN_HEIGHT + 50 or faca.rect.y < 0:
                self.faca_lista.remove(faca)

        for hitbox in self.melee_hitbox_list:
            hitbox.rect.x += self.changes_x
            hitbox.rect.y += self.changes_y

        self.hits_enemy = pygame.sprite.groupcollide(self.enemy_list, self.faca_lista, False, True,
                                                     pygame.sprite.collide_circle)
        self.hitbox_in_enemy = pygame.sprite.groupcollide(self.enemy_list, self.melee_hitbox_list, False, False,
                                                          pygame.sprite.collide_circle)
        self.enemy_hit_platform = pygame.sprite.groupcollide(self.enemy_list, self.platform_list, False, False)
        self.enemy_hit_limitador = pygame.sprite.groupcollide(self.enemy_list, self.limitador1_lista, False, False)

        for hit in self.hits_enemy:
            self.faca_3.play()

        for enemy in self.hits_enemy or self.hitbox_in_enemy:
            if not enemy.delay_dano:
                enemy.life -= randint(15, 30)
                enemy.dano_delay()

        for enemy in self.enemy_list:
            if not enemy.life > 0:
                enemy.die = True

        # for enemy in self.enemy_list:
        #     if not enemy.life > 0:
        #         self.enemy_list.remove(enemy)

        # Lógica dos escaravelhos e esqueletos é ativada ao encostar em um limitador do arquivo tmx
        for enemy in self.enemy_hit_limitador:
            if enemy.type == 1:
                enemy.change_x = enemy.change_x * -1
            if enemy.type == 3:
                if enemy.facing == 'right':
                    enemy.change_x = -2
                else:
                    enemy.change_x = 2

        # Corrige inimigos "enterrados" nas plataformas
        for enemy in self.enemy_hit_platform:
            if enemy.type == 1 and enemy.ativo:
                enemy.rect.y -= 1
            if enemy.type == 3:
                enemy.rect.y -= 1

        for escaravelho in self.enemy_list:
            if escaravelho.type == 1:
                escaravelho.player_x = self.player_pos_x
                escaravelho.player_y = self.player_pos_y
        # Se a aranha bate em uma plataforma, para seu movimento
        for aranha in self.enemy_hit_platform:
            if aranha.type == 2:
                aranha.change_y = -5

        for aranha in self.enemy_list:
            if aranha.type == 2:
                aranha.player_y = self.player_pos_y
                aranha.player_x = self.player_pos_x
                if aranha.rect.x - self.player_pos_x < 200 and self.player_pos_x < aranha.rect.x + 200:
                    aranha.action = True
                else:
                    aranha.action = False

        for esqueleto in self.enemy_list:
            if esqueleto.type == 3:
                esqueleto.player_x = self.player_pos_x
                esqueleto.player_y = self.player_pos_y
                if esqueleto.rect.x < self.player_pos_x:
                    esqueleto.facing = 'right'
                else:
                    esqueleto.facing = 'left'

                if not esqueleto.delay_attack:
                    self.hitbox_attack_inimigo.empty()

                if esqueleto.facing == 'left':
                    if esqueleto.rect.x - self.player_pos_x < 20 and self.player_pos_x < esqueleto.rect.x + 150\
                       and esqueleto.rect.y - self.player_pos_y < 50 and self.player_pos_y < esqueleto.rect.y + 50:
                        esqueleto.idle = False
                        esqueleto.walking = False
                        esqueleto.change_x = 0
                        esqueleto.attack = True
                        esqueleto.attack_delay()
                        self.hitbox_attack_inimigo.add(Hit_Box_Inimigo(esqueleto.rect.x, esqueleto.rect.y, 60, 60, esqueleto))
                else:
                    if esqueleto.rect.x - self.player_pos_x < 20 and self.player_pos_x < esqueleto.rect.x + 100\
                       and esqueleto.rect.y - self.player_pos_y < 50 and self.player_pos_y < esqueleto.rect.y + 50:
                        esqueleto.idle = False
                        esqueleto.walking = False
                        esqueleto.change_x = 0
                        esqueleto.attack = True
                        esqueleto.attack_delay()
                        self.hitbox_attack_inimigo.add(Hit_Box_Inimigo(esqueleto.rect.right, esqueleto.rect.y, 60, 60, esqueleto))

                if esqueleto.rect.x - self.player_pos_x < 600 and self.player_pos_x < esqueleto.rect.x + 600\
                   and esqueleto.rect.y - self.player_pos_y < 80 and self.player_pos_y < esqueleto.rect.y + 80:
                    esqueleto.action = True
                else:
                    esqueleto.action = False

                if esqueleto.die:
                    esqueleto.action = False
                    esqueleto.idle = False
                    esqueleto.walking = False
                    esqueleto.attack = False
                    esqueleto.hit = False

    def draw(self, screen):
        self.platform_list.draw(screen)
        self.melee_hitbox_list.draw(screen)
        self.hitbox_attack_inimigo.draw(screen)
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
        self.faca_lista.draw(screen)

        draw_HUD_bar(screen, 0, 0)
        draw_life_bar(screen, 50, 20, 200, 20, GREEN, self.player.life)

        for enemy in self.enemy_list:
            if enemy.type == 3 and enemy.mostrar_barra:
                draw_life_bar(screen, enemy.rect.x, enemy.rect.y, 100, 10, RED, enemy.life)

        print_in_screen(screen, 'Level   1-1', 20, SCREEN_WIDTH / 2, 10, WHITE)
        print_in_screen(screen, str(self.player.power), 20, SCREEN_WIDTH - 50, 10, WHITE)

        # print_in_screen(screen, str(self.player.dano_delay), 20, 1000, 100)
        # print_in_screen(screen, str(self.world_shift), 20, SCREEN_WIDTH - 50, 100)
        # Teste de hitbox com círculos
        # for hitbox in self.melee_hitbox_list:
        #     pygame.draw.circle(screen, RED, hitbox.rect.center, hitbox.radius)
        #     # pygame.draw.rect(screen, RED, hitbox.rect)
        # for hitbox2 in self.hitbox_attack_inimigo:
        #     pygame.draw.circle(screen, RED, hitbox2.rect.center, hitbox2.radius)
        # for faca in self.faca_lista:
        #     pygame.draw.circle(screen, RED, faca.rect.center, faca.radius)
        # for enemy in self.enemy_list:
        #     pygame.draw.circle(screen, RED, enemy.rect.center, enemy.radius)
        # for porta in self.porta_lista:
        #     pygame.draw.rect(screen, RED, porta.rect.center)
        # pygame.draw.circle(screen, RED, (self.player_pos_x, self.player_pos_y), 25)
        # self.porta_lista.draw(screen)

        self.tocha_lista.draw(screen)
        self.luz_lista.draw(screen)
        self.heart_list.draw(screen)
        self.poder_lista.draw(screen)


    def shift_world(self, shift_x):
        self.world_shift += shift_x
        self.rect.x += shift_x
        self.rect2.x += shift_x * 0.8
        self.rect3.x += shift_x * 0.6
        self.rect4.x += shift_x * 0.4

        for heart in self.heart_list:
            heart.rect.x += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            enemy.min_x += shift_x
            enemy.max_x += shift_x
        for bullet in self.faca_lista:
            bullet.rect.x += shift_x
        for spike in self.spike_list:
            spike.rect.x += shift_x
        for hitbox in self.melee_hitbox_list:
            hitbox.rect.x += shift_x
        for hitbox2 in self.hitbox_attack_inimigo:
            hitbox2.rect.x += shift_x
        for limitador in self.limitador1_lista:
            limitador.rect.x += shift_x
        for tocha in self.tocha_lista:
            tocha.rect.x += shift_x
        for luz in self.luz_lista:
            luz.rect.x += shift_x
        for poder in self.poder_lista:
            poder.rect.x += shift_x
        for porta in self.porta_lista:
            porta.rect.x += shift_x

    def carregar_tmx(self, num_level):
        # Carrega o arquivo tmx do Tiledmap Editor
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'level{}.tmx'.format(num_level)))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # Adiciona nas respectivas listas os objetos presentes no arquivo tmx
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player.pos_ini_x = tile_object.x
                self.player.pos_ini_y = tile_object.y
            # if tile_object.name == "porta":
            #     self.porta_lista.add(Porta(tile_object.x, tile_object.y,
            #                                tile_object.width, tile_object.height))
            if tile_object.name == "plataforma":
                self.platform_list.add(Obstacle(1, tile_object.x, tile_object.y,
                                                tile_object.width, tile_object.height))
            if tile_object.name == "plataforma2":
                self.platform_list.add(Obstacle(2, tile_object.x, tile_object.y,
                                                tile_object.width, tile_object.height))
            if tile_object.name == 'vida':
                self.heart_list.add(Heart(tile_object.x, tile_object.y,
                                          tile_object.width, tile_object.height))
            if tile_object.name == 'poder':
                self.poder_lista.add(Poder(tile_object.x, tile_object.y,
                                           tile_object.width, tile_object.height))
            if tile_object.name == 'porta':
                self.porta_lista.add(Porta(tile_object.x, tile_object.y,
                                           tile_object.width, tile_object.height))
            if tile_object.name == "espinhos":
                self.spike_list.add(Espinhos(tile_object.x, tile_object.y,
                                             tile_object.width, tile_object.height))
            if tile_object.name == "escaravelho":
                self.enemy_list.add(Escaravelho(tile_object.x, tile_object.y,
                                                tile_object.width, tile_object.height))
            if tile_object.name == "aranha":
                self.enemy_list.add(Aranha(tile_object.x, tile_object.y,
                                           tile_object.width, tile_object.height))
            if tile_object.name == "esqueleto":
                self.enemy_list.add(Esqueleto(tile_object.x, tile_object.y,
                                              tile_object.width, tile_object.height))
            if tile_object.name == "limitador1":
                self.limitador1_lista.add(Limitador(tile_object.x, tile_object.y,
                                                    tile_object.width, tile_object.height))
            if tile_object.name == "tocha":
                self.tocha_lista.add(Tocha(tile_object.x, tile_object.y))
        for tocha in self.tocha_lista:
            self.luz_lista.add(Luz(tocha.rect.x - 110, tocha.rect.y - 100))
        # for heart in self.heart_list:
        #     self.luz_lista.add(HighLight(heart.rect.x - 20, heart.rect.y - 30))

        # As imagens são carregadas normalmente, não diretamente do arquivo tmx
        self.image = pygame.image.load('maps/level1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.level1_limite = 12800

        # Cada imagem é carregada separadamente e recebe um rect para formar uma camada e para fazer o efeito parallax
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

    def save(self):
        save = open('save.txt', 'w')
        save.write(str(self.player.life))
        save.write('\n')
        save.write(str(self.player.power))
        save.write('\n')
        save.write(str(self.level_no))
        save.write('\n')
        save.write(str(self.world_shift))
        save.write('\n')
        save.write(str(self.player_pos_x))
        save.write('\n')
        save.write(str(self.player_pos_y))
        save.close()



class Level01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -12800 + SCREEN_WIDTH
        self.carregar_tmx(1)


class Level02(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -11000
        self.carregar_tmx(1)


pygame.init()

# Inicializa a função Joystick
pygame.joystick.init()
JOYSTICK = False
joysticks = []

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init() # -1 é um loop infinito, usado para inicializar todos os controles

if len(joysticks) > 1:
    JOYSTICK = True


def marca():
    show_marca = True
    pygame.mouse.set_visible(False)
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    marca1 = pygame.image.load('img/marca.png').convert()
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
    global load_game
    running_menu = True
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
                        load_game = False
                        running_menu = False
                        pygame.mixer_music.stop()
                    if pos_light == 2:
                        confirm.play()
                        load_game = True
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
                        load_game = False
                        running_menu = False
                        pygame.mixer_music.stop()
                    if pos_light == 2:
                        confirm.play()
                        load_game = True
                        running_menu = False
                        pygame.mixer_music.stop()
                    if pos_light == 3:
                        confirm.play()
                        pygame.quit()
                        quit()

        joystick_count = pygame.joystick.get_count()

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
        print_in_screen(screen, 'Novo jogo', 25, pos_play[0] + 70, pos_play[1] + 150, BLUE)
        print_in_screen(screen, 'Carregar jogo', 25, pos_config[0] + 70, pos_config[1] + 150, BLUE)
        print_in_screen(screen, 'Sair do jogo', 25, pos_off[0] + 70, pos_off[1] + 150, BLUE)

        if pos_light == 1:
            screen.blit(light, pos_light1)
        elif pos_light == 2:
            screen.blit(light, pos_light2)
        elif pos_light == 3:
            screen.blit(light, pos_light3)

        clock.tick(10)

        pygame.display.flip()


menu()


def loading():
    pygame.mouse.set_visible(False)
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    carregando = pygame.image.load('img/Carregando.png').convert()
    screen.blit(carregando, [0, 0])
    pygame.display.flip()


loading()


def main():
    # screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Super Hero Mummy: Ramsés")
    player = Player()
    level_list = [Level01(player), Level02(player)]
    current_level_no = 0
    current_level = level_list[current_level_no]
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = player.pos_ini_x
    player.rect.y = player.pos_ini_y
    active_sprite_list.add(player)
    pygame.mouse.set_visible(False)
    done = False
    pygame.mixer.music.load('msc/stage.ogg')
    pygame.mixer.music.play(loops=-1)

    load = open('save.txt', 'r')
    data = []
    for line in load:
        data.append(line)
    if load_game:
        player.life = int(data[0])
        player.power = int(data[1])
        current_level_no = int(data[2])
        current_level.shift_world(int(data[3]))
        player.rect.centerx = int(data[4])
        player.rect.centery = int(data[5])

    '''-------------------------------------------- Loop do jogo ---------------------------------------------------'''

    while not done:
        if player.life <= 0:
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if not JOYSTICK and event.type == pygame.KEYDOWN:
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

            if JOYSTICK and event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0 and not player.dash_delay and not player.tomando_dano:
                    player.jump()
                if event.button == 1 and not player.melee_atk and not player.dash_delay \
                        and not player.dash_limit and not player.tomando_dano:
                    player.dash = True
                    player.do_dash()
                    player.delay_dash()
                if event.button == 2 and not player.dash and not player.tomando_dano:
                    player.melee_atk = True
                    player.melee()
                if event.button == 3 and not player.attacking and not player.tomando_dano:
                    player.attacking = True
                    pygame.time.set_timer(pygame.USEREVENT + 1, 500)
                    player.shoot()
                if event.button == 6:
                    current_level.save()
                if event.button == 7:
                    pygame.quit()
                    quit()

            if event.type == pygame.USEREVENT+1:
                player.attacking = False
            if event.type == pygame.USEREVENT+2:
                player.dano_delay = False
                player.tomando_dano = False
                player.change_x2 = 0
                player.change_y2 = 0
            if event.type == pygame.USEREVENT+3:
                player.attacking = False
                player.attack_delay = False
            if event.type == pygame.USEREVENT+4:
                player.melee_atk = False
                player.melee_delay = False
            if event.type == pygame.USEREVENT+5:
                player.dash = False
                player.dash_change_x = 0
            if event.type == pygame.USEREVENT+6:
                player.dash_delay = False
            if event.type == pygame.USEREVENT+7:
                for enemy in current_level.enemy_list:
                    enemy.hit = False
                    enemy.delay_dano = False
                    enemy.mostrar_barra = False
            if event.type == pygame.USEREVENT-1:
                for enemy in current_level.enemy_list:
                    enemy.delay_attack = False
            if event.type == pygame.USEREVENT-2:
                player.apertando_cima = False
            if event.type == pygame.USEREVENT-3:
                player.apertando_baixo = False

        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            for i in range(2):
                axis = joystick.get_axis(i)
                if JOYSTICK and i == 0 and -0.4 < axis < 0.4:
                    player.stop()
                if i == 0 and axis > 0.2:
                    player.go_right()
                    player.facing = 'right'
                if i == 0 and axis < -0.2:
                    player.go_left()
                    player.facing = 'left'

            hats = joystick.get_numhats()

            for i in range(hats):
                hat = joystick.get_hat(i)
                if hat == (1, 0):
                    player.go_right()
                if hat == (-1, 0):
                    player.go_left()
                if hat == (0, 1):
                    player.cima()
                if hat == (0, -1):
                    player.baixo()

        active_sprite_list.update()
        current_level.update()

        # Se o jogador está no canto direito da tela, ele para e o mundo se move no eixo x negativamente
        if player.rect.right >= 906 and current_level.world_shift > current_level.level_limit:
            diff = player.rect.right - 906
            player.rect.right = 906
            current_level.shift_world(-diff)

        # Se o jogador está no canto esquerdo da tela, ele para e o mundo se move no eixo x positivamente
        if player.rect.left <= 453 and current_level.world_shift < 0:
            diff = 453 - player.rect.left
            player.rect.left = 453
            current_level.shift_world(diff)

        if player.apertando_cima and player.porta:
            if current_level_no < len(level_list) - 1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                current_level.level_no += 1

        current_level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(30)
        pygame.display.flip()

    pygame.quit()


main()
