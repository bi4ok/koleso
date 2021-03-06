import sys
import random
import math
import pygame
from sprite import Wheel, Pointer, Button, Lumi, Cards
from settings import *
from utils_wheel import wheel_maker, make_a_result, form_results
import os


class Kolizei:
    def __init__(self, img_arrow_path='images\\lumi_clear_2.png',
                 img_wheel_path_null='images\\koleso_hi_res.png',
                 img_background_path='images\\koleso.png',
                 cards_directory='cards',
                 card_extension='png',
                 music_wheel='music\\WheelSoundEffect.ogg',
                 music_win='music\\DropSoundEffect.ogg',
                 lumi_path='lumi'):
        pygame.init()
        self.img_wheel_path_null = os.path.normpath(img_wheel_path_null)
        img_arrow_path = os.path.normpath(img_arrow_path)
        img_background_path = os.path.normpath(img_background_path)
        music_wheel = os.path.normpath(music_wheel)
        music_win = os.path.normpath(music_win)
        self.cards_directory = os.path.normpath(cards_directory)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load(img_background_path).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()
        pygame.mixer.init()
        self.music = {'wheel': pygame.mixer.Sound(music_wheel),
                      'win': pygame.mixer.Sound(music_win)}
        self.cards, self.step, self.card_range = form_results(self.cards_directory, extension=card_extension)
        self.current_card = Cards(self.cards)
        self.img_wheel_path = wheel_maker(self.cards,
                                          radius=1740,
                                          radius_max=1990,
                                          path_to_wheel=self.img_wheel_path_null,
                                          font_scale=50)
        self.wheel = Wheel(self.img_wheel_path)
        self.lumi = Lumi(lumi_path)
        pointer = Pointer(img_arrow_path)
        button = Button(x=WIDTH * 0.9, y=HEIGHT * 0.1, w=100, h=50, on_click=self.run_wheel_global)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.wheel)
        self.all_sprites.add(pointer)
        self.all_sprites.add(self.current_card)
        self.all_sprites.add(self.lumi)
        self.all_sprites.add(button)
        self.mouse_handlers = [button.handle_mouse_event]
        self.running = True
        self.context = {'flag': False}
        pygame.display.set_caption("Kolizei")
        self.clock = pygame.time.Clock()
        self.mouse_block = False
        self.exeptions = []
        self.card_extension = card_extension
        self.lumi_is_closed = True
        self.next_img_wheel_path = None

    def make_new_wheel(self):
        if len(self.cards) == 1:
            self.exeptions = []
        self.cards, self.step, self.card_range = form_results(self.cards_directory,
                                                              extension=self.card_extension,
                                                              exceptions=self.exeptions)
        self.next_img_wheel_path = wheel_maker(self.cards,
                                               radius=1740,
                                               radius_max=1990,
                                               path_to_wheel=self.img_wheel_path_null,
                                               font_scale=50)

    def update_wheel(self):
        if self.next_img_wheel_path:
            self.wheel.__init__(self.next_img_wheel_path)
            self.context['flag'] = False
            del self.context['text']

    def lumi_open(self):
        if self.lumi_is_closed is True:
            self.music['win'].set_volume(0.1)
            self.music['win'].play()
            open_lumi = 0
            lumi_gen = self.lumi.open_lumi()
            lumi_running = True
            open_speed = 90
            while lumi_running:
                open_speed += 30
                self.clock.tick(FPS)
                self.all_sprites.draw(self.screen)
                if open_lumi < 7:
                    if open_speed >= 100:
                        open_speed = 0
                        open_lumi = next(lumi_gen)
                elif open_lumi == 7:
                    lumi_running = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                pygame.display.flip()
            self.make_new_wheel()
            self.lumi_is_closed = False

    def lumi_close(self):
        if self.lumi_is_closed is False:
            close_lumi = 7
            lumi_gen_close = self.lumi.close_lumi()
            lumi_running = True
            close_speed = 90
            while lumi_running:
                close_speed += 34
                self.clock.tick(FPS)
                self.all_sprites.draw(self.screen)
                if close_lumi > 0:
                    if close_speed >= 100:
                        close_speed = 0
                        close_lumi = next(lumi_gen_close)
                elif close_lumi == 0:
                    lumi_running = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                pygame.display.flip()
            self.update_wheel()
            self.lumi_is_closed = True

    def run(self):
        self.wheel.update(0)
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
                self.draw_text(self.screen, self.context.get('text'), 25, int(WIDTH * 0.26), int(HEIGHT * 0.04))

            pygame.display.flip()
        pygame.quit()

    def cheating(self, card_name_to_delete):
        number_of_cards = len(list(self.card_range))
        fake_card_range = self.card_range.copy()
        if number_of_cards == 1:
            return fake_card_range
        elif number_of_cards in [2, 3, 4]:
            chance = random.randint(1, 10)
            if chance not in range(number_of_cards):
                del fake_card_range[card_name_to_delete]
        else:
            chance = random.randint(1, 100)
            if chance not in range(number_of_cards):
                del fake_card_range[card_name_to_delete]
        return fake_card_range

    def make_speed_card_range(self, cur_card_range):
        speed_card_range_dict = {}
        for angle in cur_card_range:
            start_angle = angle - (self.step // 4)
            speed_card_range_dict[angle] = []
            for i in range(self.step // 2):
                speed_card_range_dict[angle].append(start_angle)
                start_angle += 1
        return speed_card_range_dict

    def run_wheel_global(self):
        self.lumi_close()
        wheel_speed = random.uniform(15, 25)
        min_wheel_speed = wheel_speed / 3
        self.music['wheel'].set_volume(0.1)
        self.music['wheel'].play()
        self.mouse_block = True
        current_card_range = list(self.cheating('второе дыхание0').values())
        slow_down = False
        speed_range = self.make_speed_card_range(current_card_range)
        next_cur_pos = 0
        while self.running:
            self.clock.tick(FPS)
            self.all_sprites.draw(self.screen)
            angle_res = self.wheel.update(wheel_speed)
            pygame.display.flip()
            if slow_down is False and wheel_speed <= min_wheel_speed:
                for position, angles in speed_range.items():
                    if int(angle_res) in angles:
                        cur_pos = current_card_range.index(position)
                        next_cur_index = cur_pos + 1 if cur_pos < (len(current_card_range) - 1) else 0
                        next_cur_pos = current_card_range[next_cur_index]
                        slow_down = True
            elif slow_down is True:
                wheel_speed = min_wheel_speed * (abs(next_cur_pos - angle_res) / self.step)
                wheel_speed = wheel_speed if wheel_speed > 1 else 1
            else:
                wheel_speed = wheel_speed - 0.1 if wheel_speed > 1 else 1
            if wheel_speed == 1 and (int(angle_res) in current_card_range):
                self.music['wheel'].stop()
                result, card_name = make_a_result(angle_res, self.step, self.cards)
                self.exeptions.append(result)
                pygame.display.flip()
                self.mouse_block = False
                self.current_card.change_card(result)
                self.lumi_open()
                return card_name
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def draw_text(self, surf, text, size, x, y):
        font_name = pygame.font.match_font('bahnschrift')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)


if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
    print(os.path.dirname(sys.executable), '---')
s = Kolizei()
s.run()
