import pandas as pd
from pandas.core import algorithms
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pyreadstat as pr
import statsmodels.api as sm
import numpy as np

#读取学生数据集和家长数据集
def readFile():
    student,smeta=pr.read_sav("data/CEPS基线调查学生数据.SAV")
    parent,pmeta=pr.read_sav("data/CEPS基线调查家长数据.SAV")
    student=pd.DataFrame(student)
    parent=pd.DataFrame(parent)
    #抽取目标列合并
    stu_columns_to_merge=["ids","b01","b08a","b08b","b09","b15g1","b15g2","b2801","b2802","b2803","b2804","b2805","b2806","stprrel","stmedu","stfedu","stcog","cog3pl"]
    par_columns_to_merge=["ids","ba13"]
    student=student[stu_columns_to_merge]
    parent=parent[par_columns_to_merge]
    data=student.merge(parent,left_on="ids",right_on="ids")
    data.insert(13,"ba13",data.pop("ba13"))
    # 检查是否有空值
    #print(data[data.isnull().T.any()])
    #删除带有空值的行
    data=data.dropna(axis=0,how='any')
    #空值处理后查看每个属性的缺失率
    #print((data.isnull().sum()/len(data))*100)

    #数据规范化
    for column in data.columns:
        data[column]=(data[column]-data[column].min())/(data[column].max()-data[column].min())

    # 计算加权平均值
    def weighted_averageb28(row):
        weights = [1, 1, 1, 1, 1, 1]
        return sum(w * row[col] for w, col in zip(weights, data[['b2801', 'b2802', 'b2803', 'b2804', 'b2805', 'b2806']]))
    data['b28'] = data.apply(weighted_averageb28,axis=1)

    def weighted_averageb15(row):
        weights = [1, 1]
        return sum(w * row[col] for w, col in zip(weights, data[['b15g1','b15g2']]))
    data['b15'] = data.apply(weighted_averageb15, axis=1)
    print(data.columns)
    return data


def columns():
    data=readFile()
    columns=data.columns


def main():
    columns()

if __name__=="__main__":
    main()

#计算各个因素的权重和e
def calculation():
    '''
    stmedu=x1
    stfedu=x2
    b08a=x3
    b08b=x4
    b09=w1(b08a+b08b)+w2(stmedu+stfedu)+e
    b01=w1*b09+e
    ba13=x5
    b2801-b2806=w1*stprrel+w2ba13+e
    b15g1/b15g2=w1*stprrel+e
    stprrel=x6
    stcog/cog3pl=w1*stmedu+w2*stfedu+w3*b08a+w4*08b+w5*b09+w6*b01+w7*stprrel+w8*b15+w10*b28+w11*ba13+e
    '''
    f=np.zeros([10,12])             #用于存储方程组
    data=readFile()

    #x_train, x_test, y_train, y_test = train_test_split(x, y_stcog, train_size=0.25, stratify=y_stcog)

    print("=====================================================")
    print("b09 = w1*b08a + w2*b08b + w3*stmedu + w4*stfedu + e")
    print("-----------------------------------------------------")
    x = data[['b08a', 'b08b', 'stmedu', 'stfedu']]
    y = data['b09']
    model = LinearRegression()
    model.fit(x, y)
    print("intercept:",model.intercept_)
    print("coef:",model.coef_)

    print("=====================================================")
    print("                    b01=w1*b09+e")
    print("-----------------------------------------------------")
    x = data[['b09']]
    y = data['b01']
    model = LinearRegression()
    model.fit(x, y)
    print("intercept:", model.intercept_)
    print("coef:", model.coef_)

    print("=====================================================")
    print("            b2801~b2806=w1*stprrel+w2*ba13+e")
    print("-----------------------------------------------------")
    x = data[['stprrel','ba13']]
    y=data['b28']
    model = LinearRegression()
    model.fit(x, y)
    print("intercept:", model.intercept_)
    print("coef:", model.coef_)

    print("=====================================================")
    print("              b15g1/b15g2=w1*stprrel+e")
    print("-----------------------------------------------------")
    x = data[['stprrel']]
    y = data['b15']
    model = LinearRegression()
    model.fit(x, y)
    print("intercept:", model.intercept_)
    print("coef:", model.coef_)




