from naoqi import ALProxy
behaviors = ALProxy("ALBehaviorManager", "pepper.local", 9559)
behaviors.stopAllBehaviors()