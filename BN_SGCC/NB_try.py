import sklearn
import pandas as pd
import os
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
# 导入朴素贝叶斯分类器
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print('hello')
    # 数据预处理
    file_path = os.getcwd()
    data = pd.read_csv(file_path+"/fake_data.csv", encoding='gbk', engine='python')

