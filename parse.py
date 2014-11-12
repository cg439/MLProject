import nltk, re, os 

#rev = os.listdir("Reviews/")

##takes in all the reviews in the directory Reviews and adds them to a reviews.txt
#if reviews.txt already has stuff in it and you want to add more, delete the content first,
#or else it will be duplicated
def concatReviews(filename):
	with open(filename) as f:
		content = f.readlines()
	revs = open("reviews.txt", "a")
	for line in content:
		revs.write(line)
	f.close()

#the below code is ran only once to create a file containing all reviews 
# for r in rev:
# 	r = "Reviews/" + r 
#  	concatReviews(r)

#splits a given file into sentences, appending to a sentence array
#it also stores the (word, sentence) into a hashtable 
def splitBySentence(filename):
	sentences = []
	sentenceMap = {}
	with open(filename) as f:
		content = f.readlines()
		for line in content:
			split = re.split(r'[?!.]', line)
			for word in split:
				sentenceMap[word] = line
			sentences.append(split)
	return sentences, sentenceMap 

#given a sentence array will tokenize them and then tag each word with POS 
def posTag(sentences):
	tokens = []
	tagged = []
	for sent in sentences:
		tokens.append(nltk.word_tokenize(sent))
	tagged = nltk.pos_tag(tokens)
	return tokens, tagged

#example of how to use FreqDist. feed it an array of tokens.
#this returns 2 because 'abc' exists twice in the given array  
#print nltk.FreqDist(['what', 'omg', 'abc', 'abc'])['abc']
#the below line finds the freq 
#print nltk.FreqDist(['what', 'omg', 'abc', 'abc']).freq('abc')
#finds the most common n samples, n being 2 in this case, returning (sample, count)
#print nltk.FreqDist(['what', 'omg', 'abc', 'abc']).most_common(2)
#plots the frequency graph. require matplotlib 
#nltk.FreqDist(['what','omg','abc','abc']).plot()

#tree creation, groups at given grammar 
# grammar = "NP: {<DT>?<JJ>*<NN>}"

# cp = nltk.RegexpParser(grammar)
# result = cp.parse(sentence)
# print(result)
# result.draw()

#tree traversal
# def traverse(t):
#     try:
#         t.label()
#     except AttributeError:
#         print(t, end=" ")
#     else:
#         # Now we know that t.node is defined
#         print('(', t.label(), end=" ")
#         for child in t:
#             traverse(child)
#         print(')', end=" ")
