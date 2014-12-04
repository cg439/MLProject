xmlfile = open('testdatawithsenti.txt')
testfile = open('results')

xmldict = {}
testdict = {}

TOTAL = 1492
accuracy = 0.0
correct_count = 0.0

for line in xmlfile.read().strip().splitlines():
	arr = line.split(',')
	s_id = arr[0]
	polarity = arr[1].strip()

	xmldict[s_id] = polarity

for line in testfile.read().strip().splitlines():
	arr = line.split(',')
	s_id = arr[0]
	polarity = arr[1].strip()
	if s_id in xmldict:
		if polarity == xmldict[s_id]:
			correct_count += 1

accuracy = correct_count / TOTAL
print accuracy

