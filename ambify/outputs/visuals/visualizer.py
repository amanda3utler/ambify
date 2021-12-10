import numpy as np
from PIL import Image
import requests
from ambify.login import get_info
import time

def crop_im(us_name,pl_name):
    myobj = get_info(us_name,pl_name)
    with myobj.get_pl_cover() as im:
        if im.width > im.height:
            left = im.width//2 - im.height//2
            right = im.width//2 + im.height//2
            bbox = (left,0,right,im.height)
            imcrop = im.crop(bbox)
        elif im.width < im.height:
            lower = im.height//2 - im.width//2
            upper = im.height//2 + im.width//2
            bbox = (0,lower,im.width,upper)
            imcrop = im.crop(bbox)
        else:
            imcrop = im.crop()
    imcrop = imcrop.resize((660, 660))
    return imcrop


palette1 = ["yellow","cadmium-yellow","amber","yellow-orange","tangerine"]
header = "https://htmlcolorcodes.com/assets/images/colors/"
end = "-color-solid-background-1920x1080.png"

def get_colors(num):
    pthnm = header+palette1[num]+end
    return pthnm
