import random


def random_split_jsonl(file_path):
    data = list()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(line)
        random.shuffle(data)
        trainset = data[:int(0.7 * len(data))]
        validset = data[int(0.7 * len(data)):int(0.85 * len(data))]
        testset = data[int(0.85 * len(data)):]

    out = [['train',trainset], ['valid',validset], ['test',testset]]
    for out_path, data in out:
        with open(out_path+'.jsonl', 'w', encoding='utf-8') as f:
            for line in data:
                f.writelines(line)


if __name__ == '__main__':
    random_split_jsonl('LinearAlgebra_data.jsonl')
