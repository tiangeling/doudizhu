import numpy as np
import os, sys
def preProcessHand(hand, pokerValue):
	pokerDict = dict([("3",0),("4",0),("5",0),("6",0),("7",0),("8",0),("9",0),("10",0),("j",0),("q",0),("k",0),("a",0),("2",0),("ltg",0),("wcy",0)])
	for i in range(len(hand)):
		pokerDict[hand[i]] += 1
	return pokerDict
	


def dumbGrade(pokerDict, pokerValue):
	grade = 0
	if (pokerDict["wcy"]!=0 and pokerDict["ltg"] !=0):
		grade += 150 #king
		pokerDict["wcy"] = 0
		pokerDict["ltg"] = 0
	for key in pokerDict:
		grade += pokerDict[key] * pokerValue[key]

	return grade

def getStreak(pokerDict):
	streakEnd = 0 #exclusive
	streakLength = 0
	curEnd = 0 #exclusive
	curLength = 0
	keyList = pokerDict.keys()
	streak = []
	for i in range(len(keyList)):
		curKey = keyList[i]
		if ((pokerDict[curKey]) > 0):
			curLength += 1
		else:
			curLength = 0
		curEnd += 1
		if (curLength >= 5) and (curLength >= streakLength):
				streakLength = curLength
				streakEnd = curEnd
	if (streakLength != 0):
		for i in range(streakEnd - streakLength, streakEnd):
			streak.append(keyList[i])

		return streak
	else:
		return None

def removeStreak(pokerDict, streak):
	j = 0
	keyList = pokerDict.keys()
	for i in range(len(streak)):
		while (j < len(keyList)):
			if (keyList[j] == streak[i]):
				pokerDict[keyList[j]] -= 1
				j += 1
				break
			j += 1
	return pokerDict

def gradehand(pokerDict, pokerValue, grade, gradeList):

	for key in pokerDict:
		if (pokerDict[key] == 4):
			pokerDict_4 = pokerDict.copy()
			pokerDict_4[key] -= 4
			tempGrade_4 = grade + 10*pokerValue[key]
			gradeList.append(gradehand(pokerDict_4, pokerValue, tempGrade_4, gradeList))
		streak = getStreak(pokerDict)
		if (streak != None):
			pokerDict_S = pokerDict.copy()
			pokerDict_S = removeStreak(pokerDict_S, streak)
			streakLength = len(streak)
			tempGrade_S = grade + streakLength * pokerValue[streak[streakLength//2]]
			gradeList.append(gradehand(pokerDict_S, pokerValue, tempGrade_S, gradeList))
		if (pokerDict[key] == 3):
			pokerDict_3 = pokerDict.copy()
			pokerDict_3[key] -= 3
			tempGrade_3 = grade + 5*pokerValue[key]
			gradeList.append(gradehand(pokerDict_3, pokerValue, tempGrade_3, gradeList))
		if (pokerDict[key] == 2):
			pokerDict_2 = pokerDict.copy()
			pokerDict_2[key] -= 2
			tempGrade_2 = grade + 3*pokerValue[key]
			gradeList.append(gradehand(pokerDict_2, pokerValue, tempGrade_2, gradeList))


	return dumbGrade(pokerDict, pokerValue)+grade


def calculateResult(fileName, type, pokerValue):
	print("----------" + type + "----------")
	farmer = []
	host = []
	for line in open(os.path.join(sys.path[0], fileName), "r"):
		hand = eval(line)
		pokerDict = preProcessHand(hand, pokerValue)
		tempGradeList = []
		gradehand(pokerDict, pokerValue, 0, tempGradeList)
		if (len(hand) == 17):
			farmer.append(max(tempGradeList))
		else:
			host.append(max(tempGradeList))
	
	farmer.sort()
	host.sort()

	if (len(farmer) != 0):
		for i in range(len(farmer)):
			print("Hand " + str(i+1) + " has score " + str(farmer[i]))
		farmerMean = np.mean(farmer)
		farmerStd = np.std(farmer, ddof = 1)
		print("Mean: " + str(farmerMean))
		print("Std: " + str(farmerStd))

	if (len(host) != 0):
		for i in range(len(host)):
			print("Hand " + str(i+1) + " has score " + str(host[i]))
		hostMean = np.mean(host)
		hostStd = np.std(farmer, ddof = 1)
		print("Mean: " + str(hostMean))
		print("Std: " + str(hostStd))
	
	


def main():
	pokerValue = dict([("2",14),("3",3),("4",4),("5",5),("6",6),("7",7),("8",8),("9",9),("10",10),("j",11),("q",12),("k",13),("a",14),("ltg",18),("wcy",23)])
	calculateResult("card.txt", "not paid", pokerValue)
	#calculateResult("", "")

	


main()