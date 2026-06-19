# 基于朴素贝叶斯的垃圾短信过滤器

本项目使用 **卡方检验（Chi-Square Test）** 提取关键词，并结合 **朴素贝叶斯（Naive Bayes）** 算法实现中文垃圾短信分类。

## 项目结构

```
rdfz-bayes-spam-filter-project/
├── dataset/
│   ├── corpus.csv          # 短信语料库（标注垃圾/正常短信）
│   └── test_data.txt       # 测试数据
├── utils.py                # 工具函数（读取语料库）
├── chi2_get_words.py       # 卡方检验提取关键词
├── bayes_evaluate.py       # 朴素贝叶斯短信分类
├── target_words.txt        # 生成的关键词列表（运行后生成）
└── target_words_freq.txt   # 关键词词频及卡方值（运行后生成）
```

## 依赖

- Python 3.10+
- [jieba](https://github.com/fxsjy/jieba) - 中文分词库

安装依赖：

```bash
pip install jieba
```

## 使用方法

### 第一步：提取关键词

在当前目录下运行卡方检验脚本，从语料库中提取垃圾短信关键词：

```bash
python chi2_get_words.py
```

该脚本会：
1. 读取 `dataset/corpus.csv` 语料库
2. 使用 jieba 进行中文分词
3. 计算每个词的卡方值（显著性水平 α = 0.001，阈值 10.828）
4. 输出关键词到 `target_words.txt` 和 `target_words_freq.txt`

### 第二步：短信分类

在当前目录下运行贝叶斯分类器，交互式输入短信内容进行垃圾短信检测：

```bash
python bayes_evaluate.py
```

程序会：
1. 读取语料库和关键词列表
2. 计算每个关键词在垃圾短信和正常短信中的概率
3. 提示输入短信内容
4. 输出该短信是垃圾短信的概率

## 算法说明

### 卡方检验（Chi-Square Test）

用于衡量词语与垃圾短信类别之间的独立性。卡方值越大，说明该词与垃圾短信的相关性越强。

计算公式：

```
χ² = (a+b+c+d) × (ad-bc)² / ((a+c)(b+d)(a+b)(c+d))
```

其中：
- a = 包含该词的垃圾短信数量
- b = 包含该词的正常短信数量
- c = 不包含该词的垃圾短信数量
- d = 不包含该词的正常短信数量

### 朴素贝叶斯分类（Naive Bayes）

基于贝叶斯定理，假设各特征（关键词）之间相互独立，计算短信属于垃圾短信的后验概率：

```
P(垃圾|短信) = P(短信|垃圾) × P(垃圾) / P(短信)
```

## 数据集格式

`dataset/corpus.csv` 格式：

```csv
is_spam,body
1,【工行优惠季领10元**支付券】...
0,市气象台31日6时发布...
```

- `is_spam`: 1 表示垃圾短信，0 表示正常短信
- `body`: 短信内容

## 注意事项

- `target_words.txt` 和 `target_words_freq.txt` 已加入 `.gitignore`，不会被提交到版本控制，仅在运行后生成。
- 卡方值阈值设为 10.828（对应 α = 0.001），可根据需要调整
- 分词时会自动过滤单字、标点符号及英文数字
