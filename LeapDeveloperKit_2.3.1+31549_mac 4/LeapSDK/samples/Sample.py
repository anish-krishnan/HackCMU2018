################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
import sys
import csv
import string
sys.path.insert(0, 
"/Users/anishkrishnan/GitHub/HackCMU2018/LeapDeveloperKit_2.3.1+31549_mac 4/LeapSDK/lib")

import Leap, thread, time, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from neural_nets import * 
from random import shuffle

from os import system

def load_model():
	global model
	model = buildModel()
	# this is key : save the graph after loading the model
	global graph
	graph = tf.get_default_graph()
	
class SampleListener(Leap.Listener):
	word = ""
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
	
	
	@staticmethod
	def makeDict(L):
		myDict = dict()
		
		for i in range(len(L)):
			myDict[str(i)] = L[i]
		return myDict

	
	@staticmethod
	def convertToVector(L):
		#palm coordinates 
		xp,yp,zp = L[0]
		newList = []
		for i in range(1,len(L)):
			#finger coordinates 
			xf,yf,zf = L[i]
			unitVector = math.sqrt((xf -xp)**2 + (yf - yp)**2 + (zf - zp)**2)
			vector = [(xf - xp)/(unitVector), (yf-yp)/(unitVector), (zf-zp)/(unitVector)]
			newList.extend(vector)
		return newList 

	def on_init(self, controller):
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

		# Enable gestures
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"

	def on_frame(self, controller):
		# Get the most recent frame and report some basic information
		frame = controller.frame()

		# print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
		#       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

		# Get hands
		for hand in frame.hands:
			
			handFrameList = []

			handType = "Left hand" if hand.is_left else "Right hand"

			# print "  %s, id %d, position: %s" % (
			#     handType, hand.id, hand.palm_position)
			# print("     HAND {", handType, "}:", str(hand.palm_position))
			
			handFrameList.append([hand.palm_position[0], hand.palm_position[1], hand.palm_position[2]])

			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction

			# Calculate the hand's pitch, roll, and yaw angles
			# print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
			#     direction.pitch * Leap.RAD_TO_DEG,
			#     normal.roll * Leap.RAD_TO_DEG,
			#     direction.yaw * Leap.RAD_TO_DEG)

			# Get arm bone
			arm = hand.arm
			# print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
			#     arm.direction,
			#     arm.wrist_position,
			#     arm.elbow_position)
			# print("     WRIST: ", str(arm.wrist_position))

			# Get fingers
			for finger in hand.fingers:

				# print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
				#     self.finger_names[finger.type],
				#     finger.id,
				#     finger.length,
				#     finger.width)

				# Get bones
				for b in range(1, 4):
					bone = finger.bone(b)
					# print "      Bone: %s, start: %s, end: %s, direction: %s" % (
					#     self.bone_names[bone.type],
					#     bone.prev_joint,
					#     bone.next_joint,
					#     bone.direction)
					# print "         Bone:", b, str(bone.next_joint)
					handFrameList.append([bone.next_joint[0], bone.next_joint[1], bone.next_joint[2]])
						
			
			inputNode = SampleListener.convertToVector(handFrameList)
			
		
			
			with open('temp.csv', mode='w') as csv_file:
				wr = csv.writer(csv_file, dialect='excel')
				wr.writerow(inputNode)
			csv_file.close()
			
			fullList = []
			def readCSV(path):
				info = []
		
				with io.open(path, encoding='utf-8') as file:
					reader = csv.reader(file)
					for row in reader:
						try: info.append(row)
						except: continue
				return info
			data = readCSV("temp.csv")
			fullList.extend(data)
			shuffle(fullList)
			
			numList = []
			for i in fullList[0]:
				numList.append(float(i))
			
			numpyMatrix = (np.matrix(numList))
			threshold = .97
			

			#numpyMatrix = (np.matrix(np.array(inputNode))).transpose()
			#print(numpyMatrix)
			#print(numpyMatrix.shape)
			#letter = predictLetter(model, numpyMatrix, .8)
			with graph.as_default():
				array=model.predict(numpyMatrix)
				i=np.argmax(array)
				if (array[0][i]>=threshold):
					if i == 26:
						letter = " " 
						sayStr = "say " + "space"
					else:
						letter = chr(ord("a")+i)
						sayStr = "say " + letter
					system(sayStr)
					SampleListener.word += letter
					
					
			print(SampleListener.word)
			if SampleListener.word in string.whitespace or SampleListener.word == "":
				sayStr = "say no word"
			else:
				sayStr = "say " + str(SampleListener.word)
			system(sayStr)
			
			if len(SampleListener.word) > 4:
				SampleListener.word = ""
			
			time.sleep(0.5)
			
			
			
			
			
			
			
			
			
			
			
				
		
			
			"""
			print("ALTERED")
			print(inputNode)
			print ""
			print handFrameList
			print str(len(handFrameList)) + "\n\n"
			
			with open('space.csv', mode='a') as csv_file:
				wr = csv.writer(csv_file, dialect='excel')
				wr.writerow(["space"] + inputNode)
			csv_file.close()
			"""

		# Get tools
		for tool in frame.tools:

			print "  Tool id: %d, position: %s, direction: %s" % (
				tool.id, tool.tip_position, tool.direction)

		# Get gestures
		# for gesture in frame.gestures():
		#     if gesture.type == Leap.Gesture.TYPE_CIRCLE:
		#         circle = CircleGesture(gesture)

		##           # Determine clock direction using the angle between the pointable and the circle normal
		#         if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
		#             clockwiseness = "clockwise"
		#         else:
		#             clockwiseness = "counterclockwise"

		##           # Calculate the angle swept since the last frame
		#         swept_angle = 0
		#         if circle.state != Leap.Gesture.STATE_START:
		#             previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
		#             swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

		##           print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
		#                 gesture.id, self.state_names[gesture.state],
		#                 circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

		##       if gesture.type == Leap.Gesture.TYPE_SWIPE:
		#         swipe = SwipeGesture(gesture)
		#         print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
		#                 gesture.id, self.state_names[gesture.state],
		#                 swipe.position, swipe.direction, swipe.speed)

		##       if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
		#         keytap = KeyTapGesture(gesture)
		#         print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
		#                 gesture.id, self.state_names[gesture.state],
		#                 keytap.position, keytap.direction )

		##       if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
		#         screentap = ScreenTapGesture(gesture)
		#         print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
		#                 gesture.id, self.state_names[gesture.state],
		#                 screentap.position, screentap.direction )

		if not (frame.hands.is_empty and frame.gestures().is_empty):
			print ""

	def state_string(self, state):
		if state == Leap.Gesture.STATE_START:
			return "STATE_START"

		if state == Leap.Gesture.STATE_UPDATE:
			return "STATE_UPDATE"

		if state == Leap.Gesture.STATE_STOP:
			return "STATE_STOP"

		if state == Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"

def init(data):
	# load data.xyz as appropriate
	data.symbols = PhotoImage(file = "Letters/symbols2.gif")
	data.logo = PhotoImage(file = "syneLogo.gif")
	data.axy = [75,100]
	data.imagePosition = [200, 250]
	data.line = [data.imagePosition[0]+50,data.imagePosition[1]-30, data.imagePosition[0]+300, data.imagePosition[1]-30] 
	data.textString = "Hi"
	data.textLocation = [data.line[0] + 20,data.line[1] - 25]
	
def mousePressed(event, data):
	# use event.x and event.y
	print(event.x, event.y)

def keyPressed(event, data):
	# use event.char and event.keysym
	pass

def timerFired(data):
	pass
	

def redrawAll(canvas, data):
	
	canvas.create_rectangle(0, 0, 750, 1200, fill='#80DEEA')
	data.textString += getLetter()
	
	# draw in canvas
	
	canvas.create_image(0, 0, anchor=NW, image = data.logo)
	canvas.create_image(tuple(data.imagePosition), anchor = NW, image = data.symbols)
	#canvas.create_image(1400, 780, anchor = SE, image = data.logo)
	#word we're typing out 
	canvas.create_text(tuple(data.textLocation), text = data.textString, font = "Helvitica 35")
	canvas.create_line(tuple(data.line), width = 5)
def run(width=300, height=300):
	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)





if __name__ == "__main__":
	load_model()
	run(750, 1200)
