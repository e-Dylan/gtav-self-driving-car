import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

train_data = np.load("training_data_big.npy", allow_pickle = True)
print(len(train_data))

df = pd.DataFrame(train_data) # convert train_data file into tensor
print(df.head())

# Raw data is almost ENTIRELY displaying "going forward, press W", unbalanced.
# Balance data into equal distribution of each situation to prevent overfitting to one situation.
# Set all quantities of data set to the quantity of the minimum value.

print(Counter(df[1].apply(str)))

lefts = []
forwards = []
rights = []

shuffle(train_data) # shuffle images to create generality, each image is its own general learning action

for data in train_data: # run through every data point in the training_data tensor [img, [A, W, D]]
    img = data[0]
    choice = data[1]
    
    if choice == [1, 0, 0]:
        lefts.append([img, choice])
    elif choice == [0, 1, 0]:
        forwards.append([img, choice])
    elif choice == [0, 0, 1]:
        rights.append([img, choice])
    else:
        print("no key matches to training image!")

# Equalize data list lengths
forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]

# add three lists into one big list
final_data = forwards + lefts + rights

shuffle(final_data)
print(len(final_data))
np.save("training_data_balanced_big.npy", final_data) # file name, tensor var to save to that file




# for data in train_data: # TRAIN_DATA: [image, keyvector[A, W, D] ]
#     img = data[0]
#     choice = data[1]
#     cv2.imshow("test", img) # display training data image
#     print(choice)
#     if cv2.waitKey(25) & 0XFF == ord("q"):
#         cv2.destroyAllWindows()
#         break
