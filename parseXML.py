import operator

def parseXML(filename, senti=False):
	sentences = []
	termMap = {}
	senti_dict = {}

	with open(filename) as f:
		content = f.readlines()
		i = 0
		while i < len(content):
			if "sentence id=" in content[i]:
				parted = content[i].partition("sentence id=\"")
				partedEnd = parted[2].partition("\">")
				sentId = partedEnd[0]
				i+=1
				next = content[i]
				sentParted = next.partition("<text>")
				sentEndParted = sentParted[2].partition("</text>")
				sentence = sentEndParted[0]
				sentences.append((sentence, sentId))
				i+=1
				if "<aspectTerms>" in content[i]:
					count = {}
					i+=1
					nextTerm = content[i]
					terms = []
					while "</aspectTerms>" not in nextTerm:
						nextTerm = content[i]
						termParted = nextTerm.partition("term=")
						termEndParted = termParted[2].partition(" polarity")
						term = termEndParted[0]
						if term != "":
							terms.append(term)

						if senti:
							polarityParted = nextTerm.partition("polarity=\"")
							polarityEndParted = polarityParted[2].partition('\" from')
							polarity = polarityEndParted[0]
							if polarity != '':
								if polarity not in count:
									count[polarity] = 1
								else:
									count[polarity] += 1
						i+=1
					termMap[sentId] = terms
					if senti:
						senti_dict[sentId] = max(count.iteritems(), key = operator.itemgetter(1))[0] 
				else:
					termMap[sentId] = [] 
					i+=1 
			else:
				i+=1 
	if senti:
		return sentences, termMap, senti_dict
	else:
		return sentences, termMap

s, t, d = parseXML('AnnotatedData/Laptops_Train.xml', senti = True)
senti_f = open('testdatawithsenti.txt', 'w')
for k in d:
	senti_f.write(','.join(map(str, [k, d[k]])))
	senti_f.write('\n')
senti_f.close()


s_f = open('parsedSentences.txt', 'w')
for sentence in s:
	s_f.write('%s *** %s\n' % (sentence[1], sentence[0]))
s_f.close()


# print s

# print t



