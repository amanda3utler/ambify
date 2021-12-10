### IMPORTS ###
import numpy as np
from PIL import Image
import requests
from ambify.login import get_info
import time

def crop_im(us_name,pl_name):
    '''
    A function that crops the playlist cover (since user-uploaded playlist art can be any dimensions)

    Parameters
    ----------
    us_name: str
        Username
    pl_name: str
        Playlist name

    Returns
    imcrop: PIL.Image.Image
        Cover art cropped to square of 660 by 660 pixels
    '''
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
