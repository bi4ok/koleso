from settings import *
import pygame
import settings as c
import os


class Pointer(pygame.sprite.Sprite):
    def __init__(self, img_arrow_path):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(img_arrow_path).convert_alpha()
        self.image = pygame.transform.scale(player_img, (HEIGHT, HEIGHT))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 3.55, HEIGHT // 2)


class Wheel(pygame.sprite.Sprite):
    def __init__(self, img_wheel_path):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(img_wheel_path).convert_alpha()
        self.image = pygame.transform.scale(player_img, (int(HEIGHT * 2.32), int(HEIGHT * 2.32)))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 20, HEIGHT // 2)
        self.angle = 0

    def update(self, angle_change):
        self.angle -= angle_change
        if self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
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
        # self.text.draw(surface)

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
            context['flag'] = True
            self.image.fill((30, 140, 0))
            self.state = 'hover'
            return True


class Lumi(pygame.sprite.Sprite):
    def __init__(self, path_to_frames):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        for frame in os.listdir(path_to_frames):
            path_to_frame = os.path.join(path_to_frames, frame)
            image = pygame.image.load(path_to_frame).convert_alpha()
            scale_rate = 1.3
            image = pygame.transform.scale(image, (int(HEIGHT / scale_rate), int(HEIGHT / scale_rate)))
            self.frames.append(image)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 3.75, HEIGHT // 2.1)
        self.current_frame = 0

    def open_lumi(self):
        for frame in self.frames:
            self.image = frame
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect(center=self.rect.center)
            yield self.current_frame
            self.current_frame += 1

    def close_lumi(self):
        for frame in self.frames[::-1]:
            self.image = frame
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect(center=self.rect.center)
            yield self.current_frame
            self.current_frame -= 1


class Cards(pygame.sprite.Sprite):
    def __init__(self, cards):
        pygame.sprite.Sprite.__init__(self)
        self.cards = {}
        for card_name, angle_and_path in cards.items():
            image = pygame.image.load(angle_and_path['path']).convert_alpha()
            image = pygame.transform.scale(image, (int(HEIGHT / 2.5), int((HEIGHT / 2.5) * 1.518)))
            self.cards[card_name] = image
        self.image = list(self.cards.items())[0][1]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 3.75, HEIGHT // 2.1)
        self.current_card_name = list(self.cards.items())[0][0]

    def change_card(self, change_to):
        if self.cards.get(change_to):
            self.image = self.cards[change_to]
            self.current_card_name = change_to
        else:
            print('НЕТ КАРТЫ')