import random


def code():
    string = []
    for i in range(5):
        l = chr(random.randint(97, 122))
        b = chr(random.randint(65, 90))
        n = str(random.randint(0, 9))

        t = random.choice([l, b, n])
        string.append(t)
    return ''.join(string)


from PIL import Image, ImageDraw, ImageFont


def code_img():
    with open('1.png', 'wb') as f:
        img_obj = Image.new('RGB', (80, 100), (55, 255, 255))
        draw_obj = ImageDraw.Draw(img_obj)
        font_obj = ImageFont.truetype('static/font/kumo.tff', 28)
        draw_obj.text((0, 0), ('a'), fill=(255, 100, 255), font=font_obj)

        img_obj.save(f)


code_img()
