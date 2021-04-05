from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import getImage

import numpy as np
import pandas as pd
import os ,glob
import tensorflow as tf
import keras
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from keras.utils import normalize
from PIL import Image
import warnings
from tensorflow.keras.models import load_model
warnings.filterwarnings("ignore")

parentFolderRelativePath = settings.BASE_DIR

# Create your views here.

def detect_view(request):
    # logic
    return render(request,'Brain_tumor_detection/detect.html')


tumorPrediction = {
    "result" : False,
    "percent_accuracy" : 0,
}


def index(request):
    if request.method == "POST":
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            clearFolder()
            form.save()
            # testAndDisplayResult()
            obj = form.instance
            return render(request, "Brain_tumor_detection/detect.html", {"obj": obj, "predict":tumorPrediction })
    else:
        form = ImageForm()
    img = getImage.objects.all()
    return render(request, "Brain_tumor_detection/detect.html", {"img": img, "form": form})


def getImagePath():
    # parentPath = 'C:/Users/prasad/PycharmProjects/djangoFinalProject/media/img/'
    imageFolder = os.path.join(parentFolderRelativePath, 'media/img/')

    imageList = os.listdir(imageFolder)
    imageName = imageList[0]
    imagePath = ''

    if len(imageList) == 0: # check for empty folder
        print("Folder is Empty")
    else:
        imagePath = os.path.join(imageFolder, imageName)
        print(imagePath)

    return imagePath


def clearFolder():
    # parentPath = 'C:/Users/prasad/PycharmProjects/djangoFinalProject/media/img/'

    imgFolder = os.path.join(parentFolderRelativePath, 'media/img/')
    filelist = glob.glob(os.path.join(imgFolder, "*")) # to get all images inside folder
    for f in filelist:
        os.remove(f)

# def copyImage():
#     destination = 'Brain_tumor_detection/templates/Brain_tumor_detection/'
#     shutil.copy(getImagePath(), destination)


def testAndDisplayResult():

    # model2 = load_model('C:/Users/prasad/PycharmProjects/djangoFinalProject/model/')

    modelFolder = os.path.join(parentFolderRelativePath, 'model/')
    model2 = load_model(modelFolder)
    # copyImage()


    img_path = getImagePath()
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    img_data = preprocess_input(x)

    # make prediction
    result = model2.predict(img_data)
    print(result)

    result[0][0]  # n

    result[0][1]  # y

    accuracy_percent = int(result[0][0] * 100)
    print("Healthy Brain probability - " + str(int(result[0][0] * 100)) + "%")  # non_tumor -- healthy
    print("Tumorous Brain Image probability - " + str(int(result[0][1] * 100)) + "%")  # tumor --

    # if rs[0][0] >= 0.6:
    #     prediction = 'This image is NOT tumorous.'
    if (result[0][1] >= 0.60 and (result[0][1] > result[0][0])):
        prediction = 'Warning! This image IS tumorous.'
        tumorPrediction["result"] = True
    else:
        prediction = 'This image is NOT tumorous.'
        tumorPrediction["result"] = False

    tumorPrediction["percent_accuracy"] = accuracy_percent
    print(prediction)


def getPrediction():
    return tumorPrediction
