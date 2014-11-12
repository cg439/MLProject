import nltk, re, pprint, os 

rev = os.listdir("Reviews/")

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

def splitBySentence(filename):
	with open(filename) as f:
		content = f.readlines()
		for line in content:
			line.split()
# #need to refactor using re 
# for t in text1:
# 	if t == ',' or t == '.' or t == '!' or t == '?' or t == ':' or t == ')' or t == '(':
# 		text1.remove(t)

# sentence = nltk.pos_tag(text1)
# print sentence 
# grammar = "NP: {<DT>?<JJ>*<NN>}"

# ##i don't know why regex parser doesn't work 
# cp = nltk.RegexpParser(grammar)
# result = cp.parse(sentence)
# print(result)
# result.draw()


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
