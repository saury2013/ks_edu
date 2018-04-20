# -*- coding: utf-8 -*-
__author__ = 'Allen'

import jieba
import jieba.posseg as pseg
from gensim import corpora, models, similarities


def tokenization(str):
    stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']
    stopwords = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')']
    corpora_documents = []
    for s in str.split():
        str_list = [x for x in pseg.cut(s.strip())]
        print(str_list)
        result = []
        for word, flag in str_list:
            if flag not in stop_flag and word not in stopwords:
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
    print("new_vec:",new_vec)
    lsi_vec = lsi[new_vec]
    new_vec_tfidf = tfidf[lsi_vec]

    sims = index[new_vec_tfidf]
    print(sims.tolist())
    sims_list = sims.tolist()
    max_val = 0
    for s_list in sims_list:
        max_val += max(s_list) if isinstance(s_list,list) else s_list
    avg = max_val/len(texts)
    print("avg:",avg)
    return avg



# test_str = "(1)研究性学习。研究性学习是指学生基于自身兴趣，在教师指导下，从自然、社会和学生自身生活中选择和确定研究专题，主动地获取知识、应用知识、解决问题的学习活动。\
# 　　(2)社区服务与社会实践。社区服务与社会实践是学生在教师指导下，走出教室，参与社区和社会实践活动，以获取直接经验、发展实践能力、增强社会责任感为主旨的学习领域。\
# 　　(3)信息技术教育。信息技术不仅是综合实践活动有效实施的重要手段，而且是综合实践活动探究的重要内容。信息技术教育的目的在于帮助学生发展适应信息时代需要的信息素。\
# 　　(4)劳动技术教育。劳动与技术教育是以学生获得积极劳动体验、形成良好技术素养为主的多方面发展为目标，且以操作性学习为特征的学习领域。"
# test_str2 = "(1)研究性学习。研究性学习是指学生基于自身兴趣，在教师指导下，从自然、社会和学生自身生活中选择和确定研究专题，主动地获取知识、应用知识、解决问题的学习活动。\
# 　　社区服务与社会实践是学生在教师指导下，走出教室，参与社区和社会实践活动，以获取直接经验、发展实践能力、增强社会责任感为主旨的学习领域。\
# 　　(3)信息技术教育。信息技术不仅是综合实践活动有效实施的重要手段，而且是综合实践活动探究的重要内容。信息技术教育的目的在于帮助学生发展适应信息时代需要的信息素。\
# 　　(4)劳动技术教育。劳动与技术教育是以学生获得积极劳动体验、形成良好技术素养为主的多方面发展为目标，且以操作性学习为特征的学习领域。"
#
# similarity_analysis(test_str,test_str2)