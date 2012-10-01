'''
Implement Rocchio algo on a corpus of relevant documents
by weighting based on td-idf to iteratively form a new query vector of weightings
for each unique term across all dictionaries (from invertedFiles) passed into Rocchio
'''
import constants
import math
import sys
import PorterStemmer

class RocchioOptimizeQuery:



    def __init__(self, firstQueryTerm):
        '''
        Constructor
        '''
        self.query = {}
        self.query[firstQueryTerm] = 1
     
        
    def Rocchio(self, invertedFile, documentsList, relevantDocs, nonrelevantDocs):
        '''
        output new query vector'
        
        'calculate IDF per inverted file'
        'calculate TF per inverted file'
        
        'generate weight vector for relevant terms'

        '''
        p = PorterStemmer.PorterStemmer()

        weights = {}
        for term in invertedFile.iterkeys():
            sterm = term
            if constants.STEM_IN_ROCCHIO:
                sterm = p.stem(term.lower(), 0,len(term)-1)            
            weights[sterm] = 0.0    #initialize weight vector for each key in inverted file
        print ''

        relevantDocsTFWeights = {}
        nonrelevantDocsTFWeights = {} 

        # Compute relevantDocsTFWeights and nonrelevantDocsTFWeights vectors
        for docId in relevantDocs:
            doc = documentsList[docId]
            for term in doc["tfVector"]:
                sterm = term
                if constants.STEM_IN_ROCCHIO:
                    sterm = p.stem(term.lower(), 0,len(term)-1)

                if sterm in relevantDocsTFWeights:
                    relevantDocsTFWeights[sterm] = relevantDocsTFWeights[sterm] + doc["tfVector"][term]
                else:
                    relevantDocsTFWeights[sterm] = doc["tfVector"][term]

        for docId in nonrelevantDocs:
            doc = documentsList[docId]
            for term in doc["tfVector"]:
                sterm = term
                if constants.STEM_IN_ROCCHIO:
                    sterm = p.stem(term.lower(), 0,len(term)-1)                

                if sterm in nonrelevantDocsTFWeights:
                    nonrelevantDocsTFWeights[sterm] = nonrelevantDocsTFWeights[sterm] + doc["tfVector"][term]
                else:
                    nonrelevantDocsTFWeights[sterm] = doc["tfVector"][term]


        for term in invertedFile.iterkeys():
            idf = math.log(float(len(documentsList)) / float(len(invertedFile[term].keys())), 10)

            sterm = term
            if constants.STEM_IN_ROCCHIO:
                sterm = p.stem(term.lower(), 0,len(term)-1)

            for docId in invertedFile[term].iterkeys():
                if documentsList[docId]['IsRelevant'] == 1:
                    weights[sterm] = weights[sterm] + constants.BETA * idf * (relevantDocsTFWeights[sterm] / len(relevantDocs))
                else:
                    weights[sterm] = weights[sterm] - constants.GAMMA * idf * (nonrelevantDocsTFWeights[sterm]/len(nonrelevantDocs))

            if term in self.query:
                self.query[term] = constants.ALPHA * self.query[term] + weights[sterm]   #build new query vector of weights
            elif weights[sterm] > 0:
                self.query[term] = weights[sterm]

        return self.query
    
            
        
        
    