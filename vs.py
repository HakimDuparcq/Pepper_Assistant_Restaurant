import time
import paramiko
from naoqi import ALProxy

#a la suite dans visueal studio code python 2.7.18
def ecrire(a):
    with open("C:/Users/hakdu/OneDrive/Bureau/pepper/memoire.txt", "w") as filout:
        filout.write(a + "\n")




def prendre_photo():
    IP = "10.224.0.242"
    PORT = 9559

    # prendre une photo sur pepper et stocker dans recordings-cameras
    photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
    photoCaptureProxy.setResolution(3)
    photoCaptureProxy.setPictureFormat("jpg")
    photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
    # connection pc - pepper via SSH
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="10.224.0.242",username="nao",password="PepperISEN")
    ftp_client=ssh_client.open_sftp()
    ftp_client.get("recordings/cameras/image.jpg","C:/Users/hakdu/OneDrive/Bureau/pepper/image.jpg")
    ftp_client.close()

    #ecrire('nouvelle photo')
    #time.sleep(4)
    print("j'ai pris une nouvelle photos...")


tts = ALProxy("ALTextToSpeech", "10.224.0.242", 9559)
tts.setLanguage("French")
def main(session):
    tts = session.service("ALTextToSpeech")

while True:
    prendre_photo()
    ecrire('nouvelle photo')
    
    time.sleep(1)
    
    masque_ou_pas = open("memoire.txt", "r")
    lines=masque_ou_pas.readlines()
    for line in lines:
        print("txt: ",line)
    #print(masque_ou_pas)
    #tempo=lines
    #while tempo==lines:
        #masque_ou_pas = open("memoire.txt", "r")
        #lines=masque_ou_pas.readlines()
        #for line in lines:
            #print("txt: ",line)
            #print(masque_ou_pas)


    if len(lines)!=0:
        if len(lines)==1:
            if 'Mask\n' in lines:
                tts.say("une personne avec masque")
            else :
                tts.say("une personne sans masque")
        if len(lines)==2:
            if 'Mask\n' in lines and 'No Mask\n' in lines:
                tts.say("une personne avec masque, et une personne sans masque")


    else:
        print("pas de visage")


    # if len(lines)!=0:
    #     #if lines[0] =='Mask\n' or lines[0] =='No Mask\n':
    #         tts = ALProxy("ALTextToSpeech", "10.224.0.242", 9559)
    #         tts.setLanguage("French")
    #         def main(session):
    #             tts = session.service("ALTextToSpeech")

    #         if (lines[0]=='Mask'):
    #             tts.say("merci d'avoir mis votre masque'")
    #         else:
    #             tts.say("veuillez mettre votre masque s'il vous plait")
    # else:
    #     print("pas de visage")

