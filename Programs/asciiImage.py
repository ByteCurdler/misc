#!/usr/bin/python3
from PIL import Image
import numpy, sys

#symb = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
symb = " `-_,:;^\"~\\/*!)(rl?][}|tfj+ic{1IvxznuLCYJ%kh$Za&XoO8Ud0@QbqMm#pBW"
print(len(symb))

def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'RGBA':
        channels = 4
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((height, width, channels))
    return pixel_values

if(len(sys.argv) < 2):
    imName = input("Image name: ")
else:
    imName = sys.argv[1]
    if(len(sys.argv) < 3):
        lMode = ["A", "M", "H"].index(input("""Brightness mode:
\t(A)verage (R+G+B / 3)
\t(M)in-Max (min(R,G,B)+max(R,G,B) / 3)
\t(H)uman Perception (0.21*R + 0.72*G + 0.07*B)
\t\t\tPick: """)[0].upper())
    else:
        lMode = ["A", "M", "H"].index(sys.argv[2][0].upper())

im = get_image(imName)


art = ""

for y in range(len(im)):
    for x in range(len(im[0])):
        pxl = im[y][x]
        if(lMode == 0):
            lightness = ( #Average
                            pxl[0] + pxl[1] + pxl[2]
                        ) / (255*3 / 64)
        elif(lMode == 1):
            lightness = ( #Min Max
                            min(pxl[0], pxl[1], pxl[2]) + max(pxl[0], pxl[1], pxl[2])
                        ) / (255*2 / 64) #Accounting for the fact that len(symb) = 65, not 256
        else:
            lightness = ( #Human vision
                            0.21*pxl[0] + 0.72*pxl[1] + 0.07*pxl[2]
                        ) / (255 / 64)
        art += symb[
                int(
                    lightness
                ) #int
            ] * 2 #symb
    art += "\n"

f = open(imName + ".txt", "w+")
f.write(art)
f.close()

f = open(imName + ".html", "w+")
f.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>{name} ASCII Art</title>
  </head>
  <body style="background-color: black; color:white; font-size: 2px; font-family: monospace">
    <pre>
{pic}
    </pre>
  <details style="font-size: 30px">
    <summary>Original image</summary>
    <img src="{name}" style="font-size:2px; width: {w}em">
  </details>
  </body>
</html>
""".format(name=imName, pic=art, w=len(im)*1.2))
f.close()
