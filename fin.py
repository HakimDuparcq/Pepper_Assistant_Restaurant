"""Example: Use Tracking Module to Track a Face"""
import qi
import argparse
import sys
import time
from naoqi import ALProxy
import paramiko
from naoqi import ALProxy



ip = "10.224.0.242"
tts = ALProxy("ALTextToSpeech", "10.224.0.242", 9559)
tts.setLanguage("French")

#stop choregraph
from naoqi import ALProxy
behaviors = ALProxy("ALBehaviorManager", "pepper.local", 9559)
behaviors.stopAllBehaviors()



def ecrire(fichier,a):
    l="C:/Users/hakdu/OneDrive/Bureau/pepper/" + fichier
    with open(l, "w") as filout:
        filout.write(a + "\n")

def prendre_photo(fichier):
    IP = "10.224.0.242"
    PORT = 9559

    # prendre une photo sur pepper et stocker dans recordings-cameras
    photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
    photoCaptureProxy.setResolution(2)
    photoCaptureProxy.setPictureFormat("jpg")
    photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")
    # connection pc - pepper via SSH
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="10.224.0.242",username="nao",password="PepperISEN")
    ftp_client=ssh_client.open_sftp()
    ftp_client.get("recordings/cameras/image.jpg","C:/Users/hakdu/OneDrive/Bureau/pepper/" + fichier )
    ftp_client.close()

    #ecrire1('nouvelle photo')
    #time.sleep(4)
    print("j'ai pris une nouvelle photos...")





def main(session, faceSize):
    """
    This example shows how to use ALTracker with face.
    """
    # Get the services ALTracker and ALMotion.

    motion_service = session.service("ALMotion")
    # tracker_service = session.service("ALTracker")

    # # First, wake up.
    motion_service.wakeUp()

    # # Add target to track.
    # targetName = "Face"
    # faceWidth = faceSize
    # tracker_service.registerTarget(targetName, faceWidth)

    # # Then, start tracker.
    # tracker_service.track(targetName)
    # print "ALTracker successfully started, now show your face to pepper!"
    # print "Use Ctrl+c to stop this script."
    

    b=1  #pour pas dire tout le temps bonjour
    try:
        while True:
            #stop choregraphe
            from naoqi import ALProxy
            behaviors = ALProxy("ALBehaviorManager", "pepper.local", 9559)
            behaviors.stopAllBehaviors()

            #time.sleep(1)
            tracker_service = session.service("ALTracker")
            # Add target to track.
            targetName = "Face"
            faceWidth = faceSize
            tracker_service.registerTarget(targetName, faceWidth)
            tracker_service.track(targetName)

            print(tracker_service.isTargetLost())
            if not tracker_service.isTargetLost(): #si y a qq alors bonjour
                if b==1:
                    tts.say('Bonjour je suis peppeur votre assistant aujourdhui au labo robotique')

                #masque
                prendre_photo('image.jpg')
                ecrire('memoire.txt','nouvelle photo')
                
                time.sleep(1)
                
                masque_ou_pas = open("memoire.txt", "r")
                lines=masque_ou_pas.readlines()
                for line in lines:
                    print("txt: ",line)
                if len(lines)!=0:
                    if len(lines)==1:
                        if 'Mask\n' in lines:
                            tts.say("Merci d'avoir mis ton masque")
                            tts.say("Praisentez votre q r code de raiservation")
                            b=1
                            #qrcode
                            a=1
                            while a==1:
                                prendre_photo('imageqrcode.jpg')
                                ecrire('memoireqrcode.txt','nouvelle photo')
                                    

                                time.sleep(1)
                                    
                                masque_ou_pas = open("memoireqrcode.txt", "r")
                                lines=masque_ou_pas.readlines()
                                for line in lines:
                                    print("txt: ",line)
                                    

                                if len(lines)!=0 and 'nouvelle photo\n' not in lines:
                                    tts.say(lines[0])
                                    a=0

                                    # Stop tracker.
                                    tracker_service.stopTracker()
                                    tracker_service.unregisterAllTargets()
                                    #motion_service.rest()


                                    #run come choregraph
                                    behavior = ALProxy("ALBehaviorManager", "10.224.0.242", 9559)
                                    behavior.runBehavior("pepperaccueilchoregraphe-5bb186/behavior_1")
        




                            
                        else :
                            tts.say("Mets ton masque s'il te plait")
                            b=0
                    if len(lines)==2:
                        if 'Mask\n' in lines and 'No Mask\n' in lines:
                            tts.say("une personne avec masque, et une personne sans masque")
                        if 'Mask\n' not in lines:
                            tts.say("mettez tout les deux votre masque")
                        if 'No Mask\n' not in lines:
                            tts.say("Merci d'avoir tout les deux mis votre masque")
                        
                else:
                    tts.say("eh oh je suis la")
                    b=0
                    print("pas de visage")

        tts.say("je suis finito")     
            
    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."

    # Stop tracker.
    tracker_service.stopTracker()
    tracker_service.unregisterAllTargets()
    #motion_service.rest()

    print "ALTracker stopped."


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=ip,
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--facesize", type=float, default=0.1,
                        help="Face width.")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.facesize)