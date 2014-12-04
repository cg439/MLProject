import re

inf = open('reviews.txt')
outf = open('reviews_sentences.txt', 'w')

for line in inf.read().strip().splitlines():
	sentences = re.split(r'[?!.]', line)
	for j in sentences:
		if j.strip() != '':
			outf.write('%s\n' % j.strip())

outf.close()


