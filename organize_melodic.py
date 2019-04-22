# Date: 4/4/2019
# Author: Brandon Lucas
# Research Professor: Dr. Ian McDonough

# what modules do we need?
import os
import sys
import tensorflow as tf
import keras
from keras.layers import Dense, Flatten
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout
from keras.models import Sequential
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from organize_melodic_functions import *

orig_dir = input('Enter the origin folder: ')
data_dir = input('Enter the destination folder: ')

try:
    os.chdir(orig_dir)
except:
    print('Could not change to that directory')
    sys.exit(0)

artifact_images = []
non_artifact_images = []
for root, dirs, files in os.walk(data_dir):
    for directory in dirs:
        # make this an option later
        if "Preclin" in directory:
            os.chdir(directory)
            # the files that indicate which id's are artifacts
            artifact_numbers_file = open("fix_s8.txt")
            line = artifact_numbers_file.readline()
            artifact_numbers_file.close()
            artifact_numbers = line.strip().split(",")
            thresh_files = getFiles(root + '/' + directory, "thresh")
            # loop through the thresh files
            for file_path in thresh_files:
                filename = file_path.split("/")[-1]
                id = filename.split("_")[1]
                if id in artifact_numbers:
                    artifact_images.append(file_path)
                else:
                    non_artifact_images.append(file_path)
        os.chdir(root)

data = []
labels = []
for artifact_image in artifact_images:
    try:
        image = mpimg.imread(artifact_image, 3)
        image_from_array = Image.fromarray(image, 'RGB')
        size_image = image_from_array.resize((992, 4167))
        labels.append(1)
    except:
        print("Whoopsie! ")

for non_artifact_image in non_artifact_images:
    try:
        image = mpimg.imread(non_artifact_image, 3)
        image_from_array = Image.fromarray(image, 'RGB')
        size_image = image_from_array.resize((992, 4167))
        labels.append(0)
    except:
        print("Whoopsie! ")

df = np.array(data)
labels = np.array(labels)
(X_train, X_test) = df[(int)(0.1*len(df)):],df[:(int)(0.1*len(df))]
(y_train, y_test) = labels[(int)(0.1*len(labels)):],labels[:(int)(0.1*len(labels))]

X_train = np.arange(X_train.shape[0])/255.0

s=np.arange(X_train.shape[0])
np.random.shuffle(s)
X_train=X_train[s]
y_train=y_train[s]
X_train = X_train/255.0
X_train

model=Sequential()
model.add(Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(50,50,3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32,kernel_size=2,padding="same",activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64,kernel_size=2,padding="same",activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(500,activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(2,activation="softmax"))#2 represent output layer neurons
model.summary()

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
             metrics=["accuracy"])

model.fit(X_train,y_train, epochs=10)
X_loss, accuracy = model.evaluate(X_test,y_test)

print(accuracy)
print(X_loss)
