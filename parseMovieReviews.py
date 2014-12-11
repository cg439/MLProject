from nltk.corpus import movie_reviews
from collections import defaultdict
import sys
from nltk import PorterStemmer

ps = PorterStemmer()
traindata = sys.argv[1]
testdata = sys.argv[2]
outtrain = sys.argv[3]
outtest = sys.argv[4]

def count_features(bag_of_words, features, polarity):
    for lst in features:
        for word in lst[0].keys():
            bag_of_words[polarity][ps.stem_word(word)] += 1
    return bag_of_words

def train_bag_of_words():
    """
    @return: dictionary
      bag_of_words['neg']['word'] ==> count
      bag_of_words['pos']['word'] ==> count
    """
    def word_feats(words): return dict([(ps.stem_word(word), True) for word in words])
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

def train_xml_data():

    f = open("train320.txt")
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

def combine_bag_of_words(xml, movie):
    for k in movie:
        for key, value in movie[k].iteritems():
            if key not in xml[k]:
                xml[k][ps.stem_word(key)] = int(value)
            else:
                xml[k][ps.stem_word(key)] += int(value)
    return xml

laptop_reviews = train_xml_data()
movie_data = train_bag_of_words()

bag_of_words = combine_bag_of_words(laptop_reviews, movie_data)

print bag_of_words