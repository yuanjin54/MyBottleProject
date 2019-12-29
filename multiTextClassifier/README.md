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




