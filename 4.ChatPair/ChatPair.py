import numpy as np
import sys
import codecs
import time
import random
from SentenceSimMecab import sentence_sim
import multiprocessing as mp
            

def cal_sim(chat):
    sim_matrix = sentence_sim(chat)
    sim_matrix -= np.eye(sim_matrix.shape[0])
    return sim_matrix
    
    
def make_pairs(chat):
    pair_num = 240
    option = {"high":{"upper_threshold": 1.00, "lower_threshold": 0.985, "ratio": 0.334},\
              "low": {"upper_threshold": 0.91, "lower_threshold": 0.88, "ratio": 0.334}}
    start_time = time.time()

    picked = set()
    high_upper_th = option["high"]["upper_threshold"]
    high_lower_th = option["high"]["lower_threshold"]
    high_ratio = option["high"]["ratio"]
    low_upper_th = option["low"]["upper_threshold"]
    low_lower_th = option["low"]["lower_threshold"]
    low_ratio = option["low"]["ratio"]

    high_list = list()
    mid_list = list()
    low_list = list()

    sim_matrix = cal_sim(chat)

    candidate = np.where(sim_matrix >= low_lower_th)

    high_count = 0
    mid_count = 0
    low_count = 0
    for idx in range(pair_num):
        try_count = 0
        while True:
            r_idx = random.randrange(0, candidate[0].shape[0])
            t1 = candidate[0][r_idx]
            t2 = candidate[1][r_idx]
            similarity = sim_matrix[t1][t2]

            if (t1, t2) in picked or (t2, t1) in picked:
                continue
                
            if similarity >= high_lower_th:
                if high_count < pair_num * high_ratio:
                    break
            elif similarity <= low_upper_th:
                if low_count < pair_num * low_ratio:
                    break
            else:
                if mid_count <= pair_num * (1 - high_ratio - low_ratio):
                    break
            
            try_count += 1
            if try_count > 500000:
                break
                
        if try_count > 500000:
            break

        picked.add((t1, t2))
        recommend = "?"
        if similarity > high_lower_th:
            recommend = "1"
        elif similarity < low_upper_th:
            recommend = "0"

        pair_info = f"{similarity:.4f}, {recommend}, {chat[t1]}, {chat[t2]}\n"
        if recommend == "1":
            high_list.append(pair_info)
        elif recommend == "0":
            low_list.append(pair_info)
        else:
            mid_list.append(pair_info)

    return [high_list, mid_list, low_list]


def main(start, end):
    # filename = input()
    print(f"Start processing chunk #{start} ~ #{end}")
    chat_analysis = ChatAnalysis("../../Data/1to100_chat_norm6.txt", data_size=50000)

    for idx in range(start, end):
        chat_analysis.set_chat_chunk_num(idx)
        chat_analysis.calculate_similarity()
        #chat_analysis.save_chat_similarity_list(threshold=0.88)
        chat_analysis.save_chat_similar_pairs(pair_num=240, \
                                              option={"high":{"upper_threshold": 1.00, "lower_threshold": 0.985, "ratio": 0.334},\
                                                      "low": {"upper_threshold": 0.91, "lower_threshold": 0.88, "ratio": 0.334}})
        print(f"ChatPair #{idx} complete.\n")
        

if __name__ == "__main__":
    start_time = time.time()
    with open('../../Data/1to100_chat_norm1.txt', 'r', encoding='utf-8') as data_file:
        chat_data = data_file.readlines()
        chat_data = list(map(lambda chat: chat.strip(), chat_data))
        chat_data = np.array(chat_data[:22650000]).reshape(-1,50000)
        chat_data = chat_data.tolist()
    with mp.Pool(4) as pool:
        result = pool.map(make_pairs, chat_data)
    high_file = open('high.csv', 'a', encoding='utf-8')
    mid_file = open('mid.csv', 'a', encoding='utf-8')
    low_file = open('low.csv', 'a', encoding='utf-8')
    for res in result:
        high_file.writelines(res[0])
        mid_file.writelines(res[1])
        low_file.writelines(res[2])
    high_file.close()
    mid_file.close()
    low_file.close()
    print(f"time: {time.time() - start_time : .3f}")