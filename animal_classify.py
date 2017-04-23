from bs4 import BeautifulSoup
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
#from sklearn.decomposition import RandomizedPCA
import pylab as pl
import numpy as np
import requests
import re
import urllib2
import os
import base64
import pandas as pd
from StringIO import StringIO




# #setup a standard image size; this will distort some images but will get everything into the same shape
STANDARD_SIZE = (300, 167)
def img_to_matrix(filename, verbose=False):
    """
    takes a filename and turns it into a numpy array of RGB pixels
    """
    img = Image.open(filename)
    if verbose==True:
        print "changing size from %s to %s" % (str(img.size), str(STANDARD_SIZE))
    img = img.resize(STANDARD_SIZE)
    img = list(img.getdata())
    img = map(list, img)
    img = np.array(img)
    return img

def flatten_image(img):
    """
    takes in an (m, n) numpy array and flattens it
    into an array of shape (1, m * n)
    """
    s = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1, s)
    return img_wide[0]


img_dir = "images/"
images = [img_dir+ f for f in os.listdir(img_dir)]
labels = ["whale" if "whale" in f.split('/')[-1] else "porcupine" for f in images]

data = []
for image in images:
    img = img_to_matrix(image)
    #print img
    img = flatten_image(img)
    #print img
    data.append(img)

data = np.array(data)
data

# Creating Features
is_train = np.random.uniform(0, 1, len(data)) <= 0.7
y = np.where(np.array(labels)=="whale", 1, 0)

train_x, train_y = data[is_train], y[is_train]
test_x, test_y = data[is_train==False], y[is_train==False]

#pca = RandomizedPCA(n_components=2)
#pca = PCA(n_components=2, svd_solver='randomized')
#X = pca.fit_transform(data)
#X = pca.fit(data)

# Randomized PCA to create features
pca = PCA(n_components=2, svd_solver='randomized').fit(data)

X = pca.transform(data)
#print X[:,0]
#print X[:,1]

d = {   'x': X[:, 0],
        'y': X[:, 1],
        "label": np.where(y == 1, "whale", "porcupine")}

df = pd.DataFrame(d)
colors = ["red", "yellow"]
for label, color in zip(df['label'].unique(), colors):
    mask = df['label']==label
    pl.scatter(df[mask]['x'], df[mask]['y'], c=color, label=label)
pl.legend()
#pl.show()

# randomized pca in 5 dimensions
pca = PCA(n_components=5)
train_x = pca.fit_transform(train_x)
test_x = pca.transform(test_x)

train_x[:5]
knn = KNeighborsClassifier()
knn.fit(train_x, train_y)

pd.crosstab(test_y, knn.predict(test_x), rownames=["Actual"], colnames=["Predicted"])

def string_to_img(image_string):
    print "called string_to_image"
    #we need to decode the image from base64
    image_string = base64.decodestring(image_string)
    #since we're seing this as a JSON string, we use StringIO so it acts like a file
    img = StringIO(image_string)
    #img = PIL.Image.open(img)
    img = Image.open(img)
    img = img.resize(STANDARD_SIZE)
    img = list(img.getdata())
    img = map(list, img)
    img = np.array(img)
    s = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1, s)
    return pca.transform(img_wide[0])

def classify_image(data):
    print "called classify_image"
    data.reshape(-1,1)
    preds = knn.predict(data)
    print "pres is: "
    print preds
    preds = np.where(preds==1, "whale", "porcupine")
    pred = preds[0]
    #print pred
    return {"image_label": pred}


def execute(data):
    print "called execute"
    #img_string = data.get("image_as_base64_string", None)
    #print data
    img_string = data
    if img_string is None:
        return {"status": "error", "message": "data was None", "input_data": data}
    else:
        img = string_to_img(img_string)
        pred = classify_image(img)
        return pred


# # i don't have the image data set any more
# # so just some dummy data to get it to work :(
# new_image = open("input/p1.jpg", 'rb').read()
#
# #we need to make the image JSON serializeable
# new_image = base64.encodestring(new_image)
#
# #yh.predict("ImageClassifier", {"image_as_base64_string": new_image})
# execute(new_image)

import sys
if __name__ == '__main__':
    filePath = "./imgs/"
    fileName = "filename.jpg"#sys.argv[1]
    finalFile = filePath + fileName
    print("hehehe")
    w1 = open(finalFile, 'rb').read()
    w1 = base64.encodestring(w1)
    print execute(w1)

# w2 = open("input/w2.jpg", 'rb').read()
# w2 = base64.encodestring(w2)
# print execute(w2)
#
# w3 = open("input/w3.jpg", 'rb').read()
# w3 = base64.encodestring(w3)
# print execute(w3)
#
# p1 = open("input/p1.jpg", 'rb').read()
# p1 = base64.encodestring(p1)
# print execute(p1)
#
# p2 = open("input/p2.jpg", 'rb').read()
# p2 = base64.encodestring(p2)
# print execute(p2)
#
# p3 = open("input/p3.jpg", 'rb').read()
# p3 = base64.encodestring(p3)
# print execute(p3)
