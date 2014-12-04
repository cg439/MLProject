import parseXML as parse, getGrams 

trainSentences, trainMap = parse.parseXML("AnnotatedData\Laptops_Train.xml")
#testSentences, testMap = parse.parseXML("AnnotatedData\TestData.xml")

def genNgramsMap(trainSentences):
	biGramMap = {}
	triGramMap = {}
	for sentence, ID in trainSentences:
		biGrams = []
		triGrams = []
		bigram = getGrams.getGrams(sentence, 2)
		if bigram != []:
			for b in bigram:
				temp = ""
				for term, pos in b:
					temp += term + " "
				biGrams.append(temp.strip())
		biGramMap[ID] = biGrams
		trigram = getGrams.getGrams(sentence, 3)
		if trigram != []:
			for t in trigram:
				temp = ""
				for term, pos in t:
					temp += term+ " "
				triGrams.append(temp.strip())
		triGramMap[ID] = triGrams 
	return biGramMap, triGramMap

def match(real, train):
	real = real.strip("")
	if train.find(real)!= -1:
		return True
	return False 

def isIn(x, l2):
	if x in l2:
		return True
	else:
		for y in l2:
			if match(x, y):
				return True
		return False

def getAccuracy(realMap, trainMap):
	correct = 0
	incorrect = 0
	total = 0 

	overallCorrect = 0
	overallIncorrect = 0
	overallTotal = len(trainSentences)

	falseNegatives = 0
	falsePostiives = 0 

	for s, i in trainSentences:
		realTerms = realMap[i]
		print "actual terms: " + str(realTerms)
		trainTerms = trainMap[i]
		print "train terms: " + str(trainTerms) 

		trainCount = len(trainTerms)
		realCount = len(realTerms)

		if (trainCount - realCount) > 0:
			falsePostiives += trainCount - realCount
		elif (trainCount - realCount) < 0:
			falseNegatives += realCount - trainCount
		else:
			falsePostiives += 0

		total += len(realTerms)

		if (realTerms == [] or trainTerms == []) and not(realTerms == [] and trainTerms == []):
			temp = False 
		else:
			temp = True
			for real in realTerms:
				real = real.strip('""')
				boolean = isIn(real, trainTerms)
				temp = temp and boolean 
				if boolean:
					correct += 1
				else:
					incorrect +=1
		print "did we match all terms? : " + str(temp) 
		print "num word correct thus far: " + str(correct)
		print "total word count thus far: " + str(total)
		if temp:
			overallCorrect += 1
		else:
			overallIncorrect +=1 

	wordAccuracy = float(correct)/total
	overallAccuracy = float(overallCorrect)/overallTotal

	return wordAccuracy, overallAccuracy, falseNegatives, falsePostiives, total 	

bMap, tMap = genNgramsMap(trainSentences)
bWordAccuracy, bOverallAccuracy, bfalseNeg, bfalsePos, bTotal = getAccuracy(trainMap, bMap)
tWordAccuracy, tOverallAccuracy, tfalseNeg, tfalsePos, tTotal = getAccuracy(trainMap, tMap)

bigramResult = "chunking with grammar: <JJ><NN>: bigrams per term accuracy: " + str(bWordAccuracy) + " per sentence accuracy: " + str(bOverallAccuracy) + " false negatives: " + str(bfalseNeg) + " false positives: " + str(bfalsePos) + " total terms: " + str(bTotal) + "\n"
trigramResult =  "chunking with grammar: <DT><JJ><NN>: trigrams per term accuracy: " + str(tWordAccuracy) + " per sentence accuracy: " + str(tOverallAccuracy) + " false negatives: " + str(tfalseNeg) + " false positives: " + str(tfalsePos) +  " total terms: " + str(tTotal) + "\n" 

with open("results.txt", "a") as f:
	f.write(bigramResult)
	f.write(trigramResult)


