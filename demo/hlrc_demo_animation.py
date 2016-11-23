#!/usr/bin/python
import logging
from hlrc_client import *
import time
import sys
import random

if __name__ == "__main__":
	icub = RobotController("ROS", "/icub", loglevel=logging.DEBUG)

	# activate a neutral face
	icub.set_default_emotion(RobotEmotion(RobotEmotion.NEUTRAL))

	# look straight
        straight = RobotGaze(0,0,0)
        icub.set_gaze_target(straight)

        # say hello
	time.sleep(1.0)
	icub.set_current_emotion(RobotEmotion(RobotEmotion.HAPPY))
        icub.set_speak("Hello. My name is iCub. Welcome to this demonstration", blocking=True)

	# look at some random targets 
	gazetarget = [[0, -1], [15, 8], [-10, 5], [5, -5], [-11, -11]]
	icub.set_speak("I will now look at random locations", blocking=True)
	for location in gazetarget:
		target = RobotGaze(location[0], location[1], 0.0)
		icub.set_gaze_target(target)
		time.sleep(0.5 + random.uniform(0.5, 1.0))

	icub.set_gaze_target(straight)
	icub.set_speak("I can keep the visual focus even when i shake my head")
	time.sleep(0.5)

	#execute head shake animation
	ani = RobotAnimation(RobotAnimation.HEAD_SHAKE)
	ani.repetitions = 3
	icub.set_head_animation(ani, blocking=True)

	# goodbye eyeblink
	time.sleep(1.0)
	icub.set_speak("thanks for watching")
	time.sleep(0.5)
	icub.set_head_animation(RobotAnimation(RobotAnimation.EYEBLINK_R), blocking=True)
	
