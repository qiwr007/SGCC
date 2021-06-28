import pandas as pd
import os
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
# 导入朴素贝叶斯分类器
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt


# 可视化混淆矩阵
def cm_plot(y, yp):
    cm = confusion_matrix(y, yp)
    plt.matshow(cm, cmap=plt.cm.Blues)
    plt.colorbar()
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(y, x), horizontalalignment='center',
                         verticalalignment='center')
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
    return plt


if __name__ == '__main__':
    # 数据预处理
    file_path = os.getcwd()
    data = pd.read_csv(file_path+"/Elimination record.csv", encoding='gbk', engine='python')
    # 第一行就是一个真实的数据，需要加上一个header=None，这边不需要，直接用默认的。
    data = data.drop('设备型号', axis=1)  # 将A1那一列删除
    data = data.drop('安装地点', axis=1)  # 将安装地点那一列删除
    data.head()

    # 对原始数据集进行切分
    X_whole = data.drop('损坏性质', axis=1)  #fhjffj
    y_whole = data['损坏性质']

    # （卢利栋）将此处代码进行了修正，目前可以直接用文字作为天气标签
    # 将数据数值化，使用map函数进行映射。
    # 这边不知道为何一直报错，直接在EXCEL里面替换了
    # 下面是原来打算使用的代码
    # data['损坏时的天气']
    # data['损坏时的天气'].unique()
    label_mapping = {'晴': 1, '雷阵雨': 2, '阴': 3, '多云': 4, '冰雹': 5, '暴雨': 6, '小雨': 7, '雾': 8, '雨夹雪': 9, '大雨': 10, '大雪': 11,'沙尘暴': 12}
    data['损坏时的天气'] = data['损坏时的天气'].map(label_mapping)
    X_whole['损坏时的天气'] = data['损坏时的天气']

    """
    切分数据集
    """
    # 测试集和训练集进行切分，训练集8，测试集2
    x_train_w, x_test_w, y_train_w, y_test_w = train_test_split(X_whole, y_whole, test_size = 0.2, random_state = 0)

    # 实例化贝叶斯分类器，存在一个变量里面
    classifier = MultinomialNB(alpha=1)
    # alpha拟合模型时的平滑度，默认为1,可进行调整

    # 传入训练集数据
    classifier.fit(x_train_w, y_train_w)  # 到这儿完成了朴素贝叶斯算法的训练

    """
    训练集预测，也就是对训练集测试
    """
    # 绘制训练集混淆矩阵
    train_pred = classifier.predict(x_train_w)
    cm_plot(y_train_w, train_pred)  # 混淆矩阵

    """
    测试集预测 
    """
    test_pred = classifier.predict(x_test_w)
    cm_plot(y_test_w, test_pred)  # 混淆矩阵


    '''
    对多分类问题的评价指标。
    这边用了两个，一个是kappa系数，另一个是海明距离。
    '''

    # 用kappa系数来评价模型，取值在-1到1之间。
    # 这个系数的值越高，则代表模型实现的分类准确度越高
    from sklearn.metrics import cohen_kappa_score
    kappa = cohen_kappa_score(y_test_w, test_pred)
    print(kappa)
    # -0.20300751879699241

    # 海明距离,海明距离也适用于多分类的问题，简单来说就是衡量预测标签与真实标签之间的距离，取值在0~1之间。
    # 距离为0说明预测结果与真实结果完全相同，距离为1就说明模型与我们想要的结果完全就是背道而驰。
    from sklearn.metrics import hamming_loss
    ham_distance = hamming_loss(y_test_w, test_pred)
    print(ham_distance)
    # 0.625


    '''
    下面虚拟了一些数据，文件predict.csv文件，进行预测
    '''
    data_predict = pd.read_csv(file_path+"/predict.csv",encoding='gbk', engine='python')
    data_predict = data_predict.drop('设备型号', axis=1)#将ID那一列删除
    data_predict = data_predict.drop('安装地点', axis=1)
    X_predict_1 = data_predict.drop('损坏性质', axis=1)

    #将损坏时的天气数值化
    data_predict['损坏时的天气'] = data_predict['损坏时的天气'].map(label_mapping)
    X_predict_1['损坏时的天气']= data_predict['损坏时的天气']

    y_predict_1 = data_predict['损坏性质']
    test_pred_1 = classifier.predict_proba(X_predict_1)  #修改为预测各损坏类型的概率
    label=[
    '',
    '老化',
    '短路',
    '雷电击穿',
    '芯棒断裂',
    '受潮',
    '绝缘子断裂',
    '线圈损坏',
    '套管破裂',
    '超负荷运行',
    '工作环境过高',
    '接触面氧化过重',
    '二次开路',
    '电压过高，击穿',
    '电解液漏掉',
    '过电压击穿',
    '绕组击穿',
    '储能弹簧变形',
    ]

    i = 0
    for row in test_pred_1:
        i = i+1
        print("第"+str(i)+"行",end='\t')
        for index in np.argsort(-row):  #将数组从大到小排序并且返回下标
            print(label[classifier.classes_[index]]+":"+str(row[index]*100)[:4]+ '%', end='\t')
        print("\n", end="")
    #print(test_pred_1)




