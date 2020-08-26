import numpy as np
import os, sys
import matplotlib.pyplot as plt
from functools import lru_cache
import json

pokerValue = {"2":14,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"j":11,"q":12,"k":13,"a":14,"ltg":19,"wcy":25}

def preProcessHand(hand):
	pokerDict = {"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"j":0,"q":0,"k":0,"a":0,"2":0,"ltg":0,"wcy":0}
	for i in range(len(hand)):
		pokerDict[hand[i]] += 1
	return pokerDict
	


def dumbGrade(pokerDict):
	grade = 0
	if (pokerDict["wcy"]!=0 and pokerDict["ltg"] !=0):
		grade += 2*16*8 #king
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
	keyList = list(pokerDict.keys())
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

def getStreakPari(pokerDict):
	streakEnd = 0 #exclusive
	streakLength = 0
	curEnd = 0 #exclusive
	curLength = 0
	keyList = list(pokerDict.keys())
	streak = []
	for i in range(len(keyList)):
		curKey = keyList[i]
		if ((pokerDict[curKey]) == 2):
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

def removeStreakPair(pokerDict, streak):
	j = 0
	keyList = list(pokerDict.keys())
	for i in range(len(streak)):
		while (j < len(keyList)):
			if (keyList[j] == streak[i]):
				pokerDict[keyList[j]] -= 2
				j += 1
				break
			j += 1
	return pokerDict

def removeStreak(pokerDict, streak):
	j = 0
	keyList = list(pokerDict.keys())
	for i in range(len(streak)):
		while (j < len(keyList)):
			if (keyList[j] == streak[i]):
				pokerDict[keyList[j]] -= 1
				j += 1
				break
			j += 1
	return pokerDict


@lru_cache(maxsize=None)
def gradehand(pokerDict, grade, gradeList):
	#print(gradeList)
	pokerDict = json.loads(pokerDict)
	gradeList = json.loads(gradeList)
	index = 0
	keyList= list(pokerDict.keys())
	for key in pokerDict:
		if (pokerDict[key] == 4):
			pokerDict_4 = pokerDict.copy()
			pokerDict_4[key] -= 4
			tempGrade_4 = grade + 4*pokerValue[key]*4
			gradeList.append(gradehand(json.dumps(pokerDict_4), tempGrade_4, json.dumps(gradeList)))
		if (index < len(pokerDict) and (index+1 <len(pokerDict))):
			if ((pokerDict[keyList[index]] ==3) and (pokerDict[keyList[index+1]] == 3)):
				tempGrade_shun3 = grade + pokerValue[keyList[index+1]]*6*2.5
				pokerDict_shun3 = pokerDict.copy()
				pokerDict_shun3[keyList[index]]-=3
				pokerDict_shun3[keyList[index+1]]-=3
				gradeList.append(gradehand(json.dumps(pokerDict_shun3), tempGrade_shun3, json.dumps(gradeList)))
		streakPair = getStreakPari(pokerDict)
		#
		if(streakPair != None):
			pokerDict_SP = pokerDict.copy()
			pokerDict_SP = removeStreakPair(pokerDict_SP, streakPair)
			streakLength = len(streakPair)
			tempGrade_SP = grade + streakLength * pokerValue[streakPair[streakLength//2]]*2
			gradeList.append(gradehand(json.dumps(pokerDict_SP), tempGrade_SP, json.dumps(gradeList)))
		streak = getStreak(pokerDict)
		#streak
		if (streak != None):
			pokerDict_S = pokerDict.copy()
			pokerDict_S = removeStreak(pokerDict_S, streak)
			streakLength = len(streak)
			tempGrade_S = grade + streakLength * pokerValue[streak[streakLength//2]]*2
			gradeList.append(gradehand(json.dumps(pokerDict_S), tempGrade_S, json.dumps(gradeList)))	
		#triple
		if (pokerDict[key] == 3):
			pokerDict_3 = pokerDict.copy()
			pokerDict_3[key] -= 3
			tempGrade_3 = grade + 3*pokerValue[key]*2
			gradeList.append(gradehand(json.dumps(pokerDict_3), tempGrade_3, str(gradeList)))
		#air plane
		if (index < len(pokerDict) and (index+1 <len(pokerDict)) and (index+2<len(pokerDict))):
			if((pokerDict[keyList[index]] ==2) and (pokerDict[keyList[index+1]] == 2) and (pokerDict[keyList[index+2]]==2)):
				tempGrade_shun2 = grade + pokerValue[keyList[index+2]]*6*1.5
				pokerDict_shun2 = pokerDict.copy()
				pokerDict_shun2[keyList[index]]-=2
				pokerDict_shun2[keyList[index+1]]-=2
				pokerDict_shun2[keyList[index+2]]-=2
				gradeList.append(gradehand(json.dumps(pokerDict_shun2), tempGrade_shun2, json.dumps(gradeList)))
		#pair
		if (pokerDict[key] == 2):
			pokerDict_2 = pokerDict.copy()
			pokerDict_2[key] -= 2
			tempGrade_2 = grade + 2*pokerValue[key]*1.2
			gradeList.append(gradehand(json.dumps(pokerDict_2), tempGrade_2, json.dumps(gradeList)))

		index += 1


	if(gradeList == [] or dumbGrade(pokerDict)+grade > max(gradeList)):
		gradeList.append(dumbGrade(pokerDict)+grade)
	return max(gradeList)

def detectBreaks(pokerDict):
	result = 0
	for key in pokerDict:
		if pokerDict[key] == 0:
			if (key != "ltg" or key != "wcy"):
				result += pokerValue[key]*2
	return result

def calculateResult(fileName, type, pokerValue):
	print("----------" + type + "----------")
	farmer = []
	i = 0
	for line in open(os.path.join(sys.path[0], fileName), "r"):
		hand = eval(line)
		pokerDict = preProcessHand(hand)
		grade_reduced = detectBreaks(pokerDict)
		tempGradeList = json.dumps([])
		grade = gradehand(json.dumps(pokerDict), 0, tempGradeList)
		
		farmer.append(grade-grade_reduced)
		if(grade-grade_reduced <=0):
			print(i)
		i += 1
	farmerMean = np.mean(farmer)
	farmer.sort()
	plt.figure()
	cord = []
	for i in range (len(farmer)):
		cord.append(i)

	plt.plot(cord,farmer)
	plt.title(type)
	plt.ylabel("score")
	plt.xlabel("hand index")
	plt.savefig(type+".jpg")

	if (len(farmer) != 0):
		
		farmerStd = np.std(farmer, ddof = 1)
		print("Total hands: " + str(len(farmer)))
		print("Max: " + str(max(farmer)))
		print("Min: " + str(min(farmer)))
		print("Mean: " + str(farmerMean))
		print("Std: " + str(farmerStd))
		
	return farmer

	
def proportionCalculate(hand, farmerMean, type):
	belowAvgCount = 0.0
	for i in range (len(hand)):
		if (hand[i]<=farmerMean):
			belowAvgCount += 1.0
	belowAvgPercent = (belowAvgCount/float(len(hand)))
	aboveAvgPercent = 1 - belowAvgPercent
	print(type + " below average proportion: " + str(belowAvgPercent))
	print(type + " above average proportion: " + str(aboveAvgPercent))


def main():
	paid = calculateResult("paidCard.txt", "paid", pokerValue)
	unpaid = calculateResult("unpaidCard.txt", "not paid", pokerValue)
	farmerMean = (np.mean(paid) + np.mean(unpaid))/2
	print(" ------ overall hand power distribution ------ ")
	proportionCalculate(paid, farmerMean, "paid")
	proportionCalculate(unpaid, farmerMean, "unpaid")
	


main()