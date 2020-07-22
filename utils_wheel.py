import os

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
                font_scale=11,
                wheel_name='lokeso_test.png'):
    angle_step = 360 // len(labels)
    angle = 90
    orig = Image.open(path_to_wheel)
    width, heigth = orig.size
    middle_x, middle_y = width // 2, heigth // 2
    for label, _ in labels.items():
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
            orig.paste((0, 0, 0), box=box, mask=font_image)
            angle_cor += 1
        # print(middle_x + int(x), middle_y + int(y), '=' * 10, label)
        angle -= angle_step

    orig.save(wheel_name)
    return wheel_name


def make_a_result(current_angle, step, cards):
    while current_angle < -step // 2:
        current_angle += 360
    for chose, (minus_angle, plus_angle) in cards.items():
        if minus_angle < current_angle <= plus_angle:
            return chose
    else:
        return None


def form_results(path, extension='png'):
    results = {}
    for card in os.listdir(path):
        if card[-3:] == extension:
            results[card[:-4]] = [0, 0]
    number_of_cards = len(list(results.keys()))
    angle_step = 360 // number_of_cards
    start_angle = -angle_step // 2
    end_angle = start_angle + angle_step
    for card_name, angles in results.items():
        results[card_name] = [start_angle, end_angle]
        start_angle += angle_step
        end_angle += angle_step
    return results, angle_step

