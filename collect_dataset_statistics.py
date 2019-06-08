from classifiers.classifier import Classifier
from bert import tokenization
import numpy as np


db = '../data/databases/dataset_geraete_small.db'
t_q, t_c, t_e, _ = Classifier.load_datasplit(db, 'train')
e_q, e_c, e_e, _ = Classifier.load_datasplit(db, 'test')
v_q, v_c, v_e, _ = Classifier.load_datasplit(db, 'val')


def collect_sentences(query, context):
    out = set()
    for sample in query:
        out.add(sample['sentence'])
    for sample in context:
        out.add(sample['sentence'])
    return out


def get_avg_token_len(data, tokenizer, token_lens):
    for i, sample in enumerate(data):
        s = str(sample['sentence'])
        tokens, mapping = tokenizer.tokenize(s)
        token_lens.append(len(tokens))

    print("Avg. number of tokens: %s\n"
          "Std. deviation: %s\n"
          "Min: %s \tMax: %s" % ((sum(token_lens) / len(token_lens)), np.std(token_lens), min(token_lens), max(token_lens)))
    return token_lens


train_sentences = collect_sentences(t_q, t_c)
test_sentences = collect_sentences(e_q, e_c)
val_sentences = collect_sentences(v_q, v_c)

print("Train and Test entity union: %s" % (t_e & e_e))
print("Train and Val entity union: %s" % (t_e & v_e))
print("Val and Test entity union: %s" % (e_e & v_e))

print("Number of shared sentences in Train and Test: %s" % len(train_sentences & test_sentences))
print("Number of shared sentences in Train and Val: %s" % len(train_sentences & val_sentences))
print("Number of shared sentences in Val and Test: %s" % len(val_sentences & test_sentences))

print("Number of all entities in Train Test and Val: %s" % len(t_e | e_e | v_e))
print("Number of all sentences in Train, Test and Val: %s" % len(train_sentences | test_sentences | val_sentences))


# Calculate the avg. number of tokens per sentence for a dataset
tokenizer = tokenization.FullTokenizer(vocab_file="../bert/models/vocab.txt", do_lower_case=True)
token_lens = []
token_lens = get_avg_token_len(t_q, tokenizer, token_lens)
token_lens = get_avg_token_len(t_c, tokenizer, token_lens)

token_lens = get_avg_token_len(v_q, tokenizer, token_lens)
token_lens = get_avg_token_len(v_c, tokenizer, token_lens)

token_lens = get_avg_token_len(e_q, tokenizer, token_lens)
token_lens = get_avg_token_len(e_c, tokenizer, token_lens)

print("%s (%0.2f%%) sentences with > 128 tokens" % (len([token_len for token_len in token_lens if token_len > 128]), (100/len(token_lens))*len([token_len for token_len in token_lens if token_len > 128])))
print("%s (%0.2f%%) sentences with > 256 tokens" % (len([token_len for token_len in token_lens if token_len > 256]), (100/len(token_lens))*len([token_len for token_len in token_lens if token_len > 256])))
