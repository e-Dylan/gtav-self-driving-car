# train_model.py

import numpy as np
from alexnet import alexnet

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
neuralnetwork = "alexnetmodnew"
MODEL_NAME = f"pygta5-car-{LR}-{neuralnetwork}-{EPOCHS}-epochs.model"

model = alexnet(WIDTH, HEIGHT, LR)

train_data = np.load("C:/Users/Dylan/Desktop/build/python_projects/gta_self_driving_car/data/training_data_balanced.npy", allow_pickle = True)
print(len(train_data))
train = train_data[:-500] # leave 500 at the end out for testing
test = train_data[-500:] # last 500 data

X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
Y = [i[1] for i in train]

test_X = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
test_Y = [i[1] for i in test]

model.fit({"input": X}, {"targets": Y}, n_epoch = EPOCHS, 
            validation_set = ({"input": test_X}, {"targets": test_Y}),
            snapshot_step = 500, show_metric = True, run_id = MODEL_NAME)
0
# tensorboard --logdir=foo:C:/Users/Dylan/Desktop/build/python_projects/gta_self_driving_car/log

model.save(MODEL_NAME)
