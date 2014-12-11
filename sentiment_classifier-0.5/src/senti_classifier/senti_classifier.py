#!/usr/bin/env python
import os, re, sys, codecs, nltk, argparse, operator, string, math
from nltk.corpus import wordnet as wn
from collections import defaultdict
import cPickle as pickle
from pkg_resources import resource_string, resource_stream
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import sentiwordnet
from nltk import PorterStemmer

"""
Sentiment Classifier & WSD Module

--Pulkit Kathuria
"""
__documentation__ = "http://www.jaist.ac.jp/~s1010205/sentiment_classifier"
__url__ = "http://www.jaist.ac.jp/~s1010205/"
__online_demo__ = "http://www.jaist.ac.jp/~s1010205/sentiment_classifier"
ps = PorterStemmer()
inputfile = outputfile = ''

class SentiWordNetCorpusReader:
    def __init__(self, filename):
        """
        Argument:
        filename -- the name of the text file containing the
                    SentiWordNet database
        """        
        self.filename = filename
        self.db = {}
        self.parse_src_file()

    def parse_src_file(self):
        lines = codecs.open(self.filename, "r", "utf8").read().splitlines()
        lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
        for i, line in enumerate(lines):
            fields = re.split(r"\t+", line)
            fields = map(unicode.strip, fields)
            try:            
                pos, offset, pos_score, neg_score, synset_terms, gloss = fields
            except:
                sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))
            if pos and offset:
                offset = int(offset)
                self.db[(pos, offset)] = (float(pos_score), float(neg_score))

    def senti_synset(self, *vals):        
        if tuple(vals) in self.db:
            pos_score, neg_score = self.db[tuple(vals)]
            pos, offset = vals
            synset = wn._synset_from_pos_and_offset(pos, offset)
            return SentiSynset(pos_score, neg_score, synset)
        else:
            synset = wn.synset(vals[0])
            pos = synset.pos
            offset = synset.offset
            if (pos, offset) in self.db:
                pos_score, neg_score = self.db[(pos, offset)]
                return SentiSynset(pos_score, neg_score, synset)
            else:
                return None

    def senti_synsets(self, string, pos=None):
        sentis = []
        synset_list = wn.synsets(string, pos)
        for synset in synset_list:
            sentis.append(self.senti_synset(synset.name()))
        sentis = filter(lambda x : x, sentis)
        return sentis

    def all_senti_synsets(self):
        for key, fields in self.db.iteritems():
            pos, offset = key
            pos_score, neg_score = fields
            synset = wn._synset_from_pos_and_offset(pos, offset)
            yield SentiSynset(pos_score, neg_score, synset)

class SentiSynset:
    def __init__(self, pos_score, neg_score, synset):
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = 1.0 - (self.pos_score + self.neg_score)
        self.synset = synset

    def __str__(self):
        """Prints just the Pos/Neg scores for now."""
        s = ""
        s += self.synset.name + "\t"
        s += "PosScore: %s\t" % self.pos_score
        s += "NegScore: %s" % self.neg_score
        return s

    def __repr__(self):
        return "Senti" + repr(self.synset)


    
def train_xml_data():

    f = open(inputfile)
    bag_of_words = {}
    bag_of_words['neg'] = defaultdict(int)
    bag_of_words['pos'] = defaultdict(int)

    negfeats = {}
    posfeats = {}

    for line in f.read().strip().splitlines():
        line = unicode(line.strip(), 'utf-8')
        if line:
            arr = line.split('***')
            sentence = arr[2].strip()
            regex = re.compile('[%s]' % re.escape(string.punctuation))
            sentence = regex.sub(' ', sentence)
            polarity = arr[1].strip()[:3]

            if polarity in ('pos', 'neg'):
                words = sentence.split()
                for word in words:
                    if word not in bag_of_words[polarity]:
                        bag_of_words[polarity][ps.stem_word(word)] = 1
                    else:
                        bag_of_words[polarity][ps.stem_word(word)] += 1

    return bag_of_words

def count_features(bag_of_words, features, polarity):
    for lst in features:
        for word in lst[0].keys():
            bag_of_words[polarity][ps.stem_word(word.lower())] += 1
    return bag_of_words

def train_bag_of_words():
    """
    @return: dictionary
      bag_of_words['neg']['word'] ==> count
      bag_of_words['pos']['word'] ==> count
    """
    def word_feats(words): return dict([(ps.stem_word(word.lower()), True) for word in words])
    bag_of_words = {}
    bag_of_words['neg'] = defaultdict(int)
    bag_of_words['pos'] = defaultdict(int)
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
    bag_of_words = count_features(bag_of_words, negfeats, 'neg')
    bag_of_words = count_features(bag_of_words, posfeats, 'pos')
    return bag_of_words

def classify_polarity(bag_of_words):
    """
    Pops word from bag_of_words['neg'/'pos'] if the word appears
    more in 'pos/'neg' respectively
    """
    for word, count in bag_of_words['neg'].items():
        if count > bag_of_words['pos'][word]: bag_of_words['pos'].pop(word)
        else: bag_of_words['neg'].pop(word)
    return bag_of_words
                    

def combine_bag_of_words(xml, movie):
    for k in movie:
        for key, value in movie[k].iteritems():
            if key not in xml[k]:
                xml[k][ps.stem_word(key)] = int(value)
            else:
                xml[k][ps.stem_word(key)] += int(value)
    return xml

"""
Word Disambiguator using nltk
Sentiment Classifier as a combination of
  -Bag of Words (nltk movie review corpus, words as features)
  -Heuristics
  
--KATHURIA Pulkit
"""
def word_similarity(word1, word2):
   w1synsets = wn.synsets(word1)
   w2synsets = wn.synsets(word2)
   maxsim = 0
   for w1s in w1synsets:
       for w2s in w2synsets:
           current = wn.path_similarity(w1s, w2s)
           if (current > maxsim and current > 0):
               maxsim = current
   return maxsim

def SentiWordNet_to_pickle(swn):
    synsets_scores = defaultdict(list)
    for senti_synset in swn.all_senti_synsets():
        if not synsets_scores.has_key(senti_synset.synset.name):
            synsets_scores[senti_synset.synset.name] = defaultdict(float)
        synsets_scores[senti_synset.synset.name]['pos'] += senti_synset.pos_score
        synsets_scores[senti_synset.synset.name]['neg'] += senti_synset.neg_score
    return synsets_scores

def disambiguateWordSenses(sentence, word):
    wordsynsets = wn.synsets(word)
    bestScore = 0.0
    result = None
    for synset in wordsynsets:
       for w in nltk.word_tokenize(sentence):
           score = 0.0
           for wsynset in wn.synsets(w):
               sim = wn.path_similarity(wsynset, synset)
               if(sim == None):
                   continue
               else:
                   score += sim
           if (score > bestScore):
              bestScore = score
              result = synset
    return result

def classify(line, synsets_scores, bag_of_words):

    #synsets_scores = pickled object in data/SentiWN.p
    pos = neg = 0
    #print line
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    line = regex.sub(' ', line)
    #print line

    if not line.strip() or line.startswith('#'):return pos, neg
    word_arr = line.split()
    #print word_arr
    for word in word_arr:
        #print word
        word = ps.stem_word(word)
        # if len(word_arr) > 6:
        if disambiguateWordSenses(line, word): 
            #print 'after if'
            disamb_syn = disambiguateWordSenses(line, word).name()
            if synsets_scores.has_key(disamb_syn):
                #print "after has key"
                #uncomment the disamb_syn.split... if also want to check synsets polarity
                if bag_of_words['neg'].has_key(word.lower()):
                    neg += math.log(bag_of_words['neg'][word]+1) * synsets_scores[disamb_syn]['neg']
                if bag_of_words['pos'].has_key(word.lower()):
                    pos += math.log(bag_of_words['pos'][word]+1) * synsets_scores[disamb_syn]['pos']
    return pos, neg

args = sys.argv
outputfile = args[1]
inputfile = args[2]
testf = args[3]

senti_pickle = resource_stream('senti_classifier', 'data/SentiWn.p')
synsets_scores = pickle.load(senti_pickle)
bag_of_words_xml = train_xml_data()
bag_of_words_movie = train_bag_of_words()

bag_of_words = combine_bag_of_words(bag_of_words_xml, bag_of_words_movie)


def polarity_scores(lines_list):

    scorer = defaultdict(list)
    pos, neg = classify(lines_list, synsets_scores, bag_of_words)
    return pos, neg

if __name__ == "__main__":

    results = []
    f = open(outputfile, 'w')

    testfile = open(testf)

    for lineno, line in enumerate(testfile.readlines()):
        line = unicode(line.strip(), 'utf-8')
        arr = line.split('***')
        line = arr[2].strip()
        s_id = int(arr[0].strip())
        #print line
        if len(line) == 0: continue
        pos, neg = polarity_scores(line)
        #print '{0:<40}... pos = {1:<5} \tneg = {2:<5}'.format(pos,neg)
        print line, pos, neg
        if pos >= neg:
            results += ['positive']
            f.write('%d, %s' % (s_id, 'positive'))
        elif pos < neg:
            results += ['negative']
            f.write('%d, %s' % (s_id, 'negative'))
        f.write('\n')
        

