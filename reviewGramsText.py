import getGrams as getGrams

bigrams = []
trigrams = []
with open('reviews.txt') as f:
	content = f.readlines()
	for line in content[:6]:
		bigrams.append(getGrams.getGrams(line, 2))
		trigrams.append(getGrams.getGrams(line, 3))
print bigrams 
print trigrams