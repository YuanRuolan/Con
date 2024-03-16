import ReadFile
import pandas as pd
from pandas.core import algorithms
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pyreadstat as pr
from sympy import *
import statsmodels.api as sm
import numpy as np
from tqdm import tqdm


#计算各个因素的权重和e
def calculation():
    # stmedu-x1=0
    # stfedu-x2=0
    # b08a-x3=0
    # b08b-x4=0
    # ba13-x5=0
    # stprrel-x6=0
    #
    # 0=w1*b08a+w2*b08b-b09+w3*stmedu+w4*stfedu+e
    # 0=w1*b09-b01+e
    # 0=w1*stprrel+w2ba13-b28+e
    # 0=-b15+w1*stprrel+e
    # 0=-stcog/cog3plw1*stmedu+w2*stfedu+w3*b08a+w4*08b+w5*b09+w6*b01+w7*stprrel+w8*b15+w10*b28+w11*ba13+e

    data,origin = ReadFile.readFile()
    coefs=[]
    intercepts=[]

    #x_train, x_test, y_train, y_test = train_test_split(x, y_stcog, train_size=0.25, stratify=y_stcog)

    # print("=====================================================")
    # print("b09 = w1*b08a + w2*b08b + w3*stmedu + w4*stfedu + e")
    # print("-----------------------------------------------------")
    x = data[['b08a', 'b08b', 'stmedu', 'stfedu']]
    y = data['b09']
    model = LinearRegression()
    model.fit(x, y)
    # print("intercept:",model.intercept_)
    # print("coef:",model.coef_)
    coefs.append(model.coef_)
    intercepts.append(model.intercept_)

    # print("=====================================================")
    # print("                    b01=w1*b09+e")
    # print("-----------------------------------------------------")
    x = data[['b09']]
    y = data['b01']
    model = LinearRegression()
    model.fit(x, y)
    # print("intercept:", model.intercept_)
    # print("coef:", model.coef_)
    coefs.append(model.coef_)
    intercepts.append(model.intercept_)

    # print("=====================================================")
    # print("            b2801~b2806=w1*stprrel+w2*ba13+e")
    # print("-----------------------------------------------------")
    x = data[['stprrel','ba13']]
    y=data['b28']
    model = LinearRegression()
    model.fit(x, y)
    # print("intercept:", model.intercept_)
    # print("coef:", model.coef_)
    coefs.append(model.coef_)
    intercepts.append(model.intercept_)

    # print("=====================================================")
    # print("              b15g1/b15g2=w1*stprrel+e")
    # print("-----------------------------------------------------")
    x = data[['stprrel']]
    y = data['b15']
    model = LinearRegression()
    model.fit(x, y)
    # print("intercept:", model.intercept_)
    # print("coef:", model.coef_)
    coefs.append(model.coef_)
    intercepts.append(model.intercept_)

    # print("=====================================================")
    # print("stcog/cog3pl=w1*stmedu+w2*stfedu+w3*b08a+w4*b08b+w5*b09+w6*b01+w7*stprrel+w8*b15+w10*b28+w11*ba13+e")
    # print("-----------------------------------------------------")
    x = data[['stmedu','stfedu','b08a','b08b','b09','b01','stprrel','b15','b28','ba13']]
    y = data['stcog']
    model = LinearRegression()
    model.fit(x, y)
    # print("intercept:", model.intercept_)
    # print("coef:", model.coef_)
    coefs.append(model.coef_)
    intercepts.append(model.intercept_)

    return coefs,intercepts,data,origin


