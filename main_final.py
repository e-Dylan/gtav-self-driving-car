import numpy as np
import cv2
import time
import os
from directkeys import PressKey, ReleaseKey, W, A, S, D
from drawlanes import draw_lanes
from grabscreen import grab_screen
from getkeys import keycheck

import random

WIDTH = 160
HEIGHT = 120
MODEL_NAME = ""

t_time = 0.09

def keys_to_output(keys):
    # [A, W, D]
    output = [0, 0, 0]
    if "A" in keys:
        output[0] = 1
    elif "D" in keys:
        output[2] = 1
    else:
        output[1] = 1

    return output

# region of interest
def roi(img, vertices):
    mask = np.zeros_like(img) # zero-filled tensor with same indices as passed image
    cv2.fillPoly(mask, vertices, 255) # fill the mask tensor poly with passed vertices
    masked_img = cv2.bitwise_and(img, mask) # take only masked portion of img
    return masked_img

def process_img(image):
    original_image = image
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2 = 300) # Canny edge detection alg
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0) # apply blur to image to remove anti-aliasing issue

    vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500],], np.int32)
    
    processed_img = roi(processed_img, [vertices]) # apply mask for ROI to processed screen image

    lines = cv2.HoughLinesP(processed_img, rho=1, theta=np.pi/180, threshold=180, minLineLength=20, maxLineGap=15)
    # declare default slopes of lane lines, in case none are found.
    m1 = 0
    m2 = 0
    try:
    #draw_lines(processed_img, lines)
        l1, l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 20)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 20)
    except Exception as e:
        print(f"PRINTING ERROR: {str(e)}")
        pass
    try:
        for coords in lines:
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)
            except Exception as e:
                print(str(e))

    except Exception as e:
        pass

    return processed_img, original_image, m1, m2

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(W)
    PressKey(A)
    ReleaseKey(D)
    time.sleep(t_time)
    ReleaseKey(A)

def right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    time.sleep(t_time)
    ReleaseKey(D)

file_name = "training_data.npy"

# check if training file exists to continue appending to
if os.path.isfile(file_name):
    print("Training data file exists, loading previous data...")
    training_data = list(np.load(file_name))
else:
    print("Training data file does not exist, starting new data file...")
    training_data = []


def main():

    last_time = time.time()
    # Count down from 4
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while (True): # hook

        if not paused:
            # 800 x 600 windowed mode
            screen = grab_screen(region=(0, 40, 800, 600))
            print(f"loop took {time.time()-last_time}")
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (WIDTH, HEIGHT))


            # processed_image, original_iamge, m1, m2 = process_img(screen)
            # cv2.imshow("ai view", processed_image)

            #prediction

            turn_thresh = 0.75
            fwd_thresh = 0.70

        
        keys = keycheck()

        if "T" in keys:
            if paused:
                # unpause ai
                paused = False
                time.sleep(1)
            else:
                # pause ai, release all keys
                paused = True
                ReleaseKey(W)
                ReleaseKey(A)
                ReleaseKey(D)
                time.sleep(1)

main()