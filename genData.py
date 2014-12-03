import nltk, re, os 

#rev = os.listdir("Reviews/")
#descrip = os.listdir("ProductDescrips/")

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

def concatDescrips(filename):
	with open(filename) as f:
		content = f.readlines()
	revs = open("descriptions.txt", "a")
	for line in content:
		revs.write(line)
	f.close()

#the below code is ran only once to create a file containing all reviews 
# for r in rev:
# 	r = "Reviews/" + r 
#  	concatReviews(r)

# for p in descrip:
# 	p = "ProductDescrips/" + p
# 	concatDescrips(p)
	
