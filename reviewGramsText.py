import getGrams as getGrams

bigrams = []
trigrams = []
with open('reviews.txt') as f:
	content = f.readlines()
	for line in content[:10]:
		bigram = getGrams.getGrams(line, 2)
		if bigram != []:
			bigrams.append(bigram)
		trigram = getGrams.getGrams(line, 3)
		if trigram != []:
			trigrams.append(trigram)
print bigrams 
print trigrams