from PIL import Image, ImageEnhance, ImageDraw, ImageFont

def to_bitmap_array(img, name):
    img = img.convert("1")
    pixels = list(img.getdata())
    byte_list = []
    for i in range(0, len(pixels), 8):
        byte = 0
        for j in range(8):
            if i + j < len(pixels):
                if pixels[i + j] == 255:
                    byte |= (1 << (7 - j))
        byte_list.append(f"0x{byte:02X}")
    return f"const unsigned char display_bitmap[] = {{\n" + ", ".join(byte_list) + "\n};"

# 二维码 128x128
qr = Image.open("qr.jpg").convert("L")
qr = qr.resize((128, 128), Image.LANCZOS)
qr = qr.point(lambda x: 0 if x < 128 else 255, "1")

# 头像 128x128
avatar = Image.open("profile.jpg").convert("L")
avatar = ImageEnhance.Contrast(avatar).enhance(2.0)
avatar = avatar.resize((128, 128), Image.LANCZOS)
avatar = avatar.point(lambda x: 0 if x < 128 else 255, "1")

# 画布 128x296
canvas = Image.new("L", (128, 296), 255)
canvas.paste(qr.convert("L"), (0, 0))
canvas.paste(avatar.convert("L"), (0, 128))

# 文字区域 128x40，底部居中
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("arial.ttf", 18)
except:
    font = ImageFont.load_default()

text = "Wolfram Liu"
bbox = draw.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
x = (128 - text_w) // 2
draw.text((x, 264), text, font=font, fill=0)

canvas.save("preview.png")

with open("imagedata.h", "w") as f:
    f.write("#pragma once\n\n")
    f.write(to_bitmap_array(canvas, "display_bitmap"))

print("完成，生成 imagedata.h 和 preview.png")