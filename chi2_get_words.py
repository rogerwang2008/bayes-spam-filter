"""
利用卡方检验法获取垃圾短信关键词
"""

import collections
import jieba

from utils import read_corpus  # 从csv文件获取语料库（短信数据集）


def chinese_tokenize(text) -> set:
    """
    中文分词
    :param text: 文本
    :return: 分词后的文本。（返回的是集合，可以认为是一个不重且无序的列表）
    """
    return set(w for w in jieba.cut(text) if w and not w.isascii())  # 去除字母和数字，只保留中文词汇


if __name__ == '__main__':
    # 1. 得到垃圾短信词汇表及词频、正常短信词汇表及词频
    # “词频”代表一个词出现在了几条短信中
    sms_corpus = read_corpus()  # 从csv文件获取语料库（短信数据集）
    sms_count = len(sms_corpus)  # 短信总条数
    spam_count = 0  # 垃圾短信条数
    ham_count = 0  # 正常短信条数
    vocabulary = set()  # 总词汇表
    spam_word_list = []  # 垃圾短信词汇表初始化为空
    ham_word_list = []  # 正常短信词汇表初始化为空
    for is_spam, body in sms_corpus:
        tokenized_body = chinese_tokenize(body)  # 中文分词
        vocabulary |= tokenized_body  # 取并集，得到总词汇表
        if is_spam:  # is_spam为1，表示是垃圾短信
            spam_word_list.extend(tokenized_body)  # 垃圾短信词汇表扩展
            spam_count += 1  # 垃圾短信条数加1
        else:  # is_spam为0，表示是正常短信
            ham_word_list.extend(tokenized_body)  # 正常短信词汇表扩展
            ham_count += 1  # 正常短信条数加1

    spam_counter = collections.Counter(spam_word_list)  # 统计垃圾短信词频
    ham_counter = collections.Counter(ham_word_list)  # 统计正常短信词频

    # 2. 利用独立性检验判断哪些词适合作为关键词，进行记录
    # 显著性水平 α 取 0.001，P(卡方 >= 10.828) = 0.001
    chi2_scores: dict[str, float] = {}  # 每一个词的卡方值表（字典）
    for word in vocabulary:  # 计算每一个 word 的卡方值并存到 chi2_scores 里
        # word 是总词汇表中的一个词
        if len(word) < 2:  # 如果当前词长度小于2，即是单字或者标点符号，则跳过
            continue

        a = spam_counter.get(word, 0)  # 出现 word 的垃圾短信的频数
        b = ham_counter.get(word, 0)  # 出现 word 的正常短信的频数
        c = spam_count - spam_counter.get(word, 0)  # 不出现 word 的垃圾短信的频数
        d = ham_count - ham_counter.get(word, 0)  # 不出现 word 的正常短信的频数
        
        chi2 = (a + b + c + d) * ((a * d - b * c) ** 2) / ((a + c) * (b + d) * (a + b) * (c + d))  # 计算卡方值
        chi2_scores[word] = chi2  # 存入卡方值表

    top_words = sorted(chi2_scores.items(), key=lambda x: x[1], reverse=True)
    for i, (word, score) in enumerate(top_words):
        if score < 10.828:
            # 卡方值阈值，小于这个值的词删除，不作为关键词
            top_words = top_words[:i]
            break

    # 3. 存储关键词到文件
    with open("target_words.txt", "w", encoding="utf-8") as f:
        f.writelines([word + "\n" for word, _ in top_words])

    # 4. 输出结果：关键词及其词频、卡方值
    print(f"关键词  \t正常短信词频\t垃圾短信词频\t卡方值")
    with open("target_words_freq.txt", "w", encoding="utf-8") as f:
        for word, score in top_words:
            ham_freq = ham_counter.get(word, 0)
            spam_freq = spam_counter.get(word, 0)
            print(f"{word:<4}\t{ham_freq:<4}\t{spam_freq:<4}\t{score:.2f}")
            f.write(f"{word}\t{ham_freq}\t{spam_freq}\t{score:.2f}\n")
