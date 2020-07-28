
def preProcessHand(hand, pokerValue):
	pokerDict = dict([("3",0),("4",0),("5",0),("6",0),("7",0),("8",0),("9",0),("10",0),("j",0),("q",0),("k",0),("2",0),("ltg",0),("wcy",0)])
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


def main():
	pokerValue = dict([("2",14),("3",3),("4",4),("5",5),("6",6),("7",7),("8",8),("9",9),("10",10),("j",11),("q",12),("k",13),("ltg",18),("wcy",23)])
	hand1 = ['3','3','3','4','5','6','8','8','8','9','10','j','j','2','2','wcy','ltg']
	hand2 = ['3','3','3','4','5','6','7','8','9','9','10','j','j','2','2','2','2']
	hand3 = ['5','2','0','wcy']
	pokerDict_1 = preProcessHand(hand1, pokerValue)
	pokerDict_2 = preProcessHand(hand2, pokerValue)
	gradeList_1 = []
	gradeList_2 = []
	gradeList_3 = []
	gradehand(pokerDict_1, pokerValue, 0,gradeList_1)
	gradehand(pokerDict_2, pokerValue, 0,gradeList_2)
	print("hand1:",max(gradeList_1))
	print("hand2:",max(gradeList_2))
	print("hand3:",5201314)


main()