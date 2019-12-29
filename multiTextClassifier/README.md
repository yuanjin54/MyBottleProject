## multiTextClassifier

### 1、项目介绍
在自然语言处理中，有一个常见的问题就是对客户的评价进行分析。 这些用户评论中，包含了大量的有用信息，例如情感分析，或者相关事实描述。 例如:
“味道不错的面馆，性价比也相当之高，分量很足～女生吃小份，胃口小的，可能吃不完呢。环境在面馆来说算是好的，至少看上去堂子很亮，也比较干净，一般苍蝇馆子还是比不上这个卫生状况的。中午饭点的时候，人很多，人行道上也是要坐满的，隔壁的冒菜馆子，据说是一家，有时候也会开放出来坐吃面的人。“
首先情感是正向的，除此之外我们还能够进行知道这个的几个事实描述：1. 性价比比较高； 2. 装修比较好； 3. 分量足。

- 位置: location
    交通是否便利(traffic convenience)
    距离商圈远近(distance from business district)
    是否容易寻找(easy to find)
- 服务(service)
    排队等候时间(wait time)
    服务人员态度(waiter’s attitude)
    是否容易停车(parking convenience)
    点菜/上菜速度(serving speed)
- 价格(price)
    价格水平(price level)
    性价比(cost-effective)
    折扣力度(discount)
- 环境(environment)
    装修情况(decoration)
    嘈杂情况(noise)
    就餐空间(space)
    卫生情况(cleaness)
- 菜品(dish)
    分量(portion)
    口感(taste)
    外观(look)
    推荐程度(recommendation)
- 其他(others)
    本次消费感受(overall experience)
    再次消费的意愿(willing to consume again)
    
而为了方便训练数据的标标注，训练数据中，<** 正面情感, 中性情感, 负面情感, 情感倾向未提及 > ** 分别对应与 (1, 0, -1, -2).

例如说，“味道不错的面馆，性价比也相当之高，分量很足～女生吃小份，胃口小的，可能吃不完呢。环境在面馆来说算是好的，至少看上去堂子很亮，也比较干净，一般苍蝇馆子还是比不上这个卫生状况的。中午饭点的时候，人很多，人行道上也是要坐满的，隔壁的冒菜馆子，据说是一家，有时候也会开放出来坐吃面的人。“
[交通是否便利(traffic convenience) -2

距离商圈远近(distance from business district) -2

是否容易寻找(easy to find) -2

排队等候时间(wait time) -2

服务人员态度(waiter’s attitude) -2

是否容易停车(parking convenience) -2

点菜/上菜速度(serving speed) -2

价格水平(price level) -2

性价比(cost-effective) 1

折扣力度(discount) -2

装修情况(decoration) 1

嘈杂情况(noise) -2

就餐空间(space) -2

卫生情况(cleaness) 1

分量(portion) 1

口感(taste) 1

外观(look) -2

推荐程度(recommendation) -2

次消费感受(overall experience) 1

再次消费的意愿(willing to consume again) -2
]

本次项目用到的环境为：
Python3.6， Pycharm, Jupyter Notebook
Keras， Tensorflow, Pandas
Linux Ubuntu 服务器
  

### 2、主要技术
    

### 3、算法实现步骤


### 4、模型评估
处理方案
1.数据处理：
数据清洗：去重、去空，繁体变简体，去除标点符号及停用词，但保留表情符号
分词：分别以char和word级别分别测试
2.模型搭建(不同模型融合）：
TextCNN
biGRU、biLSTM
biGRU、biLSTM with Attention
RCNN
3.评价标准：
样本存在严重的不平衡问题，负面情绪与中性情绪很少，如果以acc作为评价标准，虽然看起来准确度很高，但是却预测不准小样本数据，因此以f1为评价指标更为合理
最终f1=0.6056,但并没跑完所有模型，RCNN整体稍好一些，由于时间原因，RCNN只跑了前几个类别
4.调参总结
模型：TextCNN及RCNN总体表现更好一些
分词：对于RCNN, char级别好于word级别，其他未测试
LSTM与GRU:LSTM略好于GRU
Hidden_size: 256>128
Class_weight: 设置过balanced方式，但发现效果不好，分析是因为某些样本数据过少，设置太大惩罚项之后会导致小样本的过拟合
但对于TextCNN，Class_weight为0: 1, 1: 3, 2: 3, 3: 0.5更佳，但对于RCNN,不设置class_weight更佳
Batch_size:32>128,可能是由于小的batchsize随机性更强，带来的噪声有助于逃离sharp minimum，模型泛化能力更好。
Loss:虽然y为one_hot形式，但loss设置为binary_crossentropy,收敛更快，这是因为binary_crossentropy同时更新0类标签


TextCnn+Attention
结合了CNN里面的卷积操作，对卷积结果不进行maxpoolling，而直接借鉴Attention机制，对卷积结果进行处理attention处理，然后对每一个attention结果进行softmax，相当于20分类共用了卷积操作，然后对卷积结果进行不同的attention从而实现20个类别分类。
优点：保证特征的提取同时大大简化了网络结构，并取得了不错的效果，并且训练时可以进行GPU加速，时间成本低


BI-GRU+Attention
对双向GRU输出的序列进行处理attention处理，然后对每一个attention结果进行softmax，相当于20分类共用了GRU的输出序列，然后对序列进行不同的attention从而实现20个类别分类。
优点：保证特征的提取同时大大简化了网络结构，和CNN模型相比略有提升
缺点：GRU层无法进行GPU加速，导致训练时间比CNN长

Bert
直接获取相应评论的Bert模型的输出，然后对该输出进行下游训练，全连接+softmax，得到分类结果
由于该方法时间成本和硬件成本都较高，本次训练只用了10%的数据进行测试，并没有取得满意效果。
结果分析：可能训练样本不足，也有可能是没有进行好的预处理。
可能的解决方法：增加训练样本，对数据进行预处理，更换Bert模型

