#!/usr/bin/env python3
"""analyze-file-type-analyzer intro: harbour mouth before the run, nothing that carries words.
Foredeck of the waiting pilot boat in front: rope coiled over a cleat, lantern lit in its gimbal,
brass bell at its post, tied chart roll against the gunwale, all beaded with spray. Open slate
channel water midground with buoys diminishing, lamps lit, nearest buoy orange with weed at its
waterline. Sea as a brightening band behind, sky grading slate to sea glass green at the horizon."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(517)
V1 = "--v1" in sys.argv
W, H = 1200, 520
SLATE = (51, 66, 79); CHALK = (242, 240, 233); GLASS = (127, 182, 154); ORANGE = (224, 106, 31)
img = Image.new("RGB", (W, H), SLATE); d = ImageDraw.Draw(img, "RGBA")
# sky grading from slate overhead to sea glass at the horizon
for y in range(0, 238):
    t = y / 238; col = tuple(int(SLATE[i] + (GLASS[i] - SLATE[i]) * t * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=col)
# sea beyond the mouth: flat brightening band
d.rectangle([0, 238, W, 268], fill=(196, 214, 196))
# open channel water in storm slate, empty and moving
d.rectangle([0, 268, W, H], fill=(44, 58, 70))
for _ in range(120):
    x, y = random.uniform(0, W), random.uniform(276, 500); ln = random.uniform(14, 60)
    d.line([(x, y), (x + ln, y)], fill=(90, 112, 124, 130), width=2)
# line of channel buoys diminishing toward the mouth, lamps lit
buoys = [(980, 300, 46), (830, 288, 34), (716, 280, 25), (632, 274, 18), (566, 270, 13)]
for x, y, s in buoys:
    d.polygon([(x - s * .5, y), (x + s * .5, y), (x + s * .3, y + s * .8), (x - s * .3, y + s * .8)], fill=ORANGE if s > 20 else (70, 82, 92))
    d.line([(x, y), (x, y - s * .7)], fill=(30, 38, 46), width=3)
    d.ellipse([x - 4, y - s * .7 - 7, x + 4, y - s * .7 + 1], fill=(250, 226, 140))  # lamp lit
    d.ellipse([x - s * .7, y + s * .85, x + s * .7, y + s * 1.0], outline=(150, 170, 160, 120))
# nearest buoy close enough to show weed at its waterline
for i in range(9):
    d.line([(952 + i * 6, 344), (948 + i * 6, 356 + (i % 3) * 4)], fill=(70, 104, 66), width=3)
# foredeck foreground: gunwale and deck planks across the lower frame
d.polygon([(0, 402), (W, 382), (W, H), (0, H)], fill=(58, 50, 42))
for i in range(9):
    d.line([(i * 140, 404 - i * 2), (i * 140 - 30, H)], fill=(40, 34, 28), width=4)
# rope coiled over a cleat, left
for r in range(26, 6, -6):
    d.ellipse([120 - r, 452 - r * .55, 120 + r, 452 + r * .55], outline=(178, 156, 116), width=5)
d.rectangle([104, 430, 136, 442], fill=(96, 96, 100))  # cleat
# brass bell still at its post, centre left
d.rectangle([356, 398, 368, 462], fill=(84, 62, 34))
d.polygon([(338, 428), (386, 428), (378, 402), (346, 402)], fill=(196, 158, 62))
d.ellipse([332, 424, 392, 438], fill=(214, 176, 76)); d.ellipse([356, 436, 368, 446], fill=(140, 108, 40))
# oil lantern lit and steady in its gimbal, centre right
d.rectangle([838, 396, 850, 462], fill=(50, 44, 38))
d.ellipse([812, 410, 876, 452], outline=(30, 30, 30), width=4)
d.rectangle([826, 416, 862, 448], fill=(70, 60, 40))
d.ellipse([836, 420, 852, 446], fill=(252, 214, 110))  # flame
d.ellipse([840, 426, 848, 442], fill=(255, 244, 190))
# tied chart roll resting against the gunwale, right; rolled and tied, never unrolled
d.line([(1010, 452), (1150, 424)], fill=(226, 218, 196), width=30)
d.line([(1052, 444), (1056, 428)], fill=(150, 60, 40), width=5); d.line([(1110, 432), (1114, 416)], fill=(150, 60, 40), width=5)
# spray beads from the last run across the deck objects
for _ in range(160 if not V1 else 30):
    x, y = random.uniform(60, 1180), random.uniform(392, 505)
    d.ellipse([x, y, x + 3, y + 2], fill=(230, 238, 240, 170))
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/intro-v1.png" if V1 else "intro-banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
