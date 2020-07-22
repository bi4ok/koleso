from PIL import ImageFont, Image, ImageDraw
import math


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
    for label in labels:
        font = ImageFont.truetype(path_to_font, font_scale)
        line_height = sum(font.getmetrics())
        # print(label, font.getsize(label))
        fontimage = Image.new('L', (font.getsize(label)[0], line_height))
        ImageDraw.Draw(fontimage).text((0, 0), label, fill=255, font=font)
        fontimage = fontimage.rotate(angle - 90, resample=Image.BICUBIC, expand=True)
        # print(fontimage.size, '+++', angle)
        fontimage_x, fontimage_y = fontimage.size
        rads = math.radians(angle)
        x = radius * math.sin(rads)
        y = radius * math.cos(rads)
        box = (middle_x + int(x) - fontimage_x // 2, middle_y + int(y) - fontimage_y // 2)
        orig.paste((0, 0, 0), box=box, mask=fontimage)
        # print(middle_x + int(x), middle_y + int(y), '=' * 10, label)
        angle -= angle_step

    orig.save(wheel_name)
    return wheel_name
