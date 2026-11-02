#!/usr/bin/env python3
"""analyze-file-type-analyzer logo: the wake of a pilot boat at the moment it turns, from directly
above. Water and foam and nothing else: a clean V opening toward the bottom, arms uneven, outer arm
thicker and broken into sea glass flecks, storm slate calm inside the V, one short buoy orange dash
at the apex. No hull drawn. Name in Average Sans, storm slate on chalk, harbour notice plain."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont
random.seed(99)
V1 = "--v1" in sys.argv
W, H = 880, 660
SLATE = (51, 66, 79); CHALK = (242, 240, 233); GLASS = (127, 182, 154); ORANGE = (224, 106, 31)
img = Image.new("RGB", (W, H), CHALK); d = ImageDraw.Draw(img, "RGBA")
HERE = __file__.rsplit("/", 1)[0]
font = ImageFont.truetype(HERE + "/fonts/AverageSans.ttf", 40)
# water field: the upper panel is all sea
d.rectangle([70, 40, 810, 470], fill=SLATE)
for _ in range(300):
    x, y = random.uniform(76, 804), random.uniform(46, 464)
    d.point((x, y), fill=(66, 82, 96))
apex = (440, 92)
def arm(endx, thick, fleck):
    # broken foam arm: overlapping chalk flecks along the line, never a smooth edge
    steps = 90
    for i in range(steps):
        t = i / steps; x = apex[0] + (endx - apex[0]) * t; y = apex[1] + (442 - apex[1]) * t
        s = thick * (0.35 + t * 0.9) * random.uniform(0.6, 1.25)
        col = CHALK if random.random() > fleck else GLASS
        if V1:  # smooth solid arm: reads as a valley or book, the flaw draft 2 must break up
            d.ellipse([x - s * .4, y - s * .4, x + s * .4, y + s * .4], fill=CHALK)
        else:
            d.ellipse([x - s, y - s * .45, x + s, y + s * .45], fill=col)
            if random.random() > 0.5:
                fx, fy = x + random.uniform(-9, 9), y + random.uniform(-7, 7)
                d.ellipse([fx, fy, fx + 4, fy + 3], fill=CHALK)
arm(150, 15, 0.16)   # inner arm of the turn, thinner
arm(748, 26, 0.34)   # outer arm throws more water, thicker, more sea glass flecks
# foam churn right at the apex where the stern has just passed
for _ in range(46):
    x, y = random.gauss(apex[0], 20), random.gauss(apex[1] + 8, 13)
    d.ellipse([x - 6, y - 3, x + 6, y + 3], fill=CHALK)
# the single short orange dash at the apex, a hint of the boat, not a picture of it
d.line([(apex[0] - 13, apex[1] - 4), (apex[0] + 13, apex[1] + 4)], fill=ORANGE, width=7)
name = "analyze-file-type-analyzer"
tw = d.textlength(name, font=font); d.text(((W - tw) / 2, 522), name, font=font, fill=SLATE)
out = "scratch/logo-v1.png" if V1 else "logo.png"
img.save(HERE + "/" + out)
if not V1:
    img.resize((64, 48)).save(HERE + "/scratch/logo64-ship.png")
print("saved", out)
