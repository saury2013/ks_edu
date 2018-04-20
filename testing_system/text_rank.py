# -*- coding: utf-8 -*-
__author__ = 'Allen'

import math
import jieba.analyse
article_a = '我喜欢中国，也喜欢美国。'
article_b = '我喜欢足球，不喜欢篮球。'
test_str = "(1)研究性学习。研究性学习是指学生基于自身兴趣，在教师指导下，从自然、社会和学生自身生活中选择和确定研究专题，主动地获取知识、应用知识、解决问题的学习活动。\
　　(2)社区服务与社会实践。社区服务与社会实践是学生在教师指导下，走出教室，参与社区和社会实践活动，以获取直接经验、发展实践能力、增强社会责任感为主旨的学习领域。\
　　(3)信息技术教育。信息技术不仅是综合实践活动有效实施的重要手段，而且是综合实践活动探究的重要内容。信息技术教育的目的在于帮助学生发展适应信息时代需要的信息素。\
　　(4)劳动技术教育。劳动与技术教育是以学生获得积极劳动体验、形成良好技术素养为主的多方面发展为目标，且以操作性学习为特征的学习领域。"
test_str2 = "(1)研究性学习。研究性学习是指学生基于自身你们不是这样的话兴趣，在教师指导下，从自然、社会和学生自身生活中选择和确定研究专题，主动地获取知识、应用知识、解决问题的学习活动。\
　　(2)社区服务与社会实践。社区服务与社会实践是学生在教师指导下，走出教室，参与社区和社会实践活动，以获取直接经验、发展实践能力、增强社会责任感为主旨的学习领域。\
　　(3)信息技术教育。信息技术不仅是综合实践活动有效实施的重要手段，而且是综合实践活动探究的重要内容。信息技术教育的目的在于帮助学生发展适应信息时代需要的信息素。4)劳动技术教育。劳动与技术教育是以学生获得积极劳动体验、形成良好技术素养为主的多方面发展为目标，且以操作性学习为特征的学习领域。"


def cut_word(article):
    # 这里使用了TF-IDF算法，所以分词结果会有些不同->https://github.com/fxsjy/jieba#3-关键词提取
    res = jieba.analyse.extract_tags(
        sentence=article, topK=20, withWeight=True)
    return res


def tf_idf(res1=None, res2=None):
    # 向量，可以使用list表示
    vector_1 = []
    vector_2 = []
    # 词频，可以使用dict表示
    tf_1 = {i[0]: i[1] for i in res1}
    tf_2 = {i[0]: i[1] for i in res2}
    res = set(list(tf_1.keys()) + list(tf_2.keys()))

    # 填充词频向量
    for word in res:
        if word in tf_1:
            vector_1.append(tf_1[word])
        else:
            vector_1.append(0)
            if word in tf_2:
                vector_2.append(tf_2[word])
            else:
                vector_2.append(0)

    return vector_1, vector_2


def numerator(vector1, vector2):
    #分子
    return sum(a * b for a, b in zip(vector1, vector2))


def denominator(vector):
    #分母
    return math.sqrt(sum(a * b for a,b in zip(vector, vector)))


def run(vector1, vector2):
    return numerator(vector1,vector2) / (denominator(vector1) * denominator(vector2))


# vectors =  tf_idf(res1=cut_word(article=test_str), res2=cut_word(article=test_str2))
# # 相似度
# similarity = run(vector1=vectors[0], vector2=vectors[1])
# # 使用arccos计算弧度
# rad = math.acos(similarity)
# print(similarity, rad)

import difflib

# aa = 'A,B,C'
# bb = 'A,B,C'
#
# seq = difflib.SequenceMatcher(aa,bb)
#
# ratio = seq.ratio()
# print(ratio)

query_str = 'A,B,C'
s1 = 'B,A'
s2 = 'C,B,A'
s3 = 'C'
print(difflib.SequenceMatcher(None, query_str, s1).quick_ratio())
print(difflib.SequenceMatcher(None, query_str, s2).quick_ratio())
print(difflib.SequenceMatcher(None, query_str, s3).quick_ratio())