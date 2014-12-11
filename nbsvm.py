import random

sentences = {}
features = []

with open('testdatawithsenti.txt') as f:
	for line in f:
		sid, sep, classi = line.partition(",")
		if (classi.strip() == "positive"):
			s = 1
		if (classi.strip() == "negative"):
			s = -1
		if (classi.strip() == "neutral"):
			# for now, neutral elements will be negative
			continue
		sentences.update({int(sid):[s]})

with open('pasedSentences.txt') as f:
	for line in f:
		sid, sep, sent = line.partition(" *** ")
		if int(sid) in sentences:
			sentences[int(sid)].append(sent.strip())

for sent in sentences:
	words = sentences[sent][1].split()
	for word in words:
		w = word.strip(".,()!?;:'")
		if not w in features:
			features.append(w)

sampsize = int(len(sentences) * .7)
trainset = random.sample(list(sentences), sampsize)

train = open('traindat', mode = "w")
test = open('testdat', mode = "w")
for sent in sentences:
	f = []
	words = sentences[sent][1].split()
	for i in range(len(features)):
		f.append(words.count(features[i]))
	s = str(sentences[sent][0]) + " "
	for i in range(len(features)):
		s += str(i+1) + ":" + str(f[i]) + " "
	if sent in trainset:
		train.write(s.strip() + '\n')
	else:
		test.write(s.strip() + '\n')