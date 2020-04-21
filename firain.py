#!/usr/bin/env python
import math
from time import sleep
from sys import exit


try:
    from pyfiglet import figlet_format
except ImportError:
    exit("This script requires the pyfiglet module\nInstall with: sudo pip install pyfiglet")

import unicornhat as unicorn


print("""Figlet demo overlaid on rainbow demo

Text if now overlaid on rainbow background

The scrolling text is defined in the TXT variable.

If the text moves in the wrong direction, change the rotation from 0 to 180.

Text output is kind of limited on a pHAT most letters don't fit on 4x8 matrix.
""")

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()

TXT = "PI"

figletText = figlet_format(TXT+' ', "banner", width=1000) # banner font generates text with heigth 7
textMatrix = figletText.split("\n")[:width] # width should be 8 on both HAT and pHAT!
textWidth = len(textMatrix[0]) # the total length of the result from figlet
i = -1
p = 0.0

def step():
    global i
    global p
    offset = 30

    i = 0 if i>=100*textWidth else i+1 # avoid overflow
    p = p + 0.3
    for h in range(height):
        for w in range(width):
            #create the rainbows
            r = (math.cos((h+p)/2.0) + math.cos((w+p)/2.0)) * 64.0 + 128.0
            g = (math.sin((h+p)/1.5) + math.sin((w+p)/2.0)) * 64.0 + 128.0
            b = (math.sin((h+p)/2.0) + math.cos((w+p)/1.5)) * 64.0 + 128.0
            r = max(0, min(255, r + offset))
            g = max(0, min(255, g + offset))
            b = max(0, min(255, b + offset))
            #now combine rainbow and text
            hPos = (i+h) % textWidth
            chr = textMatrix[w][hPos]
            if chr == ' ':
                unicorn.set_pixel(width-w-1, h,int(r),int(g),int(b))
            else:
                unicorn.set_pixel(width-w-1, h, 255, 0, 255)
    unicorn.show()


while True:
    step()
    sleep(0.2)
