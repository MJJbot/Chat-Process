from gensim.test.utils import datapath
from gensim.models.fasttext import load_facebook_vectors
import numpy as np
from khaiii import KhaiiiApi
api = KhaiiiApi()

#cap_path = datapath("/home/ubuntu/seungho/fastText/build/run6_chat_khaiii.bin")
#cap_path = datapath("/home/ubuntu/seungho/fastText/build/run7_wiki+namu+chat_khaiii.bin")
cap_path = datapath("/home/ubuntu/seungho/fastText/build/run4_wiki+namu_khaiii.bin")
model = load_facebook_vectors(cap_path)

def get_sentence_vec(A):
    res = api.analyze(A)
    vec = np.zeros_like(model['안녕'])
    for word in res:
        for morph in word.morphs:
            vec += model[morph.lex]
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