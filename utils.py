
import os
from globalv import data_path


def label_name(img_name):
    """
    convert image name to label name
    :param img_name:
    :type img_name:
    :return:
    :rtype:
    """
    return img_name[:-4] + ".txt"


def data_split():
    """
    split training and testing data
    :return:
    :rtype:
    """
    img_name_list = [f for f in os.listdir(data_path) if f.endswith('.png') and os.path.isfile(os.path.join(data_path, f))]
    img_cnt = len(img_name_list)
    train_cnt = int(img_cnt*0.7)
    test_cnt = img_cnt - train_cnt

    with open("train.txt", "w") as file:
        for i in xrange(train_cnt):
            file.write(img_name_list[i] + '\t' + label_name(img_name_list[i]) + '\n')

    with open("test.txt", "w") as file:
        for i in xrange(test_cnt):
            file.write(img_name_list[i + train_cnt] + '\t' + label_name(img_name_list[i + train_cnt]) + '\n')
