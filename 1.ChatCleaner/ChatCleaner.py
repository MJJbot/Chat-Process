import codecs
import re
import time


# Parameter
length_minimum = 5
length_maximum = 50
set_minimum = 5
whitelist_regex = re.compile(r"([^@!#$%^&*(),.?\":{}|`~<>\[\]\-_=+\\/;'a-zA-Z0-9\u3131-\u318E\uAC00-\uD7A3\u1100-\u11f9\s]|http)")
normalize_regexs = [(re.compile(r"([@!#$%^&*(),.?\":{}|`~<>\[\]\-_=+\\/;'\u3131-\u318E\uAC00-\uD7A3])(\1{2})\1+"), "\\1\\2"),
                    (re.compile(r"[z\u314C\u314B]{2,}"), "\u314B"), # zㅌㅋ -> "ㅋ"
                    (re.compile(r"[\u3154\u3156]{2,}"), "\u314B"), # ㅔㅖ -> "ㅔ"
                    (re.compile(r"[\u3160\u315C]{2,}"), "\u3160"), # ㅠㅜ -> "ㅠ"
                    (re.compile(r"(!|\?|\~|\;| )\1+"), "\\1"), # ?, !, ~, ' ' -> "?", "!", "~", " "
                    (re.compile(r"(\.|\,|ㄷ|ㄴ|ㄱ)\1{2,}"), "\\1\\1")] # '.', ',', ㄷ, ㄴ, ㄱ -> "..", ",,", "ㄷㄷ", "ㄴㄴ", "ㄱㄱ"
korean_regex = re.compile(r"[\u3131-\u318E\uAC00-\uD7A3\u1100-\u11f9]")
english_regex = re.compile(r"[a-zA-Z]")
question_rules = {' 머임', '머예요', '뭐예요', '머에요', '인가요', '건가요', '시나요', '있나요', '하나요', ' 뭐임', '셨나요', '되나요', '뭐에요', '신가요', '을까요', '어때요', ' 어떰', '누구임', '습니까', '닐까요'}


# Utility function
def get_chats(filename):
    with open(filename, 'r', encoding='utf-8-sig') as data_file:
        return [chat.split('\t') for chat in data_file.read().splitlines()]

def get_emoticons_set(filename):
    with open(filename, 'r', encoding='utf-8-sig') as data_file:
        return set(data_file.read().splitlines())


def is_system_message(user, sentence):
    #####TEMP#####
    if user == "Twipkr" or user == "REMS2BOT":
        return True
    #####TEMP#####
    if "gifted" in sentence or "gifting" in sentence or "Gift Sub" in sentence or "subscribe" in sentence or "new here" in sentence or "have joined" in sentence:
        return True
    elif "Thanks for the gift sub" in sentence or ("정기구독권 선물" in sentence and "@" in sentence):
        return True
    return False


def is_simple_sentence(sentence):
    characters = set()
    for char in sentence:
        if char not in characters:
            characters.add(char)
            if len(characters) >= set_minimum:
                return False
    return True


def is_question(sentence):
    if sentence[0] == "?" or sentence[1] == "?":
        return False
    if "?" in sentence:
        return True
    else:
        if sentence[:-3] in question_rules:
            return True
        else:
            return False


def is_contain_other_character(sentence):
    if whitelist_regex.search(sentence) is None:
        return False
    else:
        return True


def is_duplicated(sentence, sentence_set):
    if sentence.replace(" ", "") in sentence_set:
        return True
    else:
        return False


def is_english_only(sentence):
    korean_char_count = len(korean_regex.findall(sentence))
    english_char_count = len(english_regex.findall(sentence))
    
    if english_char_count > 0 and korean_char_count == 0:
        return True
    else:
        return False


def normalize_emoticons(sentence, emoticons_set):
    words = sentence.split(" ")
    for word in words:
        if word in emoticons_set:
            sentence = sentence.replace(word, "")
    return sentence


def normalize_sentence(sentence):
    processing_time = [0] * len(normalize_regexs)
    normalized_count = [0] * len(normalize_regexs)
    for idx, regex in enumerate(normalize_regexs):
        routine_start_time = time.time()
        sentence, normalized_count[idx] = regex[0].subn(regex[1], sentence)
        processing_time[idx] = time.time() - routine_start_time
    return sentence, processing_time, [1 if sum(normalized_count) > 0 else 0, normalized_count]


def clean_chats(chats, emoticons_set):
    start_time = time.time()
    processing_time = {"length": 0, "system": 0, "simple": 0, "filter": 0, "eng_only": 0, "normalize": [0] * (len(normalize_regexs) + 1), "duplicate": 0, "question": 0}

    chat_set = set()
    chat_list = list()
    question_list = list()
    normal_list = list()

    skipped_chat_count = {"filter": 0, "length": 0, "system": 0, "simple": 0, "duplicate": 0, "eng_only": 0}
    processed_chat_count = {"chat": 0, "question": 0}
    normalized_count = [0, [0] * (len(normalize_regexs) + 1)]

    for chat in chats:
        user = chat[0]
        message = chat[1]
        
        # Normalize emoticons
        routine_start_time = time.time()
        message = normalize_emoticons(message, emoticons_set)
        processing_time["normalize"][0] += time.time() - routine_start_time

        # check length
        routine_start_time = time.time()
        if len(message) < length_minimum or len(message) > length_maximum:
            skipped_chat_count["length"] += 1
            continue
        processing_time["length"] += time.time() - routine_start_time

        # check system message
        routine_start_time = time.time()
        if is_system_message(user, message):
            skipped_chat_count["system"] += 1
            continue
        processing_time["system"] += time.time() - routine_start_time

        # check simple sentence
        routine_start_time = time.time()
        if is_simple_sentence(message):
            skipped_chat_count["simple"] += 1
            continue
        processing_time["simple"] += time.time() - routine_start_time

        # filter characters
        routine_start_time = time.time()
        if is_contain_other_character(message):
            skipped_chat_count["filter"] += 1
            continue
        processing_time["filter"] += time.time() - routine_start_time
        
        # check english only
        routine_start_time = time.time()
        if is_english_only(message):
            skipped_chat_count["eng_only"] += 1
            continue
        processing_time["eng_only"] += time.time() - routine_start_time

        # Normalize sentence
        message, normalize_time, count = normalize_sentence(message)
        normalized_count[0] += count[0]
        for idx, val in enumerate(normalize_time):
            processing_time["normalize"][idx + 1] += val
        for idx, val in enumerate(count[1]):
            normalized_count[1][idx + 1] += val

        # check duplication
        routine_start_time = time.time()
        if is_duplicated(message, chat_set):
            skipped_chat_count["duplicate"] += 1
            continue
        processing_time["duplicate"] += time.time() - routine_start_time

        chat_set.add(message.replace(" ", ""))
        chat_list.append(message + "\n")
        processed_chat_count["chat"] += 1

        # 6. check question
        routine_start_time = time.time()
        if is_question(message):
            question_list.append(message + "\n")
            processed_chat_count["question"] += 1
        else:
            normal_list.append(message + "\n")
        processing_time["question"] += time.time() - routine_start_time

        

    return chat_list, question_list, normal_list, [time.time() - start_time, processing_time], [skipped_chat_count, processed_chat_count, normalized_count]


def save_chats_and_questions(filename, chat_list, question_list, normal_list):
    filename_split = filename.split(".")
    chat_filename = ".".join(filename_split[:-1]) + "_total." + filename_split[-1]
    question_filename = ".".join(filename_split[:-1]) + "_question." + filename_split[-1]
    normal_filename = ".".join(filename_split[:-1]) + "_normal." + filename_split[-1]

    with codecs.open(chat_filename, 'w', encoding='utf-8') as output_file:
        output_file.writelines(chat_list)
    with codecs.open(question_filename, 'w', encoding='utf-8') as output_file:
        output_file.writelines(question_list)
    with codecs.open(normal_filename, 'w', encoding='utf-8') as output_file:
        output_file.writelines(normal_list)


def analyze_result(processing_time, count):
    total_time = processing_time[0]
    routine_time = processing_time[1]

    skipped = count[0]
    processed = count[1]
    normalized = count[2]

    total_skipped = sum(skipped.values())
    total = total_skipped + processed["chat"]
    total_normalized = sum(normalized[1])

    print("")
    print("Total processing time: %.3f secs" % (total_time))
    print("0. Check length     : %.3f secs" % (routine_time["length"]))
    print("1. Check system msg : %.3f secs" % (routine_time["system"]))
    print("2. Check simplicity : %.3f secs" % (routine_time["simple"]))
    print("3. Check char filter: %.3f secs" % (routine_time["filter"]))
    print("4. Check char filter: %.3f secs" % (routine_time["eng_only"]))
    print("5. Normalize chat   : %.3f secs" % (sum(routine_time["normalize"])))
    print("    0. Normalize emoticon: %.3f secs" % (routine_time["normalize"][0]))
    print("    0. Normalize general : %.3f secs" % (routine_time["normalize"][1]))
    print("    1. Normalize ㅋㅋ     : %.3f secs" % (routine_time["normalize"][2]))
    print("    2. Normalize ㅔㅖ     : %.3f secs" % (routine_time["normalize"][3]))
    print("    3. Normalize ㅠㅜ     : %.3f secs" % (routine_time["normalize"][4]))
    print("    4. Normalize ?!      : %.3f secs" % (routine_time["normalize"][5]))
    print("    5. Normalize .,;     : %.3f secs" % (routine_time["normalize"][6]))
    print("6. Check duplication: %.3f secs" % (routine_time["duplicate"]))
    print("7. Check question   : %.3f secs" % (routine_time["question"]))
    print("")
    print("Total chats: %d" % total)
    print("Skipped chats: %d (%.2f%%)" % (total_skipped, total_skipped / total * 100))
    print("  0. Skipped chats by char filter : %d (%.2f%%)" % (skipped["filter"], skipped["filter"] / total_skipped * 100))
    print("  1. Skipped chats by short length: %d (%.2f%%)" % (skipped["length"], skipped["length"] / total_skipped * 100))
    print("  2. Skipped chats by system msg  : %d (%.2f%%)" % (skipped["system"], skipped["system"] / total_skipped * 100))
    print("  3. Skipped chats by simplicity  : %d (%.2f%%)" % (skipped["simple"], skipped["simple"] / total_skipped * 100))
    print("  4. Skipped chats by duplication : %d (%.2f%%)" % (skipped["duplicate"], skipped["duplicate"] / total_skipped * 100))
    print("  5. Skipped chats by english only: %d (%.2f%%)" % (skipped["eng_only"], skipped["eng_only"] / total_skipped * 100))
    print("Processed chats: %d (%.2f%%)" % (processed["chat"], processed["chat"] / total * 100))
    print("  Processed normal chats: %d (%.2f%%)" % (processed["chat"] - processed["question"], 100 - (processed["question"] / processed["chat"] * 100)))
    print("  Processed questions   : %d (%.2f%%)" % (processed["question"], processed["question"] / processed["chat"] * 100))
    print("")
    print("Normalized chats: %d (%.2f%%), total %d words" % (normalized[0], normalized[0] / processed["chat"] * 100, total_normalized))
    print("  0. Normalized general: %d (%.2f%%)" % (normalized[1][1], normalized[1][1] / total_normalized * 100))
    print("  1. Normalized ㅋㅋ    : %d (%.2f%%)" % (normalized[1][2], normalized[1][2] / total_normalized * 100))
    print("  2. Normalized ㅔㅖ    : %d (%.2f%%)" % (normalized[1][3], normalized[1][3] / total_normalized * 100))
    print("  3. Normalized ㅠㅜ    : %d (%.2f%%)" % (normalized[1][4], normalized[1][4] / total_normalized * 100))
    print("  4. Normalized ?!     : %d (%.2f%%)" % (normalized[1][5], normalized[1][5] / total_normalized * 100))
    print("  5. Normalized .,;    : %d (%.2f%%)" % (normalized[1][6], normalized[1][6] / total_normalized * 100))
    
    with codecs.open("result.txt", 'w', encoding='utf-8') as output_file:
        output_file.write("Total processing time: %.3f secs\n" % (total_time))
        output_file.write("0. Check length     : %.3f secs\n" % (routine_time["length"]))
        output_file.write("1. Check system msg : %.3f secs\n" % (routine_time["system"]))
        output_file.write("2. Check simplicity : %.3f secs\n" % (routine_time["simple"]))
        output_file.write("3. Check char filter: %.3f secs\n" % (routine_time["filter"]))
        output_file.write("4. Check char filter: %.3f secs\n" % (routine_time["eng_only"]))
        output_file.write("5. Normalize chat   : %.3f secs\n" % (sum(routine_time["normalize"])))
        output_file.write("    0. Normalize emoticon: %.3f secs\n" % (routine_time["normalize"][0]))
        output_file.write("    0. Normalize general : %.3f secs\n" % (routine_time["normalize"][1]))
        output_file.write("    1. Normalize ㅋㅋ     : %.3f secs\n" % (routine_time["normalize"][2]))
        output_file.write("    2. Normalize ㅔㅖ     : %.3f secs\n" % (routine_time["normalize"][3]))
        output_file.write("    3. Normalize ㅠㅜ     : %.3f secs\n" % (routine_time["normalize"][4]))
        output_file.write("    4. Normalize ?!      : %.3f secs\n" % (routine_time["normalize"][5]))
        output_file.write("    5. Normalize .,;     : %.3f secs\n" % (routine_time["normalize"][6]))
        output_file.write("6. Check duplication: %.3f secs\n" % (routine_time["duplicate"]))
        output_file.write("7. Check question   : %.3f secs\n" % (routine_time["question"]))
        output_file.write("\n")
        output_file.write("Total chats: %d\n" % total)
        output_file.write("Skipped chats: %d (%.2f%%)\n" % (total_skipped, total_skipped / total * 100))
        output_file.write("  0. Skipped chats by char filter : %d (%.2f%%)\n" % (skipped["filter"], skipped["filter"] / total_skipped * 100))
        output_file.write("  1. Skipped chats by short length: %d (%.2f%%)\n" % (skipped["length"], skipped["length"] / total_skipped * 100))
        output_file.write("  2. Skipped chats by system msg  : %d (%.2f%%)\n" % (skipped["system"], skipped["system"] / total_skipped * 100))
        output_file.write("  3. Skipped chats by simplicity  : %d (%.2f%%)\n" % (skipped["simple"], skipped["simple"] / total_skipped * 100))
        output_file.write("  4. Skipped chats by duplication : %d (%.2f%%)\n" % (skipped["duplicate"], skipped["duplicate"] / total_skipped * 100))
        output_file.write("  5. Skipped chats by english only: %d (%.2f%%)\n" % (skipped["eng_only"], skipped["eng_only"] / total_skipped * 100))
        output_file.write("Processed chats: %d (%.2f%%)\n" % (processed["chat"], processed["chat"] / total * 100))
        output_file.write("  Processed normal chats: %d (%.2f%%)\n" % (processed["chat"] - processed["question"], 100 - (processed["question"] / processed["chat"] * 100)))
        output_file.write("  Processed questions   : %d (%.2f%%)\n" % (processed["question"], processed["question"] / processed["chat"] * 100))
        output_file.write("\n")
        output_file.write("Normalized chats: %d (%.2f%%), total %d words\n" % (normalized[0], normalized[0] / processed["chat"] * 100, total_normalized))
        output_file.write("  0. Normalized general: %d (%.2f%%)\n" % (normalized[1][1], normalized[1][1] / total_normalized * 100))
        output_file.write("  1. Normalized ㅋㅋ    : %d (%.2f%%)\n" % (normalized[1][2], normalized[1][2] / total_normalized * 100))
        output_file.write("  2. Normalized ㅔㅖ    : %d (%.2f%%)\n" % (normalized[1][3], normalized[1][3] / total_normalized * 100))
        output_file.write("  3. Normalized ㅠㅜ    : %d (%.2f%%)\n" % (normalized[1][4], normalized[1][4] / total_normalized * 100))
        output_file.write("  4. Normalized ?!     : %d (%.2f%%)\n" % (normalized[1][5], normalized[1][5] / total_normalized * 100))
        output_file.write("  5. Normalized .,;    : %d (%.2f%%)\n" % (normalized[1][6], normalized[1][6] / total_normalized * 100))

# Main function
def main():
    filename = "../../Data/1to100.txt" #input("filename: ")
    filname_emoticons = "../../Data/emoticons.txt" #input("filename: ")
    chats = get_chats(filename)
    emoticons_set = get_emoticons_set(filname_emoticons)
    chat_list, question_list, normal_list, processing_time, count = clean_chats(chats, emoticons_set)
    save_chats_and_questions(filename, chat_list, question_list, normal_list)
    analyze_result(processing_time, count)


if __name__ == "__main__":
    main()

