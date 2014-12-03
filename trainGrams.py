import parseXML as parse, getGrams 

trainSentences, trainMap = parse.parseXML("AnnotatedData\\test.xml")
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
	if real.find(train) != -1 or train.find(real)!= -1:
		return True
	return False 

def getAccuracy(realMap, trainMap):
	correct = 0
	incorrect = 0
	total = 0 

	overallCorrect = 0
	overallIncorrect = 0
	overallTotal = len(trainSentences)

	for s, i in trainSentences:
		realTerms = realMap[i]
		print realTerms
		trainTerms = trainMap[i]
		print trainTerms 
		if (realTerms == [] or trainTerms == []) and not(realTerms == [] and trainTerms == []):
			temp = False 
		else:
			temp = True
			for real in realTerms:
				total +=1
				for fake in trainTerms:
					boolean = match(real, fake)
					temp = temp and boolean 
					if boolean:
						correct += 1
					else:
						incorrect +=1
		print "did we match all terms? : " + str(temp) 
		print "num word correct thus far: " + str(correct)
		if temp:
			overallCorrect += 1
		else:
			overallIncorrect +=1 
	wordAccuracy = float(correct)/total
	overallAccuracy = float(overallCorrect)/overallTotal

	return wordAccuracy, overallAccuracy		

bMap, tMap = genNgramsMap(trainSentences)
bWordAccuracy, bOverallAccuracy = getAccuracy(trainMap, bMap)
tWordAccuracy, tOverallAccuracy = getAccuracy(trainMap, tMap)

print "bigrams per word accuracy: " + str(bWordAccuracy) + " per sentence accuracy: " + str(bOverallAccuracy) 
print "trigrams per word accuracy: " + str(tWordAccuracy) + " per sentence accuracy: " + str(tOverallAccuracy) 

#running with "NP: {<JJ>*<NN>*}" and "NP: {<DT>?<JJ>*<NN>*}"
# bigrams per word accuracy: 0.554572271386 per sentence accuracy: 0.558070866142
# trigrams per word accuracy: 0.320269700801 per sentence accuracy: 0.527559055118