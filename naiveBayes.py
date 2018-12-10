import nltk
import random
##from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import os.path

print("Imports DONE")

class VoteClassifier (ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)
    
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
    

print("File reading DONE")

documents = []
all_words = []
chunkGram = r"""Chunk: {<J.?>*<RB.?>*}"""
allowed_word_types = ["J", "R"]
short_pos_words = []
short_neg_words = []

short_pos = open("short_reviews/positive.txt","r").read()
short_neg = open("short_reviews/negative.txt","r").read()

for p in short_pos.split('\n'):
    documents.append( (p, "pos") )
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    chunkParser = nltk.RegexpParser(chunkGram)
    chunked = chunkParser.parse(pos)
    for node in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        for a in node.leaves():
            if a[1][0] in allowed_word_types:                
                short_pos_words.append(a[0].lower())

for n in short_neg.split('\n'):
    documents.append( (n, "neg") )
    words = word_tokenize(n)
    neg = nltk.pos_tag(words)
    chunkParser = nltk.RegexpParser(chunkGram)
    chunked = chunkParser.parse(neg)
    for node in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        for a in node.leaves():
            if a[1][0] in allowed_word_types:
                short_neg_words.append(a[0].lower())

for w in short_pos_words:
    all_words.append(w.lower())

for w in short_neg_words:
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:5000]


print("File pre processing DONE")

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features
	
#print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))
print("Searching for models...")
if not(os.path.isfile('./NuSVC.sav')):
    print("Models not found!!!")

    


    featuresets = [(find_features(rev), category) for (rev, category) in documents]

    random.shuffle(featuresets)

    # positive data example:      
    training_set = featuresets[:10000]
    testing_set =  featuresets[10000:]
    print("Shuffle DONE")
    ##
    ### negative data example:      
    ##training_set = featuresets[100:]
    ##testing_set =  featuresets[:100]


    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Original Naive Bayes accuracy:", (nltk.classify.accuracy(classifier, testing_set))*100)
    classifier.show_most_informative_features(15)
    pickle.dump(classifier, open('NaiveBayesModel.sav', 'wb'))

    print("NB DONE")

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)
    pickle.dump(classifier, open('MNB.sav', 'wb'))
    print("MultinomialNB accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)*100))

    print("Multi DONE")

    BNB_classifier = SklearnClassifier(BernoulliNB())
    BNB_classifier.train(training_set)
    pickle.dump(classifier, open('BNB.sav', 'wb'))
    print("BernoulliNB accuracy percent:",(nltk.classify.accuracy(BNB_classifier, testing_set)*100))

    print("Bernouli DONE")

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(training_set)
    pickle.dump(classifier, open('LogReg.sav', 'wb'))
    print("LogisticRegression accuracy percent:",(nltk.classify.accuracy(LogisticRegression_classifier, testing_set)*100))

    SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    SGDClassifier_classifier.train(training_set)
    pickle.dump(classifier, open('SGDC.sav', 'wb'))
    print("SGDClassifier accuracy percent:",(nltk.classify.accuracy(SGDClassifier_classifier, testing_set)*100))

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)
    pickle.dump(classifier, open('LinearSVC.sav', 'wb'))
    print("LinearSVC accuracy percent:",(nltk.classify.accuracy(LinearSVC_classifier, testing_set)*100))

    NuSVC_classifier = SklearnClassifier(NuSVC())
    NuSVC_classifier.train(training_set)
    pickle.dump(classifier, open('NuSVC.sav', 'wb'))
    print("NuSVC accuracy percent:",(nltk.classify.accuracy(NuSVC_classifier, testing_set)*100))

    voted_classifier = VoteClassifier(classifier,
                                    MNB_classifier,
                                    BNB_classifier,
                                    LogisticRegression_classifier,
                                    SGDClassifier_classifier,
                                    LinearSVC_classifier,
                                    NuSVC_classifier)
    print("voted_classifier accuracy percent:",(nltk.classify.accuracy(voted_classifier, testing_set)*100))

    ##print("Classification:", voted_classifier.classify(testing_set[0][0]), "Confidence %:", voted_classifier.confidence(testing_set[0][0]))
    ##print("Classification:", voted_classifier.classify(testing_set[1][0]), "Confidence %:", voted_classifier.confidence(testing_set[1][0]))
    ##print("Classification:", voted_classifier.classify(testing_set[2][0]), "Confidence %:", voted_classifier.confidence(testing_set[2][0]))
    ##print("Classification:", voted_classifier.classify(testing_set[3][0]), "Confidence %:", voted_classifier.confidence(testing_set[3][0]))
    ##print("Classification:", voted_classifier.classify(testing_set[4][0]), "Confidence %:", voted_classifier.confidence(testing_set[4][0]))
else:
    print("Models Founded!!!")
    print("Loading...")
    classifier = pickle.load(open('NaiveBayesModel.sav', 'rb'))
    print("Bayes Loaded")
    MNB_classifier = pickle.load(open('MNB.sav', 'rb'))
    print("MNB Loaded")
    BNB_classifier = pickle.load(open('BNB.sav', 'rb'))
    print("BNB Loaded")
    LogisticRegression_classifier = pickle.load(open('LogReg.sav', 'rb'))
    print("LogReg Loaded")
    SGDClassifier_classifier = pickle.load(open('SGDC.sav', 'rb'))
    print("SGDC Loaded")
    LinearSVC_classifier = pickle.load(open('LinearSVC.sav', 'rb'))
    print("LinearSVC Loaded")
    NuSVC_classifier = pickle.load(open('NuSVC.sav', 'rb'))
    print("NuSVC Loaded")
    voted_classifier = VoteClassifier(classifier,
                                    MNB_classifier,
                                    BNB_classifier,
                                    LogisticRegression_classifier,
                                    SGDClassifier_classifier,
                                    LinearSVC_classifier,
                                    NuSVC_classifier)
    
def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)