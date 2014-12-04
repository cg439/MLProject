import getGrams as getGrams

bigrams = []
trigrams = []
with open('reviews.txt') as f:
	content = f.readlines()
	for line in content:
		bigram = getGrams.getGrams(line, 2)
		if bigram != []:
			bigrams.append(bigram)
		trigram = getGrams.getGrams(line, 3)
		if trigram != []:
			trigrams.append(trigram)

with open('bigrams.txt', 'a') as f:
	for b in bigrams:
		for x in b:
			f.write("%s\n" % str(x))

with open('trigrams.txt', 'a') as f:
	for t in trigrams:
		for x in t:
			f.write("%s\n" % str(x))
# print bigrams 
# print trigrams