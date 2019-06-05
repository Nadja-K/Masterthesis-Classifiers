from classifiers.classifier import Classifier


db = '../data/databases/dataset_excellent_onesize.db'
t_q, t_c, t_e, _ = Classifier.load_datasplit(db, 'train')
e_q, e_c, e_e, _ = Classifier.load_datasplit(db, 'test')
v_q, v_c, v_e, _ = Classifier.load_datasplit(db, 'val')


print(t_e & e_e)
print(t_e & v_e)
print(e_e & v_e)

def collect_sentences(query, context):
    out = set()
    for sample in query:
        out.add(sample['sentence'])
    for sample in context:
        out.add(sample['sentence'])
    return out

train_sentences = collect_sentences(t_q, t_c)
test_sentences = collect_sentences(e_q, e_c)
val_sentences = collect_sentences(v_q, v_c)

print(len(train_sentences & test_sentences))
print(len(train_sentences & val_sentences))
print(len(val_sentences & test_sentences))

print(len(t_e | e_e | v_e))
print(len(train_sentences | test_sentences | val_sentences))