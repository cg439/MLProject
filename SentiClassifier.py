from senti_classifier import senti_classifier
sentences = ['The movie was the worst movie', 'It was the worst acting by the actors']
print senti_classifier.polarity_scores(sentences)
