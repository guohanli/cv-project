import json
import os

import cv2
import numpy as np
from utils import *

def old_pic(img):
    rows, cols, channals = img.shape
    # 去噪
    img_blur = cv2.medianBlur(img, 5)
    for r in range(rows):
        for c in range(cols):
            B = img_blur.item(r, c, 0)
            G = img_blur.item(r, c, 1)
            R = img_blur.item(r, c, 2)
            img[r, c, 0] = np.uint8(min(max(0.272 * R + 0.534 * G + 0.131 * B, 0), 255))
            img[r, c, 1] = np.uint8(min(max(0.349 * R + 0.686 * G + 0.168 * B, 0), 255))
            img[r, c, 2] = np.uint8(min(max(0.393 * R + 0.769 * G + 0.189 * B, 0), 255))
    return img



def cartoon(fn_raw, edge='Canny'):
    # Reading the Image
    image = fn_raw
    # Finding the Edges of Image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
    # Making a Cartoon of the image
    color = cv2.bilateralFilter(image, 12, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    # Visualize the cartoon image
    # cv2.imshow("Cartoon", cartoon)
    # cv2.waitKey(0)  # "0" is Used to close the image window
    # cv2.destroyAllWindows()
    return cartoon

if __name__ == '__main__':
    img_path = os.path.join(album_path, 'man1.png')
    animate_path = os.path.join(current_path, '..', 'resource')
    save_path= os.path.join(animate_path, 'animate_pic','animate_man1.png')
    print(img_path)
    img = cv2.imread(img_path)
    #img=cv2.imread('E:/cv-project/resource/album/man1.png')
    #img = cv2.imread(img_path)
    dst_color=cartoon(img)
    imgnew = cv2.flip(dst_color, 1)
    #dst_color=old_pic(img)
    # cv2.imshow('img_color', dst_color)
    # cv2.waitKey()
    cv2.imwrite(save_path,imgnew)
    img_animate_path = save_path
    img_animate_name = img_name2path(img_animate_path)

    img_animate_url = img_path2url(img_animate_path)
    print(img_animate_url)