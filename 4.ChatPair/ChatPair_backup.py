import numpy as np
import sys
import codecs
import time
import random
from SentenceSimMecab import sentence_sim

class ChatAnalysis:
    def __init__(self, filename="chat.txt", data_size=50000, verbose=True):
        self.filename = filename
        self.data_size = data_size
        self.verbose = verbose
        self.sim_matrix = None
        
        start_time = time.time()
        with open(self.filename, 'r', encoding='utf-8-sig') as data_file:
            self.chat_data = data_file.readlines()
        self.chat_data = list(map(lambda chat: chat.strip(), self.chat_data))
        
        if self.verbose:
            print(f"Chat load time: {time.time() - start_time:.3f} secs")
            print(f"Total chat count: {len(self.chat_data)}")
    
    def get_chat_data(self, chat_num_in_range):
        return self.chat_data[chat_num_in_range + self.data_size * self.chunk_num]
    
    def get_chat_chunk_range(self):
        return (self.data_size * self.chunk_num, self.data_size * (self.chunk_num + 1))
    
    def set_chat_chunk_num(self, chunk_num):
        self.chunk_num = chunk_num
        self.sim_matrix = None
        
        chat_range = self.get_chat_chunk_range()
        
        if self.verbose:
            print(f"Using chat #{chat_range[0]} ~ #{chat_range[1] - 1}")
    
    def calculate_similarity(self):
        start_time = time.time()
        
        chat_range = self.get_chat_chunk_range()
        self.sim_matrix = sentence_sim(self.chat_data[chat_range[0] : chat_range[1]])
        self.sim_matrix -= np.eye(self.sim_matrix.shape[0])
        
        if self.verbose:
            print(f"Similarity calculation time: {time.time() - start_time:.3f} secs")
            print(f"Similarity matrix of #{chat_range[0]} ~ #{chat_range[1] - 1} chats is saved")
                
    def save_chat_similarity_list(self, threshold=0.8):
        if self.sim_matrix is None:
            print("Please run calculate_silimarity() first.")
            return
        
        start_time = time.time()
        
        sim_rank_per_chat = [list()] * self.sim_matrix.shape[0]
        for idx in range(len(sim_rank_per_chat)):
            sim_rank_per_chat[idx] = [(self.sim_matrix[idx][t_idx], t_idx) for t_idx in range(self.sim_matrix.shape[1])]
            sim_rank_per_chat[idx].sort(reverse=True)

        if self.verbose:
            print(f"Similarity calculation time: {time.time() - start_time:.3f} secs")
        
        filename = f"ChatSimList({self.chunk_num})_{self.data_size}({threshold}).txt"
        with codecs.open(filename, 'w', encoding='utf-8') as output_file:
            output_file.write("----------------------------------------------------------------------\n")
            for idx, chat_sims in enumerate(sim_rank_per_chat):
                output_file.write(f"Pivot : {idx:5d} - {self.get_chat_data(idx)}\n")
                for pair in chat_sims:
                    if pair[0] > threshold:
                        output_file.write(f"{pair[0]:.4f}: {pair[1]:5d} - {self.get_chat_data(pair[1])}\n")
                    else:
                        break
                output_file.write("----------------------------------------------------------------------\n")
        
        if self.verbose:
            print(f"Chat similarity list is saved to {filename}")
            
    def save_chat_similar_pairs(self, pair_num=100,\
                                option={"high":{"upper_threshold": 1.00, "lower_threshold": 0.95, "ratio": 0.3},\
                                        "low": {"upper_threshold": 0.90, "lower_threshold": 0.85, "ratio": 0.3}}):
        start_time = time.time()
        
        picked = set()
        high_upper_th = option["high"]["upper_threshold"]
        high_lower_th = option["high"]["lower_threshold"]
        high_ratio = option["high"]["ratio"]
        low_upper_th = option["low"]["upper_threshold"]
        low_lower_th = option["low"]["lower_threshold"]
        low_ratio = option["low"]["ratio"]
        print(high_upper_th, high_lower_th, high_ratio, low_upper_th, low_lower_th, low_ratio)
        
        filename = f"ChatPairs({self.chunk_num})_{self.data_size}({pair_num}).csv.txt"
        filename_high = f"ChatPairs_high({self.chunk_num})_{self.data_size}({int(pair_num * high_ratio)}).csv.txt"
        filename_mid = f"ChatPairs_mid({self.chunk_num})_{self.data_size}({int(pair_num * (1 - high_ratio - low_ratio))}).csv.txt"
        filename_low = f"ChatPairs_low({self.chunk_num})_{self.data_size}({int(pair_num * low_ratio)}).csv.txt"
        
        output_file = codecs.open(filename, 'w', encoding='utf-8')
        output_file_high = codecs.open(filename_high, 'w', encoding='utf-8')
        output_file_mid = codecs.open(filename_mid, 'w', encoding='utf-8')
        output_file_low = codecs.open(filename_low, 'w', encoding='utf-8')
        
        for idx in range(pair_num):
            while True:
                t1 = random.randrange(0, self.data_size)
                t2 = random.randrange(0, self.data_size)
                similarity = self.sim_matrix[t1][t2]
                progress = idx / pair_num
                
                if similarity < low_lower_th: #or similarity > high_upper_th:
                    continue
                if (t1, t2) in picked or (t2, t1) in picked:
                    continue
                if progress < high_ratio:
                    if similarity >= high_lower_th:
                        break
                elif progress > 1 - low_ratio:
                    if similarity <= low_upper_th:
                        break
                else:
                    if similarity < high_lower_th and similarity > low_upper_th:
                        break

            picked.add((t1, t2))
            recommend = "?"
            if similarity > high_lower_th:
                recommend = "1"
            elif similarity < low_upper_th:
                recommend = "0"

            pair_info = f"{recommend}, {similarity:.4f}, {t1}, {self.get_chat_data(t1)}, {t2}, {self.get_chat_data(t2)}\n"
            output_file.write(pair_info)
            if recommend == "1":
                output_file_high.write(pair_info)
            elif recommend == "0":
                output_file_low.write(pair_info)
            else:
                output_file_mid.write(pair_info)

            print(f"{self.chunk_num}: {idx} / {pair_num}")

        output_file.close()
        output_file_high.close()
        output_file_mid.close()
        output_file_low.close()
        
        if self.verbose:
            print(f"Chat pairing time: {time.time() - start_time:.3f} secs")
            print(f"Chat pairs are saved to {filename}")
            print(f"Chat high pairs are saved to {filename_high}")
            print(f"Chat low pairs are saved to {filename_low}")

def main(start, end):
    # filename = input()
    print(f"Start processing chunk #{start} ~ #{end}")
    chat_analysis = ChatAnalysis("../../Data/1to100_chat_norm6.txt", data_size=50000)

    for idx in range(start, end):
        chat_analysis.set_chat_chunk_num(idx)
        chat_analysis.calculate_similarity()
        #chat_analysis.save_chat_similarity_list(threshold=threshold)
        chat_analysis.save_chat_similar_pairs(pair_num=100, \
                                              option={"high":{"upper_threshold": 1.00, "lower_threshold": 0.985, "ratio": 0.334},\
                                                      "low": {"upper_threshold": 0.93, "lower_threshold": 0.88, "ratio": 0.334}})
        print(f"ChatPair #{idx} complete.\n")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))