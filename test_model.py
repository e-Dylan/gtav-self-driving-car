import numpy as np
import cv2
import time
import os
from directkeys import PressKey, ReleaseKey, W, A, S, D
from getkeys import keycheck
from grabscreen import grab_screen
from alexnet import alexnet

t_time = 0.09

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
neuralnetwork = "alexnetmodnew"
MODEL_NAME = f"pygta5-car-{LR}-{neuralnetwork}-{EPOCHS}-epochs.model"

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

model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

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

            #prediction
            prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0] # reshape current screengrab into w, h tensor and input into nn
            print(prediction) # rounded pred, unrounded vector pred

            turn_thresh = 0.3
            fwd_thresh = 0.70

            # if prediction[1] > fwd_thresh:
            #     straight()
            # elif prediction[0] > turn_thresh:
            #     straight()
            # elif prediction[2] > turn_thresh:
            #     right()
            # else:
            #     straight()

            if prediction[1] == max(prediction):
                left()
            if prediction[0] == max(prediction):
                straight()
            if prediction[2] == max(prediction):
                right()


        keys = keycheck()

        if "T" in keys:
            paused = not paused
            ReleaseKey(A)
            ReleaseKey(W)
            ReleaseKey(D)
            time.sleep(1)


main()





