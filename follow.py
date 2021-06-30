import qi
import argparse
import sys
import time
from naoqi import ALProxy
import paramiko




ip = "10.224.0.242"
tts = ALProxy("ALTextToSpeech", "10.224.0.242", 9559)
tts.setLanguage("French")

#stop choregraph
from naoqi import ALProxy
behaviors = ALProxy("ALBehaviorManager", "pepper.local", 9559)
behaviors.stopAllBehaviors()




def bumper():
    memory_service = session.service("ALMemory")
    if memory_service.getData("Device/SubDeviceList/Platform/FrontRight/Bumper/Sensor/Value") or memory_service.getData("Device/SubDeviceList/Platform/FrontLeft/Bumper/Sensor/Value") or memory_service.getData("Device/SubDeviceList/Platform/Back/Bumper/Sensor/Value"):
        return (0)
    else:
        return (1)


def slip(min,x,max):
    x=round(x,1)
    if x<min:
        return(min)
    elif x>max:
        return (max)
    else:
        return (x)


def main(session, faceSize):

    tts = ALProxy("ALTextToSpeech", "10.224.0.242", 9559)
    tts.setLanguage("French")
    
    # Get the services ALTracker and ALMotion.
    motion_service = session.service("ALMotion")
    tracker_service = session.service("ALTracker")

    motion_service.setOrthogonalSecurityDistance(0.25)
    motion_service.setTangentialSecurityDistance(0.05)

    # First, wake up.
    motion_service.wakeUp()

    #bras gauche mou
    names  = 'LArm'
    stiffnessLists  = 0.0
    timeLists  = 1.0
    motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)
    #time.sleep(1)
    


    # Get the services ALMotion & ALRobotPosture.
    motion_service  = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Pose Init
    #posture_service.goToPosture("StandInit", 0.5)

    # Example showing the use of moveToward
    x     = 0
    y     = 0.0
    theta = 0.0
    frequency = 1.0
    #motion_service.moveToward(x, y, theta)

    #avoir les angles
    motion_service  = session.service("ALMotion")
    memory_service = session.service("ALMemory")

    #exploration
    navigation_service = session.service("ALNavigation")
    # motion.moveTo(0.0, 0.0, - math.pi )
    navigation_service.stopLocalization()
    navigation_service.loadExploration("/home/nao/.local/share/Explorer/2021-06-17T152842.681Z.explo")
    # motion.moveTo(0.0, 0.0, - math.pi )
    

    #dialoge
    #tts.say("amenne moi a la table")

    #posture
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 1.0)



    tts.say("Bonjour montre moi ou son les tables mon amis")
    # while bumper():
        
 
    #     names         = "Body"
    #     useSensors    = False
    #     commandAngles = motion_service.getAngles(names, useSensors)

    #     useSensors  = True
    #     sensorAngles = motion_service.getAngles(names, useSensors)

    #     names  = 'LArm'
    #     stiffnessLists  = 0.0
    #     timeLists  = 0.1
    #     motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

    #     vitessex=slip(-0.4, float(commandAngles[2]/3), 0.4)*(-1)
    #     vitessey=slip(-0.4, float(commandAngles[6]/3), 0.4)*(-1)
    #     print('ok',vitessex,'ok', vitessey)
    #     motion_service.moveToward(vitessex, y, vitessey)
    #     time.sleep(0.3)
        
    #     navigation_service.startLocalization()
    #     print "I reached: " + str(navigation_service.getRobotPositionInMap()[0])
    #     #navigation_service.stopLocalization()
    time.sleep(2)

    guess = [0., 0. ,0.]
    navigation_service.relocalizeInMap(guess)
    navigation_service.startLocalization()






    #posture
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 1.0)



    table=0
    TABLE=[]
    while table<3:
        table=table+1
        tts.say("allons a la table"+ str(table))
        while bumper():

            #affiche les angles
            names         = "Body"
            useSensors    = False
            commandAngles = motion_service.getAngles(names, useSensors)
            # print "Command angles:"
            # print str(commandAngles)
            # print ""
            useSensors  = True
            sensorAngles = motion_service.getAngles(names, useSensors)
            # print "Sensor angles:"
            # print str(sensorAngles)
            # print ""

            #bras gauche mou
            names  = 'LArm'
            stiffnessLists  = 0.0
            timeLists  = 0.1
            motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

            vitessex=slip(-0.4, float(commandAngles[2]/3), 0.4)*(-1)
            vitessey=slip(-0.4, float(commandAngles[6]/3), 0.4)*(-1)
            print('ok',vitessex,'ok', vitessey)
            motion_service.moveToward(vitessex, y, vitessey)
            time.sleep(0.3)
            
            navigation_service.startLocalization()
            #print "I reached: " + str(navigation_service.getRobotPositionInMap()[0])
            #navigation_service.stopLocalization()
        time.sleep(2)

        TABLE.append(navigation_service.getRobotPositionInMap()[0])

    print("position des tables: ",TABLE)
    tab=""
    tab=str(TABLE[0]) + ";" + str(TABLE[1]) + ";" + str(TABLE[2])
    memory_service.insertData("oktest", tab)
    print(memory_service.getData("oktest"))

    
    motion_service.moveToward(0, 0, 0)
    tts.say("Merci")
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


