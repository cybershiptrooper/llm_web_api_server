
from sklearn.feature_extraction.text import CountVectorizer
import re
import numpy as np
import gensim
import spacy

en = spacy.load('en_core_web_sm')
def c_tf_idf(documents, m, ngram_range=(1, 1)):
    count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(documents)
    t = count.transform(documents).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)

    return tf_idf, count

def process_data(data, remove_new_lines=False):
    # Remove Emails
    ans = [re.sub('\S*@\S*\s?', '', sent) for sent in data]

    # Remove new line characters
    if remove_new_lines:
        ans = [re.sub('\s+', ' ', sent) for sent in ans]

    # Remove distracting single quotes
    ans = [re.sub("\'", "", sent) for sent in ans]

    # remove weird characters
    ans = [re.sub("[^a-zA-Z0-9,\n]+", " ", sent) for sent in ans]
    return ans

def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def process_texts_page_content(texts, remove_new_lines=False):
    for i in range(len(texts)):
        print(process_data([texts[i].page_content], remove_new_lines=remove_new_lines)[0])
        texts[i].page_content = process_data([texts[i].page_content], remove_new_lines=remove_new_lines)[0]
    return texts