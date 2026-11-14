"""Generate veniz launcher icons (coffee cup) at all densities."""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/home/z/my-project/scripts/veniz-android"

# gradient background
BG_TOP = (109, 76, 65)     # #6D4C41
BG_BOT = (62, 39, 35)      # #3E2723
CREAM = (255, 248, 240)    # #FFF8F0
CREAM_DIM = (255, 248, 240)

S = 512
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# background rounded square with vertical gradient
grad = Image.new("RGBA", (S, S))
gd = ImageDraw.Draw(grad)
for y in range(S):
    t = y / S
    c = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)) + (255,)
    gd.line([(0, y), (S, y)], fill=c)
mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([8, 8, S - 8, S - 8], radius=116, fill=255)
img.paste(grad, (0, 0), mask)
d = ImageDraw.Draw(img)

# steam: two up-curving arcs above the cup
for cx in (205, 272):
    d.arc([cx - 24, 138, cx + 24, 202], start=200, end=340,
          fill=CREAM_DIM + (170,), width=14)

# cup body
d.rounded_rectangle([148, 202, 338, 356], radius=30, fill=CREAM + (255,))
# cup top rim highlight
d.rounded_rectangle([160, 214, 326, 234], radius=10,
                    fill=(214, 190, 170, 255))

# handle (ring) on the right side
d.ellipse([318, 228, 400, 316], outline=CREAM + (255,), width=22)
# redraw body over inner part of the ring
d.rounded_rectangle([148, 202, 338, 356], radius=30, fill=CREAM + (255,))
d.rounded_rectangle([160, 214, 326, 234], radius=10,
                    fill=(214, 190, 170, 255))

# saucer
d.rounded_rectangle([112, 372, 374, 408], radius=18, fill=CREAM + (255,))

# brand text
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 58)
tb = d.textbbox((0, 0), "veniz", font=font)
tw = tb[2] - tb[0]
d.text(((S - tw) / 2, 424), "veniz", font=font, fill=CREAM + (255,))

# export all densities
sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for name, px in sizes.items():
    out = os.path.join(BASE, f"res/mipmap-{name}/ic_launcher.png")
    im = img.resize((px, px), Image.LANCZOS)
    im.save(out)
    print(out, im.size)

# blank check on the biggest one
h = img.convert("L").histogram()
nonwhite = 1 - h[255] / sum(h)
print("non-white ratio:", round(nonwhite, 3))
