import csv
import io
import numpy as np

def getData():
	def readCSV(path):
		info = []

		with io.open(path, encoding='utf-8') as file:
			reader = csv.reader(file)
			for row in reader:
				try: info.append(row)
				except: continue
		return info 

	fullList = []
	lettera = ord("a")
	for i in range(3):
		data = readCSV(("%s.csv" % chr(lettera+i)))
		fullList.extend(data)

	from random import shuffle
	shuffle(fullList)

	letterDict = dict()
	for i in range(26):
		arr = [0]*26
		arr[i] = 1
		letterDict[chr(ord("a")+i)]=arr

	letterList = []
	vectorList = []
	
	for i in fullList:
		letterList.append(letterDict[i[0]])
		vectorList.append(i[1:])
	trainNum = len(letterList)*4/5
	trainingLetter = letterList[:trainNum]
	trainingVector = vectorList[:trainNum]

	testLetter = letterList[trainNum:]
	testVector = vectorList[trainNum:]

	trainingLetter = np.array(trainingLetter)
	trainingVector = np.array(trainingVector)
	testLetter = np.array(testLetter)
	testVector = np.array(testVector)

	return (trainingVector,trainingLetter,testVector,testLetter)