from random import shuffle
from random import randint
from copy import deepcopy
from collections import Counter
import math

test_counts  = 'data/test.counts'
test_tfidf = 'data/test.tfidf'
train_counts = 'data/train.counts'
train_tfidf = 'data/train.tfidf'
vocab = 'data/vocabulary'
label_count = Counter()
fv_count = {}
vocab_dict = {}
c11 = 0
c00 = 0
c01 = 10
c10 = 15
totalWords = 0.0


def load_train_counts(file):
	return list([read_line(i) for i in open(file).read().strip().splitlines()])


def load_train_tfidf(file):
	return list([read_line(i) for i in open(file).read().strip().splitlines()])


def load_test_counts(file):
	return list([read_line(i) for i in open(file).read().strip().splitlines()])


def load_vocab(file):
	array_voacb = list([i for i in open(file).read().strip().splitlines()])

	for i in range(1, len(array_voacb)):
		vocab_dict[i] = array_voacb[i-1]

	return vocab_dict


def read_line(line):
	line = line.split()
	temp = line[1:len(line)]
	array = [int(line[0])]
	for i in temp:
		j = i.split(':')
		array.append([int(j[0]), int(j[1])])
	return array


vocab_dict_len = len(load_vocab(vocab))
train_counts_len = len(load_train_counts(train_counts))

def shuffle_train():
	train_tfidf_list = deepcopy(list([i for i in open(train_tfidf).read().strip().splitlines()]))
	train_counts_list = deepcopy(list([i for i in open(train_counts).read().strip().splitlines()]))
	f1 = open('shuffled_1.txt', 'w')
	f2 = open('shuffled_2.txt', 'w')
	f3 = open('shuffled_3.txt', 'w')
	f4 = open('shuffled_4.txt', 'w')
	shuffle(train_counts_list)
	for i in range(0, 4):
		#print len(train_tfidf_list)/4
		for j in range(0, len(train_counts_list)/4):
			if(i==0):
				f1.write("%s\n"%str(train_counts_list[j]))
			elif(i==1):
				f2.write("%s\n"%str(train_counts_list[j+50*i]))
			elif(i==2):
				f3.write("%s\n"%str(train_counts_list[j+50*i]))
			elif(i==3):
				f4.write("%s\n"%str(train_counts_list[j+50*i]))


def TrainNaiveBayes(data):
	
	#data = load_train_counts(train_counts)
	for item in data:
		label = item[0]
		
		for fv in item[1:len(item)]:
			if not fv[0] in fv_count:
				fv_count[fv[0]] = {'1':0.0, '-1':0.0, 'total': 0.0}
			fv_count[fv[0]][str(label)] += fv[1]
			fv_count[fv[0]]['total'] += fv[1]
			totalWords += fv[1]


	# for fv in fv_count:
	# 	fv_count[fv]['prob1'] = math.log((fv_count[fv]['1'] + 1) / (label_count[1]+length))
	# 	fv_count[fv]['prob-1'] = math.log((fv_count[fv]['-1'] + 1) / (label_count[-1]+length))


def Classify(data):
	labelProb = {}

	for fv in fv_count:
		if label != 0:
			#logProb = math.log(float(fv_count[fv])/totalWords)
			
			for label in label_count:
				logProb = math.log((fv_count[fv][str(label)] + 1)/(fv_count[fv]['total'] + 2))
				
				#logProb += fv[1] * fv_count[fv[0]]['prob'+str(label)]

			labelProb[label] = logProb

	if (labelProb[1]>=labelProb[-1]):
		return 1
	else:
		return -1
		#print labelProb



# results is an array of results
# data is test data
def TestClassifier(data, length):
	accurate_count = 0.0
	falseNegs = 0
	falsePos = 0
	# print len(results), len(data)
	for real in data:
		label = real[0]
		train = Classify(real, length)
		if (label == train):
			accurate_count += 1
		else:
			if train == -1:
				falseNegs += 1
			else:
				falsePos += 1

	print falsePos, falseNegs
	return accurate_count/len(data)



if __name__ == '__main__':

	train_data = load_train_counts(train_counts)
	data = load_test_counts(test_counts)
	load_vocab(vocab)
	length = len(vocab_dict)
	#print train_counts_len
	TrainNaiveBayes(train_data)

	print TestClassifier(data, length)
	print LogOdds()
