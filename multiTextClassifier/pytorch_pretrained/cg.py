import logging
logger = logging.getLogger(__name__)
vocab = load_vocab(vocab_file)
vocab = load_vocab(bert_path+'/vocab.txt')

ids_to_tokens = collections.OrderedDict(
            [(ids, tok) for tok, ids in vocab.items()])
max_len =30
pad_size = 32
def convert_tokens_to_ids(tokens):
    """Converts a sequence of tokens into ids using the vocab."""
    ids = []
    for token in tokens:
        ids.append(vocab[token])
    if len(ids) > max_len:
        logger.warning(
            "Token indices sequence length is longer than the specified maximum "
            " sequence length for this BERT model ({} > {}). Running this"
            " sequence through BERT will result in indexing errors".format(len(ids), self.max_len)
        )
    return ids
