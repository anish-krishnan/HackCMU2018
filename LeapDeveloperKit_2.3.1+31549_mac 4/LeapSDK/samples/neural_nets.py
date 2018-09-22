import tensorflow as tf
from tensorflow import keras
import numpy as np
from convertNumpy import getData
import csv 
import io


def buildModel():
	model = keras.Sequential();
	model.add(keras.layers.Dense(45, activation='relu'))
	# Add another:
	model.add(keras.layers.Dense(45, activation='relu'))
	# Add a softmax layer with 26 output units:
	model.add(keras.layers.Dense(26, activation='softmax'))

	model.compile(optimizer=tf.train.AdamOptimizer(0.001),
				  loss='categorical_crossentropy',
				  metrics=['accuracy'])

	(train_data,train_labels,val_data,val_labels)=getData()

	model.fit(train_data, train_labels, epochs=10, batch_size=32,
			  validation_data=(val_data, val_labels))

	return model

# def readCSV(path):
# 		info = []

# 		with io.open(path, encoding='utf-8') as file:
# 			reader = csv.reader(file)
# 			for row in reader:
# 				try: info.append(row)
# 				except: continue
# 		return info

# def getElement():
# 	fullList = []
# 	lettera = ord("a")
# 	for i in range(3):
# 		data = readCSV(("%s.csv" % chr(lettera+i)))
# 		fullList.extend(data)

# 	from random import shuffle
# 	shuffle(fullList)

# 	letterDict = dict()
# 	for i in range(26):
# 		arr = [0]*26
# 		arr[i] = 1
# 		letterDict[chr(ord("a")+i)]=arr
# 	letterList = []
# 	vectorList = []
# 	for i in fullList:
# 		letterList.append(letterDict[i[0]])
# 		vectorList.append(i[1:])
# 	print(letterList[0])
# 	return (np.matrix(vectorList[0]))

def predictLetter(model,element,threshold):
	letterDict = dict()
	for i in range(26):
		arr = [0]*26
		arr[i] = 1
		letterDict[chr(ord("a")+i)]=arr
	array=model.predict(element)
	i=np.argmax(array)
	if (array[0][i]>=threshold):
		return chr(ord("a")+i)
	return ""