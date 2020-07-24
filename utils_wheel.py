import os
import random

from PIL import ImageFont, Image, ImageDraw
import math


def multi_label(label,
                cuter_size=140,
                font_scale=11,
                path_to_font='arial.ttf', ):
    label = label.replace('_', ' ')
    font = ImageFont.truetype(path_to_font, font_scale)
    line_width = font.getsize(label)[0]
    if line_width > cuter_size:
        words_out = []
        words_in = label.split()
        string_for_out = ''
        for word in words_in:
            if font.getsize(string_for_out + word + ' ')[0] < cuter_size:
                string_for_out += word + ' '
                continue
            else:
                words_out.append(string_for_out)
                string_for_out = word + ' '
        if string_for_out:
            words_out.append(string_for_out)
    else:
        words_out = [label]
    return words_out


def wheel_maker(labels,
                radius=600,
                radius_max=650,
                path_to_wheel='images\koleso_1.png',
                path_to_font='arial.ttf',
                font_scale=13,
                wheel_name='images\lokeso_test.png'):
    path_to_font = os.path.join("fonts", path_to_font)
    path_to_wheel = os.path.normpath(path_to_wheel)
    wheel_name = os.path.normpath(wheel_name)
    angle_step = 360 // len(labels)
    angle = 90
    orig = Image.open(path_to_wheel)
    width, heigth = orig.size
    middle_x, middle_y = width // 2, heigth // 2
    for _, label_dict in labels.items():
        label = label_dict['name']
        font = ImageFont.truetype(path_to_font, font_scale)
        line_height = sum(font.getmetrics())
        # print(label, font.getsize(label))
        mini_label = multi_label(label, radius_max - radius, font_scale, path_to_font)
        angle_cor = 0
        for words in mini_label[::-1]:
            font_image = Image.new('L', (font.getsize(words)[0], line_height))
            ImageDraw.Draw(font_image).text((0, 0), words, fill=255, font=font)
            font_image = font_image.rotate(angle - 90 + angle_cor, resample=Image.BICUBIC, expand=True)
            # print(font_image.size, '+++', angle)
            font_image_x, font_image_y = font_image.size
            rads = math.radians(angle + angle_cor)
            x = radius * math.sin(rads)
            y = radius * math.cos(rads)
            box = (middle_x + int(x) - font_image_x // 2, middle_y + int(y) - font_image_y // 2)
            orig.paste((5, 5, 5), box=box, mask=font_image)
            angle_cor += 1.1
        # print(middle_x + int(x), middle_y + int(y), '=' * 10, label)
        angle -= angle_step

    orig.save(wheel_name)
    return wheel_name


def make_a_result(current_angle, step, cards):
    while current_angle < -step // 2:
        current_angle += 360
    for chose, card in cards.items():
        minus_angle, plus_angle = card['angles']
        if minus_angle < current_angle <= plus_angle:
            return chose, card['name']
    else:
        return None, None


# def form_results(path, extension='png', exceptions=None):
#     if exceptions is None:
#         exceptions = []
#     results = {}
#     for card in os.listdir(path):
#         if card[-3:] == extension:
#             if card[:-4] not in exceptions:
#                 results[card[:-4]] = {'angles': [0, 0], 'path': os.path.join(path, card)}
#     number_of_cards = len(list(results.keys()))
#     if number_of_cards == 0:
#         return None, None
#     angle_step = 360 // number_of_cards
#     start_angle = -angle_step // 2
#     end_angle = start_angle + angle_step
#     card_range = []
#     for card_name, angles in results.items():
#         card_range.append(start_angle + angle_step // 2 + 1)
#         results[card_name]['angles'] = [start_angle, end_angle]
#         start_angle += angle_step
#         end_angle += angle_step
#     return results, angle_step, card_range


def form_results(path, extension='png', exceptions=None):
    if exceptions is None:
        exceptions = []
    results = {}
    for card in os.listdir(path):
        if card[-3:] == extension:
            duplet = card[-6:-4]
            if duplet[0] == '-':
                duplicate_number = int(duplet[1])
                card_name = card[:-6]
            else:
                duplicate_number = 1
                card_name = card[:-4]
            for number_of_duplicate in range(duplicate_number):
                card_id = card_name + str(number_of_duplicate)
                if card_id not in exceptions:
                    results[card_name + str(number_of_duplicate)] = {'name': card_name, 'angles': [0, 0],
                                                                     'path': os.path.join(path, card)}
    shuffle_dict = list(results.items())
    random.shuffle(shuffle_dict)
    results = dict(shuffle_dict)
    number_of_cards = len(list(results.keys()))
    if number_of_cards == 0:
        return None, None
    angle_step = 360 // number_of_cards
    start_angle = -angle_step // 2
    end_angle = start_angle + angle_step
    card_range = {}
    for card_name, angles in results.items():
        card_range[card_name] = (start_angle + angle_step // 2 + 1)
        results[card_name]['angles'] = [start_angle, end_angle]
        start_angle += angle_step
        end_angle += angle_step
    return results, angle_step, card_range


# print(form_results('cards')[2])
# card_range = form_results('cards')[2]
#
# counter = 0
# def cheating(card_name_to_delete):
#     global counter
#     number_of_cards = len(list(card_range))
#     fake_card_range = card_range.copy()
#     if number_of_cards == 1:
#         print('1')
#         return fake_card_range
#     elif number_of_cards in [2, 3, 4]:
#         chance = random.randint(1, 10)
#         print('2')
#         if chance not in range(number_of_cards):
#             print('+' * 100)
#             del fake_card_range[card_name_to_delete]
#     else:
#         print('3')
#         chance = random.randint(1, 100)
#         if chance not in range(number_of_cards):
#             print('+' * 100)
#             counter += 1
#             del fake_card_range[card_name_to_delete]
#     print(counter)
#     return fake_card_range
#
#
# for i in range(1000):
#     print(len(list(cheating('бунт на корабле0').values())),list(cheating('бунт на корабле0').values()))
