import qi
import argparse
import sys
import time
from naoqi import ALProxy
import paramiko




ip = "10.224.0.242"
tts = ALProxy("ALTextToSpeech", "10.224.0.242", 9559)
tts.setLanguage("French")






def main(session, faceSize):

    tts = ALProxy("ALTextToSpeech", "10.224.0.242", 9559)
    tts.setLanguage("French")
    
    # Get the services ALTracker and ALMotion.
    motion_service = session.service("ALMotion")
    tracker_service = session.service("ALTracker")
    posture_service = session.service("ALRobotPosture")
    memory_service = session.service("ALMemory")



    TABLE=[1,2,3]
    motion_service  = session.service("ALMotion")
    memory_service = session.service("ALMemory")
    memory_service.insertData("oktest", "ok")
    time.sleep(3)
    print(memory_service.getData("oktest"))


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





