import os

from utils import read_corpus, SmsCorpus


def read_target_words(file_path: str | os.PathLike = "./target_words.txt") -> list[str]:
    """
    读取关键词列表
    :param file_path: 关键词列表文件路径
    :return: 关键词列表
    """
    with open(file_path, encoding="utf-8") as f:
        return [line.strip() for line in f if f]


def calc_probability(word: str, corpus: SmsCorpus) -> tuple[float, float]:
    """
    计算一个关键词在垃圾短信和正常短信中出现的概率
    :param word: 关键词
    :param corpus: 语料库
    :return: 概率。第一个元代表在正常短信中的概率，第二个元代表在垃圾短信中的概率
    """
    total_spam_count = 0
    total_ham_count = 0
    word_spam_count = 0
    word_ham_count = 0
    for is_spam, body in corpus:
        if is_spam:
            total_spam_count += 1
            if word in body:
                word_spam_count += 1
        else:
            total_ham_count += 1
            if word in body:
                word_ham_count += 1
    return word_ham_count / total_ham_count, word_spam_count / total_spam_count  # 返回概率


def evaluate_sms(sms: str, corpus: SmsCorpus, word_freq_dict: dict[str, tuple[float, float]]):
    """
    通过朴素贝叶斯算法计算短信的垃圾短信概率
    :param sms: 短信内容
    :param corpus: 语料库
    :param word_freq_dict: 关键词的概率的字典
    :return: 短信的垃圾短信概率
    """
    # 计算先验概率
    ham_total_count = 0

    spam_total_count = 0
    for is_spam, _ in corpus:
        if is_spam:
            spam_total_count += 1
        else:
            ham_total_count += 1

    ham_prior_probability = ham_total_count / (spam_total_count + ham_total_count)
    spam_prior_probability = spam_total_count / (spam_total_count + ham_total_count)

    # 计算似然值
    ham_likelihood = 1
    spam_likelihood = 1

    for word in target_words:
        if word not in sms:  # 短信中没有关键词，则跳过。只考虑本条短信中出现的词语
            continue
        word_ham_probability, word_spam_probability = word_freq_dict[word]  # 获取关键词的概率
        ham_likelihood *= word_ham_probability
        spam_likelihood *= word_spam_probability
        print(f"关键词：{word}；在正常短信中的概率：{word_ham_probability:.4%}；在垃圾短信中的概率：{word_spam_probability:.4%}")

    # 计算后验概率
    ham_posterior_probability = ham_likelihood * ham_prior_probability
    spam_posterior_probability = spam_likelihood * spam_prior_probability
    # 返回是垃圾短信的概率
    return spam_posterior_probability / (ham_posterior_probability + spam_posterior_probability)


if __name__ == '__main__':
    corpus = read_corpus()  # 读取语料库
    # read_corpus() 函数返回的是一个 列表 (list)，列表的每个元素都是一个二元组，第一个元标识短信是否是垃圾短信，第二个元是短信内容
    # 例如:
    # sms_data = corpus[0]  # 获取第一条短信数据
    # print(sms_data[0])  # True
    # print(sms_data[1])  # 【工行优惠季领10元**支付券】工行优惠季来啦!本周五（****年2月24日0点***点）诚邀您登录工行手机银行参加特邀……
    target_words = read_target_words()  # 读取关键词列表
    word_freq_dict = {}  # 关键词的概率的字典
    for word in target_words:
        word_freq_dict[word] = calc_probability(word, corpus)  # 计算关键词的概率，并存入字典

    while True:
        sms = input("请输入短信内容：")
        probability = evaluate_sms(sms, corpus, word_freq_dict)  # 通过朴素贝叶斯算法计算短信的垃圾短信概率
        print(f"垃圾短信概率：{probability:.10%}")
