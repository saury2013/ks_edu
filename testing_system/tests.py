from django.test import TestCase

# Create your tests here.

import jieba
import jieba.posseg as pseg
from gensim import corpora, models, similarities


# filename='result.txt'
# fileneedCut='test.txt'
# fn=open(fileneedCut,"rb")
# f=open(filename,"w+")
# for line in fn.readlines():
#     words=pseg.cut(line)
#     for w in words:
#         print (str(w))
#         f.write(str(w))
# f.close()
# fn.close()

def gen2list(words):
    result = []
    for w in words:
        result.append(w)
    return result


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


test_str = "(1)研究性学习。研究性学习是指学生基于自身兴趣，在教师指导下，从自然、社会和学生自身生活中选择和确定研究专题，主动地获取知识、应用知识、解决问题的学习活动。\
　　(2)社区服务与社会实践。社区服务与社会实践是学生在教师指导下，走出教室，参与社区和社会实践活动，以获取直接经验、发展实践能力、增强社会责任感为主旨的学习领域。\
　　(3)信息技术教育。信息技术不仅是综合实践活动有效实施的重要手段，而且是综合实践活动探究的重要内容。信息技术教育的目的在于帮助学生发展适应信息时代需要的信息素。\
　　(4)劳动技术教育。劳动与技术教育是以学生获得积极劳动体验、形成良好技术素养为主的多方面发展为目标，且以操作性学习为特征的学习领域。"
# words=pseg.cut(test_str)
# corpus = gen2list(words)
# dictionary = corpora.Dictionary(corpus)
# print(corpus)
# print(dictionary)
# doc_vectors = [dictionary.doc2bow(text) for text in corpus]
# print (len(doc_vectors))
# print (doc_vectors)
# tfidf = models.TfidfModel(doc_vectors)
# tfidf_vectors = tfidf[doc_vectors]
# print (len(tfidf_vectors))
# print (len(tfidf_vectors[0]))
#
# query_str = "(1)研究性学习。研究性学习是指学生基于自身兴趣，在教师指导下，从自然、社会和学生自身生活中选择和确定研究专题，主动地获取知识、应用知识、解决问题的学习活动"
# query=gen2list(pseg.cut(query_str))
# query_bow = dictionary.doc2bow(query)
#
# index = similarities.MatrixSimilarity(tfidf_vectors)
# sims = index[query_bow]
# print(sims)

# wordstest_model = ["我去玉龙雪山并且喜欢玉龙雪山玉龙雪山","我在玉龙雪山并且喜欢玉龙雪山"]
# textTest = [word for word in jieba.cut(test_str)]
# dictionary = corpora.Dictionary(textTest,prune_at=2000000)
# corpus_model= [dictionary.doc2bow(test) for test in textTest]
# print(corpus_model)
# [[(0, 1), (2, 3), (3, 1), (4, 1)], [(0, 1), (1, 1), (2, 2), (3, 1)]]
# 目前只是生成了一个模型,并不是将对应的corpus转化后的结果,里面存储有各个单词的词频，文频等信息
# tfidf_model = models.TfidfModel(corpus_model)
#使用测试文本来测试模型，提取关键词,test_bow提供当前文本词频，tfidf_model提供idf计算
testword = "劳动与技术教育成良好技术素养为主的多方面发展为目标是以学生获得积极劳动体验、学习为特征的学习形，且以操作性领域。"
# print([word for word in jieba.cut(testword)])
# test_bow = dictionary.doc2bow([word for word in jieba.cut(testword)])
# print (tfidf_model[test_bow])
#
# test_list = [str for str in pseg.cut(test_str)]
# test2_list = [str for str in pseg.cut(testword)]
# text = tokenization(test_list)
# text2 = tokenization(test2_list)
# print(text)
#
# dictionary = corpora.Dictionary([text])
# print(dictionary)
# corpus = [dictionary.doc2bow(t) for t in [text]]
# query_vec = dictionary.doc2bow(text2)
# print(corpus)
# print("query_vec:",query_vec)
# tfidf = models.TfidfModel(corpus)
# print(tfidf[query_vec])
texts = tokenization(test_str)
dictionary = corpora.Dictionary(texts)
print(dictionary)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
corpus_lsi = lsi[corpus_tfidf]
index = similarities.MatrixSimilarity(lsi[corpus])
new_vec = dictionary.doc2bow(jieba.cut(testword, cut_all=False))
lsi_vec = lsi[new_vec]
sims = index[lsi_vec]
print(sims.tolist())
print(list(enumerate(sims)))
simsorted = sorted(enumerate(sims), key=lambda item: -item[1])
print(simsorted)

# import re
# from math import sqrt
# #You have to install the python lib
# import jieba
#
# def file_reader(filename,filename2):
#     file_words = {}
#     ignore_list = [u'的',u'了',u'和',u'呢',u'啊',u'哦',u'恩',u'嗯',u'吧'];
#     accepted_chars = re.compile("[\\u4E00-\\u9FA5]+")
#
#
#     all_the_text = test_str
#     seg_list = jieba.cut(all_the_text, cut_all=True)
#         #print "/ ".join(seg_list)
#     for s in seg_list:
#         if accepted_chars.match(s) and s not in ignore_list:
#             if s not in file_words.keys():
#                 file_words[s] = [1,0]
#             else:
#                 file_words[s][0] += 1
#
#
#
#     all_the_text = testword
#     seg_list = jieba.cut(all_the_text, cut_all=True)
#     for s in seg_list:
#         if accepted_chars.match(s) and s not in ignore_list:
#             if s not in file_words.keys():
#                 file_words[s] = [0,1]
#             else:
#                 file_words[s][1] += 1
#
#     sum_2 = 0
#     sum_file1 = 0
#     sum_file2 = 0
#     for word in file_words.values():
#         sum_2 += word[0]*word[1]
#         sum_file1 += word[0]**2
#         sum_file2 += word[1]**2
#
#     rate = sum_2/(sqrt(sum_file1*sum_file2))
#     print ('rate: ')
#     print (rate)
#
# file_reader('thefile.txt','thefile2.txt')