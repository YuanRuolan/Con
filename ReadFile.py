import pandas as pd
from pandas.core import algorithms
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pyreadstat as pr
from sympy import *
import statsmodels.api as sm
import numpy as np
from tqdm import tqdm


#读取学生数据集和家长数据集
def readFile():
    student,smeta=pr.read_sav("/Users/yuanruolan/Desktop/ceps数据/SPSS-CEPS基线（13-14）/Chinese/SPSS格式/CEPS基线调查学生数据.SAV")
    parent,pmeta=pr.read_sav("/Users/yuanruolan/Desktop/ceps数据/SPSS-CEPS基线（13-14）/Chinese/SPSS格式/CEPS基线调查家长数据.SAV")
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

    # 计算加权平均值
    def weighted_averageb28(row):
        weights = [1, 1, 1, 1, 1, 1]
        return sum(
            w * row[col] for w, col in zip(weights, data[['b2801', 'b2802', 'b2803', 'b2804', 'b2805', 'b2806']]))

    data['b28'] = data.apply(weighted_averageb28, axis=1)

    # 处理b15g1,b15g2数据不一致问题，将两列合并成一列
    def b15g12(data):
        data['b15']=data['b15g1']*60+data['b15g2']
        return data
    data=b15g12(data)

    for i in range(6):
        str1='b280'+str(i+1)
        data.drop(str1,axis=1,inplace=True)

    data.drop('b15g1', axis=1, inplace=True)
    data.drop('b15g2', axis=1, inplace=True)
    data.insert(6, "b15", data.pop("b15"))
    data.insert(7, "b28", data.pop("b28"))

    origin=data.copy()  #尚未归一化的数据
    # 数据规范化
    for column in data.columns:
        data[column]=(data[column]-data[column].min())/(data[column].max()-data[column].min())
    return data,origin


'''
最终有用的
["b01：1，2","b08a：1-9","b08b：1-9","b09：1-5","ba13:数值","b15：g1:0,1;g2:数值","b28:1-6","stprrel:1,2","stmedu:1-9","stfedu:1-9","stcog","cog3pl"]
'''














