import json
from nltk import word_tokenize


def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line)


def doccano2BIO(file_name, output_file='out.txt'):
    def _get_pair():
        global end_offset1
        data = load_jsonl(file_name)
        for line in data:
            text = line['text']
            words, labels_ = list(), list()
            for ent in line['entities']:
                label, start_offset, end_offset = ent['label'], ent['start_offset'], ent['end_offset']
                if not words:
                    words = word_tokenize(text[0:start_offset], language="english")
                    labels_ = ['O'] * len(words)
                    word_labeled = word_tokenize(text[start_offset:end_offset], language="english")
                    words.extend(word_labeled)
                    labels_.append('B-' + label)
                    labels_.extend(['I-' + label] * (len(word_labeled) - 1))
                    end_offset1 = end_offset
                else:
                    word_o = word_tokenize(text[end_offset1 + 1: start_offset], language="english")
                    words.extend(word_o)
                    labels_.extend(['O'] * len(word_o))
                    word_labeled = word_tokenize(text[start_offset:end_offset], language="english")
                    words.extend(word_labeled)
                    labels_.append('B-' + label)
                    labels_.extend(['I-' + label] * (len(word_labeled) - 1))
                    end_offset1 = end_offset
                if end_offset1 < len(text):
                    word_o = word_tokenize(text[end_offset1 + 1: -1], language="english")
                    words.extend(word_o)
                    labels_.extend(['O'] * len(word_o))
            yield words, labels_

    with open(output_file, 'w+', encoding='utf-8') as f:
        content = []
        for text, labels in _get_pair():
            if text:
                s = []
                item = zip(list(text), labels)
                for line in item:
                    s.append(' '.join(line) + '\n')
                s = ''.join(s)[:-1]
                content.append(s)
        content = "\n\n".join(content)
        f.write(content)


if __name__ == '__main__':
    doccano2BIO('test.jsonl', 'test.txt')
