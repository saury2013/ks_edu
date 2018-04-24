# -*- coding: utf-8 -*-
__author__ = 'Allen'

import jieba.posseg as pseg
from gensim import corpora, models, similarities


def tokenization(str):
    stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']
    # stopwords = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')']
    corpora_documents = []
    for s in str.split():
        str_list = [x for x in pseg.cut(s.strip())]
        # print(str_list)
        result = []
        for word, flag in str_list:
            if flag not in stop_flag:
                result.append(word)
        corpora_documents.append(result)
    return corpora_documents

def similarity_analysis(text1,text2):
    texts = tokenization(text1)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
    corpus_lsi = lsi[corpus_tfidf]
    index = similarities.MatrixSimilarity(lsi[corpus])
    new_vec = [dictionary.doc2bow(text) for text in  tokenization(text2)]
    # print("new_vec:",new_vec)
    lsi_vec = lsi[new_vec]
    new_vec_tfidf = tfidf[lsi_vec]

    sims = index[new_vec_tfidf]
    # print(sims.tolist())
    sims_list = sims.tolist()
    max_val = 0
    for s_list in sims_list:
        max_val += max(s_list) if isinstance(s_list,list) else s_list
    avg = max_val/len(texts)
    # print("avg:",avg)
    return avg



