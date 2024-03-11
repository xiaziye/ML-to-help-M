from nltk.tokenize import sent_tokenize
import re

file_path = "./train.txt"
save_path = "./train_save.txt."


def sen_split(sens, sen_list):
    for sentence in sens:
        sentence = re.sub(r'[^\w\s]', '', sentence)  # 去除标点符号
        sentence = re.sub(r'\d+', '', sentence)
        sentence = sentence.lower()  # 大写变小写
        if sentence != '':
            sentence = sentence + '\n'
            sen_list.append(sentence)
    return sen_list


if __name__ == "__main__":
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
        sentences = sent_tokenize(data)
        char_sen = list()
        result = sen_split(sentences, char_sen)
        f.close()
    with open(save_path, 'w+', encoding='utf-8') as f:
        for re_l in result:
            f.write(re_l)
