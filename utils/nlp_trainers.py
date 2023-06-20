from gensim import corpora
from gensim import models
import gensim
import numpy as np
from .nlp_utils import *

class LDATrainer:
    def __init__(self, num_topics, docs, passes=1) -> None:
        self.num_topics = num_topics
        self.stopwords = en.Defaults.stop_words
        self.stopwords = self.stopwords.union({'from', 'subject', 're', 'edu', 'use', 'et', 'al'})
        self.docs = self.process_texts(docs)
        self.dictionary = corpora.Dictionary(self.docs)
        self.corpus = [self.dictionary.doc2bow(text) for text in self.docs]
        self.lda_model = models.LdaMulticore(corpus=self.corpus,
                                        id2word=self.dictionary,
                                        num_topics=self.num_topics, 
                                        random_state=0,
                                        chunksize=100,
                                        passes=passes)

    def _hellinger(self, lda_vec1, lda_vec2):
        dense1 = gensim.matutils.sparse2full(lda_vec1, self.lda_model.num_topics)
        dense2 = gensim.matutils.sparse2full(lda_vec2, self.lda_model.num_topics)
        return np.sqrt(0.5 * ((np.sqrt(dense1) - np.sqrt(dense2))**2).sum())

    def get_most_similar_documents(self, query, top_k=5):
        query_bow = self.dictionary.doc2bow(query)
        query_lda = self.lda_model[query_bow]
        # sort according to hellinger distance
        dists = np.array(
            [self._hellinger(query_lda, self.lda_model[self.corpus[i]]) 
                    for i in range(len(self.corpus))])
        idx = np.argsort(dists)[:top_k]
        return [(i, self.docs[i], dists[i]) for i in idx]
    
    def process_texts(self, texts):
        """
        Processes a list of texts 
        """
        texts = process_data(texts, remove_new_lines=True)
        texts = list(sent_to_words(texts))
        texts = [[word for word in text if word not in self.stopwords] for text in texts]
        return texts
    
    def process_query(self, query):
        return self.process_texts([query])[0]
    
    def process_and_rank(self, query):
        processed_query = self.process_query(query)
        print(processed_query)
        return self.get_most_similar_documents(processed_query)
    
    def make_smart_queries(self):
        topic_data =[]
        for j in range(self.lda_model.num_topics):
            topic_query = ""
            for i, _ in self.lda_model.get_topic_terms(j):
                topic_query += " " + self.dictionary[i]
            topic_query = topic_query.strip()
            topic_data.append(topic_query)
        return topic_data