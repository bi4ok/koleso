from settings import *
import pygame
import settings as c


class Pointer(pygame.sprite.Sprite):
    def __init__(self, img_arrow_path):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(img_arrow_path).convert()
        self.image = pygame.transform.scale(player_img, (562, 562))
        self.image.set_colorkey(BLACK)
        self.orig_image = self.image
        # self.orig_image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 3.55, HEIGHT // 2)


class Wheel(pygame.sprite.Sprite):
    def __init__(self, img_wheel_path):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(img_wheel_path).convert()
        self.image = pygame.transform.scale(player_img, (1300, 1300))
        self.image.set_colorkey(BLACK)
        self.orig_image = self.image
        # self.orig_image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 20, HEIGHT // 2)
        self.angle = 0

    def update(self, angle_change):
        self.angle -= angle_change
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.left > WIDTH:
            self.rect.right = 0
        return self.angle


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, on_click=lambda x: None, padding=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey(BLACK)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.state = 'normal'
        self.on_click = on_click

    @property
    def back_color(self):
        return dict(normal=c.button_normal_back_color,
                    hover=c.button_hover_back_color,
                    pressed=c.button_pressed_back_color)[self.state]

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.rect)
        #self.text.draw(surface)

    def handle_mouse_event(self, type, pos, context):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos, context)

    def handle_mouse_move(self, pos):
        if self.rect.collidepoint(pos):
            if self.state != 'pressed':
                self.image.fill((30, 140, 0))
                self.state = 'hover'
        else:
            self.image.fill((55, 255, 0))
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.image.fill((190, 30, 30))
            self.state = 'pressed'

    def handle_mouse_up(self, pos, context):
        if self.state == 'pressed':
            context['text'] = self.on_click()
            self.image.fill((30, 140, 0))
            self.state = 'hover'
