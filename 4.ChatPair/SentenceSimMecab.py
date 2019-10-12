from gensim.test.utils import datapath
from gensim.models.fasttext import load_facebook_vectors
import numpy as np
from konlpy.tag import Mecab
mecab = Mecab()

#cap_path = datapath("/home/ubuntu/seungho/fastText/build/run8_chat_mecab.bin")
cap_path = datapath("/home/ubuntu/seungho/fastText/build/run9_chat_mecab_190818_2237.bin")
model = load_facebook_vectors(cap_path)
example = model['안녕']

def get_sentence_vec(A):
    res = mecab.morphs(A)
    vec = np.zeros_like(example)
    for morph in res:
        vec += model[morph]
    return vec

def sentence_sim(list_of_sent):
    list_of_sent_vec = list()
    for sent in list_of_sent:
        list_of_sent_vec.append(get_sentence_vec(sent))
    A = np.array(list_of_sent_vec)
    inner = np.matmul(A, A.T)
    B = np.linalg.norm(A, axis=1, keepdims=True)
    norm = np.matmul(B, B.T)
    sim = inner / norm
    return sim