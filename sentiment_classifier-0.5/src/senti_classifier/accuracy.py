xmlfile = open('fulldata.txt')
testfile = open('results320')

xmldict = {}
testdict = {}

accuracy = 0.0
correct_count = 0.0
falseneg = 0.0
falsepos = 0.0
totalcount = 0.0

for line in xmlfile.read().strip().splitlines():
	arr = line.split('***')
	s_id = arr[0].strip()
	polarity = arr[1].strip()

	xmldict[s_id] = polarity

for line in testfile.read().strip().splitlines():
	arr = line.split(',')
	s_id = arr[0]
	polarity = arr[1].strip()
	if s_id in xmldict:
		if polarity == xmldict[s_id]:
			correct_count += 1
			totalcount += 1
		elif polarity == 'negative' and xmldict[s_id] == 'positive':
			falseneg += 1
			totalcount += 1
		elif polarity == 'positive' and xmldict[s_id] == 'negative':
			falsepos += 1
			totalcount += 1


accuracy = correct_count / totalcount
print accuracy, falseneg, falsepos, totalcount

