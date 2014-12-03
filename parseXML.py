def parseXML(filename):
	sentences = []
	termMap = {}

	with open(filename) as f:
		content = f.readlines()
		i = 0
		while i < len(content):
			if "sentence id=" in content[i]:
				parted = content[i].partition("sentence id=")
				partedEnd = parted[2].partition(">")
				sentId = partedEnd[0]
				i+=1
				next = content[i]
				sentParted = next.partition("<text>")
				sentEndParted = sentParted[2].partition("</text>")
				sentence = sentEndParted[0]
				sentences.append((sentence, sentId))
				i+=1
				if "<aspectTerms>" in content[i]:
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
						i+=1
					termMap[sentId] = terms
				else:
					termMap[sentId] = [] 
					i+=1 
			else:
				i+=1 
	return sentences, termMap 
