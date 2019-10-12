import codecs
import re
import time


# Parameter
check_regexs = [re.compile(r"\*\*\* [0-9]{3,10}"),
                re.compile(r"([^ㄱ-ㅎㅏ-ㅣ가-힣\n]*\@[ㄱ-ㅎㅏ-ㅣ가-힣]+ [^ㄱ-ㅎㅏ-ㅣ가-힣\n]+|[^ㄱ-ㅎㅏ-ㅣ가-힣\n]+ \@[ㄱ-ㅎㅏ-ㅣ가-힣]+[^ㄱ-ㅎㅏ-ㅣ가-힣\n]*)")]


# Utility function
def get_chats(filename):
    with open(filename, 'r', encoding='utf-8-sig') as data_file:
        return data_file.read().splitlines()


def check_sentence(sentence):
    checked = 0
    checked_detail = [0] * len(check_regexs)
    processing_time = [0] * len(check_regexs)
    
    for idx, regex in enumerate(check_regexs):
        routine_start_time = time.time()
        result = regex.search(sentence)
        if result is not None:
            if result.start() == 0 and result.end() == len(sentence):
                checked_detail[idx] = 1
                checked = 1
        processing_time[idx] = time.time() - routine_start_time
        
    return checked, checked_detail, processing_time


def check_chats(chats):
    processing_time = [0] * len(check_regexs)

    chat_list = list()
    checked_list = list()

    passed_count = 0
    checked_count = 0
    checked_detail = [0] * len(check_regexs)

    for chat in chats:
        # Check sentence
        checked, checked_d, check_time = check_sentence(chat)
        checked_count += checked
        for idx, val in enumerate(check_time):
            processing_time[idx] += val
        for idx, val in enumerate(checked_d):
            checked_detail[idx] += val

        if checked == 0:
            chat_list.append(chat + "\n")
            passed_count += 1
        else:
            checked_list.append(chat + "\n")

    return chat_list, checked_list, [passed_count, checked_count], checked_detail, processing_time


def save_chats(filename, chat_list, checked_list):
    filename_split = filename.split(".")
    chat_filename = ".".join(filename_split[:-1]) + "_post." + filename_split[-1]
    checked_filename = ".".join(filename_split[:-1]) + "_skipped." + filename_split[-1]

    with codecs.open(chat_filename, 'w', encoding='utf-8') as output_file:
        output_file.writelines(chat_list)
    with codecs.open(checked_filename, 'w', encoding='utf-8') as output_file:
        output_file.writelines(checked_list)


def analyze_result(count, checked_detail, processing_time):
    total_time = sum(processing_time)

    total_count = sum(count)
    passed_count = count[0]
    checked_count = count[1]

    print("")
    print("Total processing time: %.3f secs" % (total_time))
    print("1. *** Number (View bot) : %.3f secs" % (processing_time[0]))
    print("2. @Korean and English   : %.3f secs" % (processing_time[1]))
    print("")
    print("Total chats: %d" % total_count)
    print("Passed chats : %d (%.2f%%)" % (passed_count, passed_count / total_count * 100))
    print("Checked chats: %d (%.2f%%)" % (checked_count, checked_count / total_count * 100))
    print("  1. *** Number (View bot): %d (%.2f%%)" % (checked_detail[0], checked_detail[0] / checked_count * 100))
    print("  2. @Korean and English  : %d (%.2f%%)" % (checked_detail[1], checked_detail[1] / checked_count * 100))

    
    with codecs.open("result.txt", 'w', encoding='utf-8') as output_file:
        output_file.write("Total processing time: %.3f secs\n" % (total_time))
        output_file.write("Total processing time: %.3f secs\n" % (total_time))
        output_file.write("1. *** Number (View bot) : %.3f secs\n" % (processing_time[0]))
        output_file.write("2. @Korean and English   : %.3f secs\n" % (processing_time[1]))
        output_file.write("\n")
        output_file.write("Total chats: %d\n" % total_count)
        output_file.write("Passed chats : %d (%.2f%%)\n" % (passed_count, passed_count / total_count * 100))
        output_file.write("Checked chats: %d (%.2f%%)\n" % (checked_count, checked_count / total_count * 100))
        output_file.write("  1. *** Number (View bot): %d (%.2f%%)\n" % (checked_detail[0], checked_detail[0] / checked_count * 100))
        output_file.write("  2. @Korean and English  : %d (%.2f%%)\n" % (checked_detail[1], checked_detail[1] / checked_count * 100))

# Main function
def main():
    filename = "../../Data/1to100_normal_190827_2331.txt" #input("filename: ")
    chats = get_chats(filename)
    chat_list, checked_list, count, checked_detail, processing_time = check_chats(chats)
    save_chats(filename, chat_list, checked_list)
    analyze_result(count, checked_detail, processing_time)


if __name__ == "__main__":
    main()

