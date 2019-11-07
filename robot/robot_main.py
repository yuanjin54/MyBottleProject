import pandas as pd
import re
import os
import numpy as np
import tensorflow as tf
import time
from gensim.models import Word2Vec
import jieba
from tqdm import tqdm  # 用于显示进度条的
import logging

import warnings

warnings.filterwarnings('ignore')

# cur_path = '/Users/yuanjin/PycharmProjects/MyBottleProject/robot/'
cur_path = '/home/student/project/project-01/ase/robot/'


def save_log():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('robot.log', mode='w')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


logger = save_log()

# filename = '../../nlp_data_set/project04/qa_corpus.csv'
filename = '/home/student/dataset/project-4/qa_corpus.csv'
data = pd.read_csv(filename)
# 去除缺失的空值
data = data.dropna()
data = data.drop(['qid'], 1)
# 对去除以后的内容重新分配index
data = data.reset_index(drop=True)

answers = data['answer'].tolist()
questions = data['question'].tolist()


def is_chinese(word):
    for ch in list(word):
        if ch < u'\u4e00' or ch > u'\u9fff':
            return False
    return True


stopwords = [line.strip() for line in open(cur_path + 'stopwords.txt', 'r', encoding='utf8').readlines()]


# 切词并去掉停用词
def get_contents(texts, isRemoveStopword=False):
    contents = []
    for text in tqdm(texts):
        sentence = ''.join(re.findall(r'\w+', text))
        copy_words = []
        words = list(jieba.cut(sentence))
        for word in words:
            # if is_chinese(word):
            if isRemoveStopword and word in stopwords: continue
            copy_words.append(word)
        contents.append(' '.join(words))
    return contents


logger.info('Running remove stop the word')

clean_answers = get_contents(answers)
# clean_questions = get_contents(questions, isRemoveStopword=True)
clean_questions = get_contents(questions, isRemoveStopword=False)


# 统计整个词库单词的个数，形式为{‘垃圾’:897,'非常':234,....}
def count_words(count_dict, text):
    for setence in text:
        for word in setence.split():
            # if not is_chinese(word): continue
            if word not in count_dict:
                count_dict[word] = 1
            else:
                count_dict[word] += 1


# 单词的字典，也就是说word_count存储单词的词频，不包括重复单词
word_counts = {}
count_words(word_counts, clean_answers)
count_words(word_counts, clean_questions)
print("总的单词数量为 :", len(word_counts))
logger.info("总的单词数量为 :{}".format(str(len(word_counts))))

# 将训练好的向量以字典形式存储,第一步加载词向量，word2vec_model最终的形式为{‘垃圾’:(词向量)，‘漂亮’:(词向量),...}
word2vec_model = Word2Vec.load(cur_path + 'word2vec/word2vec.model')

# 查看词典中有多少单词不在训练好的词向量空间中
missing_words = 0
for word, count in word_counts.items():
    if word not in word2vec_model:
        missing_words += 1  # 统计不在词向量的字典中的个数,且满足经常出现条件
missing_ratio = round(missing_words / len(word_counts), 4) * 100
print("Number of words missing from CN:", missing_words)
print("大概有 {}% 的单词不在训练好的词向量模型中。".format(missing_ratio))
logger.info("Number of words missing from CN: {}".format(missing_words))
logger.info("大概有 {}% 的单词不在训练好的词向量模型中。".format(missing_ratio))

# 其实这里的意思是给word_counts里面的每个词编个号[('您', 0), ('可以', 1), ...]
vocab_to_int = {}
value = 0
# 将单词映射为整数
for word, count in word_counts.items():
    if word in word2vec_model:
        vocab_to_int[word] = value
        value += 1
# 特殊符号
codes = ["<UNK>", "<PAD>", "<EOS>", "<GO>"]
for code in codes:
    vocab_to_int[code] = len(vocab_to_int)

# 颠倒vocab_to_int
int_to_vocab = {}
for word, value in vocab_to_int.items():
    int_to_vocab[value] = word
usage_ratio = round(len(vocab_to_int) / len(word_counts), 4) * 100

embedding_dim = 300
nb_words = len(vocab_to_int)
# 初始化词向量，最后得到word_embedding_matrix为矩阵shape为nb_words * 300
word_embedding_matrix = np.zeros((nb_words, embedding_dim), dtype=np.float32)
for word, i in vocab_to_int.items():
    if word in word2vec_model:
        word_embedding_matrix[i] = word2vec_model[word]
    else:
        # 随机初始化一个向量
        new_embedding = np.array(np.random.uniform(-1.0, 1.0, embedding_dim))
        word_embedding_matrix[i] = new_embedding


# 将setence中的单词形成数字[[1,234,7687,23,...],[345,908,2359,11234,...],...]
def convert_to_ints(text, word_count, unk_count, eos=False):
    ints = []
    for setence in text:
        setence_ints = []  # 一个句子里面每个词的编号
        for word in setence.split():
            word_count += 1
            if word in vocab_to_int:
                setence_ints.append(vocab_to_int[word])
            else:
                setence_ints.append(vocab_to_int['<UNK>'])
                unk_count += 1
        if eos:
            setence_ints.append(vocab_to_int['<EOS>'])
        ints.append(setence_ints)
    return ints, word_count, unk_count


word_count = 0
unk_count = 0
# int_answers和int_questions格式为[[1,234,7687,23,...],[345,908,2359,11234,...],...] 里面存的都是每个词的编号
int_answers, word_count, unk_count = convert_to_ints(clean_answers, word_count, unk_count)
int_questions, word_count, unk_count = convert_to_ints(clean_questions, word_count, unk_count, eos=True)

unk_percent = round(unk_count / word_count, 4) * 100
print("Total number of words:", word_count)
print("Total number of UNKs:", unk_count)
print("Percent of words that are UNK: {}%".format(unk_percent))
logger.info("Total number of words: ".format(word_count))
logger.info("Total number of UNKs: {}".format(unk_count))
logger.info("Percent of words that are UNK: {}%".format(unk_percent))

print("tf path {}".format(tf.__path__))
print("tf version {}".format(tf.__version__))


def create_lengths(text):
    lengths = []
    for setence in text:
        lengths.append(len(setence))
    return pd.DataFrame(lengths, columns=['counts'])


lengths_answers = create_lengths(int_answers)
lengths_questions = create_lengths(int_questions)


# 统计unk的数目，为下一步筛选有效训练集做准备
def unk_counter(setence):
    unk_count = 0
    for word in setence:
        if word == vocab_to_int['<UNK>']:
            unk_count += 1
    return unk_count


sorted_answers = []
sorted_questions = []
max_question_length = 42
max_answer_length = 484
min_length = 1
unk_question_limit = 1
unk_answer_limit = 0
# 按长度排序，循环中count为序号
for length in range(min(lengths_questions.counts), max_question_length):
    for count, words in enumerate(int_answers):
        if (len(int_answers[count]) >= min_length and
                len(int_answers[count]) <= max_answer_length and
                len(int_questions[count]) >= min_length and
                unk_counter(int_answers[count]) <= unk_answer_limit and
                unk_counter(int_questions[count]) <= unk_question_limit and
                length == len(int_questions[count])
        ):
            sorted_answers.append(int_answers[count])
            sorted_questions.append(int_questions[count])

logger.info("以上得到经预处理后长短排序升序的questions")


# 以上得到经预处理后长短排序升序的questions

# 为输入定义占位符
def model_inputs():
    input_data = tf.placeholder(tf.int32, [None, None], name='input')  # 应该是batch_size*dimensions，batch_size*句长
    targets = tf.placeholder(tf.int32, [None, None], name='targets')  # 应该是batch_size*句长
    lr = tf.placeholder(tf.float32, name='learning_rate')  # 学习率应该更小一些
    keep_prob = tf.placeholder(tf.float32, name='keep_prob')  # 防止过拟合
    answer_length = tf.placeholder(tf.int32, (None,), name='answer_length')  # answer的长度
    max_answer_length = tf.reduce_max(answer_length, name='max_dec_len')  # tf.reduce_max()计算各个维度上元素的最大值
    question_length = tf.placeholder(tf.int32, (None,), name='question_length')  # question的长度
    return input_data, targets, lr, keep_prob, answer_length, max_answer_length, question_length


# 每个batch开始阶段加<GO>
def process_encoding_input(target_data, vocab_to_int, batch_size):  # target就是answer
    ending = tf.strided_slice(target_data, [0, 0], [batch_size, -1], [1, 1])  # 三维切片，每一维切割都是来自于上一维切割的结果
    dec_input = tf.concat([tf.fill([batch_size, 1], vocab_to_int['<GO>']), ending], 1)
    return dec_input


# 创建encoding层
def encoding_layer(rnn_size, sequence_length, num_layers, rnn_inputs, keep_prob):
    for layer in range(num_layers):
        with tf.variable_scope('encoder_{}'.format(layer)):
            cell_fw = tf.nn.rnn_cell.BasicLSTMCell(rnn_size)
            cell_fw = tf.nn.rnn_cell.DropoutWrapper(cell_fw, input_keep_prob=keep_prob)
            cell_bw = tf.nn.rnn_cell.BasicLSTMCell(rnn_size)
            cell_bw = tf.nn.rnn_cell.DropoutWrapper(cell_bw, input_keep_prob=keep_prob)
            enc_output, enc_state = tf.nn.bidirectional_dynamic_rnn(cell_fw,
                                                                    cell_bw,
                                                                    rnn_inputs,
                                                                    sequence_length,
                                                                    dtype=tf.float32)
        enc_output = tf.concat(enc_output, 2)
    return enc_output, enc_state  # enc_output应该为中间向量


def training_decoding_layer(dec_embed_input,
                            answer_length,
                            dec_cell,
                            initial_state,
                            output_layer,
                            vocab_size,
                            max_answer_length):  # 用于训练模型
    training_helper = tf.contrib.seq2seq.TrainingHelper(inputs=dec_embed_input,
                                                        sequence_length=answer_length,
                                                        time_major=False)  # 帮助建立一个训练的decoder类
    training_decoder = tf.contrib.seq2seq.BasicDecoder(dec_cell,
                                                       training_helper,
                                                       initial_state,
                                                       output_layer)  # 构造一个decoder
    training_logits, _, _ = tf.contrib.seq2seq.dynamic_decode(training_decoder,
                                                              output_time_major=False,
                                                              impute_finished=True,
                                                              maximum_iterations=max_answer_length)
    # 构造一个动态的decoder,返回(final_outputs, final_state, final_sequence_lengths).final_outputs是一个namedtuple，
    # 里面包含两项(rnn_outputs, sample_id)
    return training_logits


def inference_decoding_layer(embeddings,
                             start_token,
                             end_token,
                             dec_cell,
                             initial_state,
                             output_layer,
                             max_answer_length,
                             batch_size):  # decoding，解码要有<GO>和<EOS>，用于预测
    start_token = tf.tile(tf.constant([start_token], dtype=tf.int32),
                          [batch_size],
                          name='start_token')  # tile扩展向量
    inference_helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(embeddings, start_token,
                                                                end_token)  # 方便最后预测，seq2seq中帮助建立Decoder的一个类，在预测时使用
    inference_decoder = tf.contrib.seq2seq.BasicDecoder(dec_cell, inference_helper, initial_state,
                                                        output_layer)  # 构造一个decoder
    inference_logits, _, _ = tf.contrib.seq2seq.dynamic_decode(inference_decoder,
                                                               output_time_major=False,
                                                               impute_finished=True,
                                                               maximum_iterations=max_answer_length)
    return inference_logits


# decoding层
def decoding_layer(dec_embed_input, embeddings, enc_output, enc_state, vocab_size, question_length, answer_length,
                   max_answer_length, rnn_size, vocab_to_int, keep_prob, batch_size, num_layers):
    for layer in range(num_layers):
        with tf.variable_scope('decoder_{}'.format(layer)):
            lstm = tf.nn.rnn_cell.LSTMCell(rnn_size, initializer=tf.random_uniform_initializer(-0.1, 0.1, seed=2))
            dec_cell = tf.nn.rnn_cell.DropoutWrapper(lstm, input_keep_prob=keep_prob)
    output_layer = tf.layers.Dense(vocab_size, kernel_initializer=tf.truncated_normal_initializer(mean=0.0,
                                                                                                  stddev=0.1))  # 构造一个全连接的类，后续的vocab_size= len(vocab_to_int)+1仍需弄清楚
    attn_mech = tf.contrib.seq2seq.BahdanauAttention(rnn_size, enc_output, question_length, normalize=False)  # 集中机制
    dec_cell = tf.contrib.seq2seq.AttentionWrapper(dec_cell, attn_mech, rnn_size)
    initial_state = dec_cell.zero_state(batch_size=batch_size, dtype=tf.float32).clone(cell_state=enc_state[0])
    #     initial_state = tf.contrib.seq2seq.AttentionWrapperState(cell_state=enc_state[0],attention=dec_cell,time=0,alignments=(),alignment_history=(),attention_state=())#可以理解为只给第一个，然后
    # initial_state = dec_cell.zero_state(dtype=tf.float32, batch_size=batch_size)
    with tf.variable_scope("decode"):
        training_logits = training_decoding_layer(dec_embed_input, answer_length, dec_cell, initial_state, output_layer,
                                                  vocab_size, max_answer_length)
    with tf.variable_scope("decode", reuse=True):
        inference_logits = inference_decoding_layer(embeddings, vocab_to_int['<GO>'], vocab_to_int['<EOS>'], dec_cell,
                                                    initial_state, output_layer, max_answer_length, batch_size)
    return training_logits, inference_logits


def seq2seq_model(input_data, target_data, keep_prob, question_length, answer_length, max_answer_length, vocab_size,
                  rnn_size, num_layers, vocab_to_int, batch_size):
    embeddings = word_embedding_matrix  # 因为要预测所有的词，所以是全体词汇表的长度
    enc_embed_input = tf.nn.embedding_lookup(embeddings, input_data)
    enc_output, enc_state = encoding_layer(rnn_size, question_length, num_layers, enc_embed_input, keep_prob)
    dec_input = process_encoding_input(target_data, vocab_to_int, batch_size)
    dec_embed_input = tf.nn.embedding_lookup(embeddings, dec_input)
    training_logits, inference_logits = decoding_layer(dec_embed_input, embeddings, enc_output, enc_state, vocab_size,
                                                       question_length, answer_length, max_answer_length, rnn_size,
                                                       vocab_to_int, keep_prob, batch_size, num_layers)
    return training_logits, inference_logits


# 构造pad层
def pad_sentence_batch(sentence_batch):  # pad层填充
    max_sentence = max([len(sentence) for sentence in sentence_batch])
    return [sentence + [vocab_to_int['<PAD>']] * (max_sentence - len(sentence)) for sentence in sentence_batch]


def get_batches(answers, questions, batch_size):  # 获取数据
    for batch_i in range(0, len(questions) // batch_size):
        start_i = batch_i * batch_size
        answers_batch = answers[start_i:start_i + batch_size]
        questions_batch = questions[start_i:start_i + batch_size]
        pad_answers_batch = np.array(pad_sentence_batch(answers_batch))
        pad_questions_batch = np.array(pad_sentence_batch(questions_batch))
        pad_answers_lengths = []
        for answer in pad_answers_batch:
            pad_answers_lengths.append(len(answer))
        pad_questions_lengths = []
        for question in pad_questions_batch:
            pad_questions_lengths.append(len(question))
        yield pad_answers_batch, pad_questions_batch, pad_answers_lengths, pad_questions_lengths


# epochs = 100
epochs = 100
# batch_size = 64
batch_size = 256
rnn_size = 256
num_layers = 2
learning_rate = 0.005
keep_probability = 0.75

train_graph = tf.Graph()
with train_graph.as_default():
    input_data, targets, lr, keep_prob, answer_length, max_answer_length, question_length = model_inputs()
    training_logits, inference_logits = seq2seq_model(tf.reverse(input_data, [-1]), targets, keep_prob, question_length,
                                                      answer_length
                                                      , max_answer_length, len(vocab_to_int), rnn_size, num_layers,
                                                      vocab_to_int, batch_size)  # -1说明将其颠倒过来以后方便联系
    training_logits = tf.identity(training_logits.rnn_output, 'logits')  # 保存每个单词的概率，用于计算loss
    inference_logits = tf.identity(inference_logits.sample_id, name='predictions')  # 保存最后的单词结果
    masks = tf.sequence_mask(answer_length, max_answer_length, dtype=tf.float32,
                             name='masks')  # engths代表的是一个一维数组，代表每一个sequence的长度，那么该函数返回的是一个mask的张量，张量的维数是：(lengths.shape,maxlen)
    with tf.name_scope("optimization"):
        cost = tf.contrib.seq2seq.sequence_loss(training_logits, targets,
                                                masks)  # 用于计算seq2seq中的loss。当我们的输入是不定长的时候，weights参数常常使用我们1.11中得到的mask
        optimizer = tf.train.AdamOptimizer(lr)
        gradients = optimizer.compute_gradients(cost)
        capped_gradients = [(tf.clip_by_value(grad, -5., 5.), var) for grad, var in gradients if
                            grad is not None]  # 输入一个张量A，把A中的每一个元素的值都压缩在min和max之间。小于min的让它等于min，大于max的元素的值等于max
        train_op = optimizer.apply_gradients(capped_gradients)  # 梯度修剪主要避免训练梯度爆炸和消失问题
print("Graph is built")
logger.info('Graph is built')

start = 0
end = start + len(sorted_answers)
sorted_answers_short = sorted_answers[start:end]
sorted_questions_short = sorted_questions[start:end]
print('The shortest question length: ', len(sorted_questions_short[0]))
print('The longest question length: ', len(sorted_questions_short[-1]))
print('The shortest answer length: ', len(sorted_answers_short[0]))
print('The longest answer length: ', len(sorted_answers_short[-1]))

logger.info('Starting Training ...')

learning_rate_decay = 0.95
min_learning_rate = 0.0005
display_step = 20
stop_early = 0
stop = 3
per_epoch = 3
update_check = (len(sorted_questions_short) // batch_size // per_epoch) - 1

update_loss = 0
batch_loss = 0

answer_update_loss = []
checkpoint = "best_model.ckpt"
with tf.Session(graph=train_graph) as sess:
    sess.run(tf.global_variables_initializer())
    for epoch_i in range(1, epochs + 1):
        update_loss = 0
        batch_loss = 0
        for batch_i, (answers_batch, questions_batch, answers_lengths, questions_lengths) in enumerate(
                get_batches(sorted_answers_short, sorted_questions_short, batch_size)):
            start_time = time.time()
            feed_dict = {input_data: questions_batch, targets: answers_batch, lr: learning_rate,
                         answer_length: answers_lengths, question_length: questions_lengths,
                         keep_prob: keep_probability}
            _, loss = sess.run([train_op, cost], feed_dict=feed_dict)
            batch_loss += loss
            update_loss += loss
            end_time = time.time()
            batch_time = end_time - start_time
            if batch_i % display_step == 0 and batch_i > 0:
                print('Epoch{:>3}/{} Batch {:>4}/{} - Loss: {:>6.3f}, Seconds:{:>4.2f}'.format(epoch_i, epochs, batch_i,
                                                                                               len(
                                                                                                   sorted_questions_short) // batch_size,
                                                                                               batch_loss / display_step,
                                                                                               batch_time * display_step))
                logger.info(
                    'Epoch{:>3}/{} Batch {:>4}/{} - Loss: {:>6.3f}, Seconds:{:>4.2f}'.format(epoch_i, epochs, batch_i,
                                                                                             len(
                                                                                                 sorted_questions_short) // batch_size,
                                                                                             batch_loss / display_step,
                                                                                             batch_time * display_step))
            if batch_i % update_check == 0 and batch_i > 0:
                print("Average loss for this update:", round(update_loss / update_check, 3))
                logger.info("Average loss for this update: {}".format(str(round(update_loss / update_check, 3))))
                answer_update_loss.append(update_loss)
                # 如果update_loss最小，则保存模型
                if update_loss <= min(answer_update_loss):
                    print('New Record')
                    logger.info('New Record')
                    stop_early = 0
                    saver = tf.train.Saver()
                    saver.save(sess, os.path.join(cur_path, checkpoint))
                else:
                    print('No Improvement')
                    logger.info('No Improvement')
                    stop_early += 1
                    if stop_early == stop:
                        break
                update_loss = 0
        learning_rate *= learning_rate_decay
        if learning_rate < min_learning_rate:
            learning_rate = min_learning_rate
        if stop_early == stop:
            print("Stopping Training")
            logger.info('Stopping Training')
            break
    logger.info('Training finished!')
    print('Training finished!')
