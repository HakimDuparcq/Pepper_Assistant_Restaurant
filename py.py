#python 3.6.5 check masque
# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
from PIL import Image
#import qi
import argparse
import sys

def detruire():
    with open("C:/Users/hakdu/OneDrive/Bureau/pepper/memoire.txt", "w") as filout:
        filout.write("")

def fin_de_lia(a):
    with open("C:/Users/hakdu/OneDrive/Bureau/pepper/memoire.txt", "a") as filout:
        filout.write(a + "\n")

def cherche_image():
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    #frame = vs.read()
    #frame =Image.open(r"C:\Users\hakdu\Documents\Face-Mask-Detection-master\dataset\with_mask\327.jpg")
    frame = cv2.imread(r'C:/Users/hakdu/OneDrive/Bureau/pepper/image.jpg')

    frame = imutils.resize(frame, width=400)

    #cv2.destroyAllWindows()
    # show the output frame
    #cv2.imshow("Frame", frame)

    # detect faces in the frame and determine if they are wearing a
    # face mask or not
    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    # loop over the detected face locations and their corresponding
    # locations
    detruire()
    i=1
    for (box, pred) in zip(locs, preds):
        print("visage:",i)
        i=i+1
        # unpack the bounding box and predictions
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        # determine the class label and color we'll use to draw
        # the bounding box and text
        label = "Mask" if mask > withoutMask else "No Mask"
        #ECRIT MASK OU PAS MASK DANS LE TXT
        fin_de_lia(label)
        #print("label: ",label)
        #return (label)
        #color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
        # include the probability in the label
        #label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
        # display the label and bounding box rectangle on the output
        # frame
        #cv2.putText(frame, label, (startX, startY - 10),
            #cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        #cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)















def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()
    #print(detections.shape)

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face =  cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)

# load our serialized face detector model from disk
prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
maskNet = load_model("mask_detector.model")










iiii=1
iii=1
ii=1
aa=0
while aa==0:
    with open("C:/Users/hakdu/OneDrive/Bureau/pepper/memoire.txt", 'r') as filin:
        lignes = filin.readlines()
        for line in lignes:
            print ("voici_txt ", line)

        if len(lignes)!=0:
            if lignes[0]=="nouvelle photo\n":
                print('new picture')
                ii=1
                iii=1
                try:
                    cherche_image()
                    print("cherche image \n")
                except:
                    print("pas de visage")
                    print("\n")
            else:
                if ii==1:
                    print("no new picture")
                    print("\n")
                    ii=0
        else:
            if iii==1:
                print("txt vide")
                print("\n")
                iii=0


    key = cv2.waitKey(1) & 0xFF
    #print(label)
    #if the `q` key was pressed, break from the loop
    if key == ord("q"):
        a=1
        break

