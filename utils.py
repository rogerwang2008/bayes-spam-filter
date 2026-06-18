"""
工具函数。除非必须，不要修改
"""

import os

SmsCorpus = list[tuple[bool, str]]


def read_corpus(file_path: str | os.PathLike = "./dataset/corpus.csv") -> SmsCorpus:
    """
    获取语料库
    :param file_path: 语料库 csv 文件路径
    :return: 一个列表。其中每个元素是一个元组，第一个元素代表是否为垃圾短信，第二个元素代表短信实际内容
    """
    sms_list = []
    with open(file_path, encoding="utf-8") as f:
        next(f)  # 跳过第一行表头
        for line in f:
            is_spam, body = line.strip().split(",", 1)
            sms_list.append((is_spam == "1", body))
    return sms_list
