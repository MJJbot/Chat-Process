from sklearn.cluster import AgglomerativeClustering
import numpy as np
import codecs
import time
from SentenceSimMecab import sentence_sim


cluster_num = 7500
data_size = 50000
algorithm = "past"
past_threshold = float(input("past_threshold: "))#0.98
chunk_num = 0

start_time = time.time()
filename = "../../Data/1to100_chat_norm5.txt" #input("filename: ")
with open(filename, 'r', encoding='utf-8-sig') as data_file:
    chats = data_file.readlines()
    chats = list(map(lambda chat: chat.strip(), chats)) # to delete newline character
print(len(chats))
print("File open time: %.3f secs" % (time.time() - start_time))


start_time = time.time()
sim_matrix = sentence_sim(chats[data_size * chunk_num : data_size * (chunk_num+ 1)])
print("Similarity calc time: %.3f secs" % (time.time() - start_time))


start_time = time.time()
if algorithm == "hc":
    clusterer = AgglomerativeClustering(n_clusters=cluster_num, affinity='precomputed', linkage='average').fit(1 - sim_matrix)
    clusters = [[] for _ in range(cluster_num)]
    label_list = clusterer.labels_
    for idx in range(len(label_list)):
        clusters[label_list[idx]].append(idx)
elif algorithm == "past":
    clusters = []
    idx_x, idx_y = np.where(sim_matrix > past_threshold)
    for idx in range(len(idx_x)):
        x, y = idx_x[idx], idx_y[idx]
        if y <= x:
            continue
        cluster_exist = False
        for cluster_idx in range(len(clusters)):
            if x in clusters[cluster_idx]:
                cluster_exist = True
                clusters[cluster_idx].add(y)
                break
        if cluster_exist == False:
            cluster = {x, y}
            clusters.append(cluster)

cluster_lens = list()
for idx in range(len(clusters)):
    cluster_lens.append((len(clusters[idx]), idx))
cluster_lens.sort(reverse=True)
print("time: %.3f secs" % (time.time() - start_time))


with codecs.open(f"{algorithm}_{len(clusters)}_{data_size}({chunk_num})({past_threshold}).txt", 'w', encoding='utf-8') as output_file:
    for len, idx in cluster_lens:
        if len == 1:
            continue
        output_file.write("---------------------------------------\n")
        for chat in clusters[idx]:
            output_file.write(chats[chat] + '\n')


exit()

similarity_threshold = 0.92

start_time = time.time()
close_chats = np.where(sim_matrix > similarity_threshold)
relate_counts = [[0, idx] for idx in range(data_size)]
for idx in range(len(close_chats[0])):
    relate_counts[close_chats[0][idx]][0] += 1
relate_counts.sort(reverse=True)
print(relate_counts[:30])
print("time: %.3f secs" % (time.time() - start_time))


for idx in range(30):
    print(chats[relate_counts[idx][1]])

