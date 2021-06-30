import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
import csv
import requests
from bs4 import BeautifulSoup
import imutils
import time

def detruire():
    with open("C:/Users/hakdu/OneDrive/Bureau/pepper/memoireqrcode.txt", "w") as filout:
        filout.write("")

def ecrire(a):
    with open("C:/Users/hakdu/OneDrive/Bureau/pepper/memoireqrcode.txt", "w") as filout:
        filout.write(a)






#scan image qrcode enregistrée
def qrcode():
    image = cv2.imread(r'C:/Users/hakdu/OneDrive/Bureau/pepper/imageqrcode.jpg')
    image = imutils.resize(image, width=400)

    #cv2.destroyAllWindows()
    # show the output frame
    #cv2.imshow("Frame", image)


    #detruire()
    decodedObjects = pyzbar.decode(image)
    for obj in decodedObjects:
        #print ("Data:", obj.data)


        requete = requests.get(obj.data)
        page = requete.content
        soup = BeautifulSoup(page, "lxml")

        h1 = soup.find("p")
        print(h1.string)
        ecrire(h1.string)












iiii=1
iii=1
ii=1
aa=0
while aa==0:
    with open("C:/Users/hakdu/OneDrive/Bureau/pepper/memoireqrcode.txt", 'r') as filin:
        lignes = filin.readlines()
        for line in lignes:
            print ("voici_txt ", line)


        if (True):
            if (True):
                print('new picture')
                ii=1
                iii=1
                try:
                    qrcode()
                    print("cherche image \n")
                except:
                    print("pas de qrcode")
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

    time.sleep(0.5)


    key = cv2.waitKey(1) & 0xFF
    #print(label)
    #if the `q` key was pressed, break from the loop
    if key == ord("q"):
        a=1
        break


