#!/usr/bin/env python3
"""analyze-file-type-analyzer banner: harbour mouth half an hour before sunrise, camera low on the
pilot boat looking aft. Wake spreads across the whole lower frame, boiling near the stern, settling
into long lines. Inbound ship in the upper distance past the bow at frame right, dark hull, two lit
portholes. Channel markers both sides, nearest buoy orange with lamp just lit. Foreground foredeck:
rolled chart tied with cord, brass bell on its post, rope over a cleat, lantern steady in a gimbal.
Title painted on the transom board at the stern in Average Sans chalk on slate, weathered edges,
one line only, no other readable wording anywhere."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(641)
V1 = "--v1" in sys.argv
W, H = 1200, 520
SLATE = (51, 66, 79); CHALK = (242, 240, 233); GLASS = (127, 182, 154); ORANGE = (224, 106, 31)
img = Image.new("RGB", (W, H), SLATE); d = ImageDraw.Draw(img, "RGBA")
HERE = __file__.rsplit("/", 1)[0]
# sky grading slate to a thin sea glass band at the horizon
for y in range(0, 190):
    t = y / 190; col = tuple(int(SLATE[i] + (GLASS[i] - SLATE[i]) * t * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=col)
d.rectangle([0, 190, W, 208], fill=(206, 222, 200))
# inbound ship, upper right distance: dark hull riding high, two lit portholes, bow wave barely started
d.polygon([(828, 168), (1150, 168), (1122, 198), (862, 198)], fill=(28, 34, 40))
d.rectangle([920, 138, 1064, 168], fill=(36, 44, 52))
for px in (962, 1018):
    d.ellipse([px, 176, px + 10, px * 0 + 186], fill=(250, 226, 140))
for i in range(16):
    d.ellipse([850 + i * 8, 200 + (i % 2) * 3, 858 + i * 8, 205], fill=(220, 228, 220, 130))
# channel water and markers on both sides
d.rectangle([0, 208, W, H], fill=(42, 56, 68))
for x, y, s, near in [(150, 268, 30, True), (360, 240, 18, False), (1064, 252, 22, False), (940, 232, 14, False)]:
    d.polygon([(x - s * .5, y), (x + s * .5, y), (x + s * .3, y + s * .8), (x - s * .3, y + s * .8)], fill=ORANGE if near else (66, 78, 88))
    d.ellipse([x - 3, y - 12, x + 3, y - 6], fill=(250, 226, 140))
# wake spreading behind across the whole lower frame: boiling near stern, long lines toward edges
for i in range(240):
    t = random.random(); x = 600 + (random.random() - 0.5) * (120 + t * 1080); y = 300 + t * 130
    s = (1 - t) * 13 + 3
    d.ellipse([x - s, y - s * .4, x + s, y + s * .4], fill=CHALK if random.random() > 0.22 else GLASS)
for side in (-1, 1):
    for k in range(5):
        d.line([(600 + side * 30, 302), (600 + side * (420 + k * 130), 470 - k * 8)], fill=(210, 220, 210, 110), width=3)
# foredeck foreground objects, ready and unposed
d.polygon([(0, 452), (330, 430), (330, H), (0, H)], fill=(56, 48, 40))  # deck corner left with bell and rope
d.polygon([(338, 448), (352, 434), (352, 486), (338, 486)], fill=(84, 62, 34))
d.polygon([(324, 436), (366, 436), (358, 414), (332, 414)], fill=(196, 158, 62)); d.ellipse([320, 432, 370, 444], fill=(214, 176, 76))
for r in range(22, 5, -5):
    d.ellipse([150 - r, 474 - r * .55, 150 + r, 474 + r * .55], outline=(178, 156, 116), width=4)
d.polygon([(880, H), (W, H), (W, 424), (920, 440)], fill=(56, 48, 40))  # deck corner right with chart and lantern
d.line([(976, 470), (1108, 448)], fill=(226, 218, 196), width=26)
d.line([(1016, 464), (1019, 450)], fill=(150, 60, 40), width=4); d.line([(1070, 456), (1073, 442)], fill=(150, 60, 40), width=4)
d.rectangle([928, 428, 968, 472], fill=(60, 52, 42)); d.ellipse([936, 434, 960, 464], fill=(252, 214, 110)); d.ellipse([944, 442, 952, 458], fill=(255, 244, 190))
# transom board at the stern, centre: slate painted wood, title in chalk Average Sans, weathered edges
d.rectangle([318, 318, 882, 392], fill=(44, 56, 68)); d.rectangle([318, 318, 882, 392], outline=CHALK, width=3)
for _ in range(60):  # weathering flecks at the letter edges and board corners
    x, y = random.uniform(322, 878), random.uniform(322, 388)
    d.point((x, y), fill=(70, 84, 96))
if V1:  # flaw: title hoisted on the sky as a sign instead of painted on the transom
    f = ImageFont.truetype(HERE + "/fonts/AverageSans.ttf", 44)
    t = "analyze-file-type-analyzer"; tw = d.textlength(t, font=f); d.text(((W - tw) / 2, 30), t, font=f, fill=CHALK)
else:
    f = ImageFont.truetype(HERE + "/fonts/AverageSans.ttf", 37)
    t = "analyze-file-type-analyzer"; tw = d.textlength(t, font=f); d.text(((W - tw) / 2, 336), t, font=f, fill=CHALK)
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/banner-v1.png" if V1 else "banner.png"
img.save(HERE + "/" + out); print("saved", out)
