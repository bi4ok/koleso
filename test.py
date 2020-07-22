import pygame
from sprite import Wheel, Pointer, Button
from settings import *
from utils_wheel import wheel_maker, make_a_result, form_results
import os


class Kolizei:
    def __init__(self, img_arrow_path='images\lumi.png',
                 img_wheel_path_null='images\circle.png',
                 img_background_path='images\koleso.png',
                 cards_directory='cards',
                 card_extension='txt',
                 music_wheel='music\WheelSoundEffect.ogg',
                 music_win='music\DropSoundEffect.ogg', ):
        pygame.init()
        img_wheel_path_null = os.path.normpath(img_wheel_path_null)
        img_arrow_path = os.path.normpath(img_arrow_path)
        img_background_path = os.path.normpath(img_background_path)
        music_wheel = os.path.normpath(music_wheel)
        music_win = os.path.normpath(music_win)
        cards_directory = os.path.normpath(cards_directory)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load(img_background_path).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()
        self.music = {'wheel': pygame.mixer.Sound(music_wheel),
                      'win': pygame.mixer.Sound(music_win)}
        self.cards, self.step = form_results(cards_directory, extension=card_extension)
        self.img_wheel_path = wheel_maker(self.cards, radius=560, radius_max=660, path_to_wheel=img_wheel_path_null)
        self.all_sprites = pygame.sprite.Group()
        self.wheel = Wheel(self.img_wheel_path)
        pointer = Pointer(img_arrow_path)
        button = Button(x=WIDTH * 0.9, y=HEIGHT * 0.1, w=100, h=50, on_click=self.run_wheel_global)
        self.all_sprites.add(self.wheel)
        self.all_sprites.add(pointer)
        self.all_sprites.add(button)
        self.mouse_handlers = [button.handle_mouse_event]
        self.running = True
        self.context = {}
        pygame.mixer.init()
        pygame.display.set_caption("Kolizei")
        self.clock = pygame.time.Clock()
        self.mouse_block = False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.screen.blit(self.background, self.background_rect)
            self.all_sprites.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    for handler in self.mouse_handlers:
                        handler(event.type, event.pos, self.context)
            if self.context.get('text'):
                self.draw_text(self.screen, self.context.get('text'), 18, int(WIDTH * 0.26), int(HEIGHT * 0.04))
            pygame.display.flip()
        pygame.quit()

    def run_wheel_global(self):
        wheel_speed = 3
        self.music['wheel'].set_volume(0.1)
        self.music['wheel'].play()
        self.mouse_block = True
        while True:
            self.clock.tick(FPS)
            self.all_sprites.draw(self.screen)
            angle_res = self.wheel.update(wheel_speed)
            wheel_speed -= (1 / FPS)
            pygame.display.flip()
            if wheel_speed <= 0:
                self.music['wheel'].stop()
                result = make_a_result(angle_res, self.step, self.cards)
                pygame.display.flip()
                self.mouse_block = False
                return result
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def draw_text(self, surf, text, size, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)


s = Kolizei()
s.run()
