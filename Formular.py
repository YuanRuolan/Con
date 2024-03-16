from sympy import *
import pandas as pd
from Callculation import calculation

def statistics(data):
    med={}
    x =['b08a', 'b08b', 'stmedu', 'stfedu','ba13','stprrel']
    for i in x:
        med[i]=data[i].median()
    return med

#将列名转换成数组
def getColumnslist(data):
    columns=[column for column in data]
    return columns



def formular():
    coefs,intercepts,data,origin=calculation()
    part_of_varible = statistics(data)  # 字典记录只受自己影响的属性的值
    columns = getColumnslist(data)
    columns.remove('ids')
    columns.remove('cog3pl')
    print(columns)
    print(origin.head(4))
    #生成系数矩阵
    matrix=[]

    # stmedu-x1=0
    initial_ls=[0]*(len(columns)+1)
    initial_ls[columns.index('stmedu')]=1
    initial_ls[-1]=part_of_varible['stmedu']
    #print(initial_ls)
    matrix.append(initial_ls)

    # stfedu-x2=0
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('stfedu')] = 1
    initial_ls[-1] = part_of_varible['stfedu']
    #print(initial_ls)
    matrix.append(initial_ls)

    # b08a-x3=0
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('b08a')] = 1
    initial_ls[-1] = part_of_varible['b08a']
    #print(initial_ls)
    matrix.append(initial_ls)

    # b08b-x4=0
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('b08b')] = 1
    initial_ls[-1] = part_of_varible['b08b']
    #print(initial_ls)
    matrix.append(initial_ls)

    # ba13-x5=0
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('ba13')] = 1
    initial_ls[-1] = part_of_varible['ba13']
    #print(initial_ls)
    matrix.append(initial_ls)

    # stprrel-x6=0
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('stprrel')] = 1
    initial_ls[-1] = part_of_varible['stprrel']
    #print(initial_ls)
    matrix.append(initial_ls)

    #
    # 0=w1*b08a+w2*b08b-b09+w3*stmedu+w4*stfedu+e
    #['b01', 'b08a', 'b08b', 'b09', 'ba13', 'b15', 'b28',
    # 'stprrel', 'stmedu', 'stfedu', 'stcog', 'cog3pl']
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('b08a')] = coefs[0][0]
    initial_ls[columns.index('b08b')] = coefs[0][1]
    initial_ls[columns.index('b09')] = -1
    initial_ls[columns.index('stmedu')] = coefs[0][2]
    initial_ls[columns.index('stfedu')] = coefs[0][3]
    initial_ls[-1] = -intercepts[0]
    #print(initial_ls)
    matrix.append(initial_ls)

    # 0=w1*b09-b01+e
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('b09')] = coefs[1][0]
    initial_ls[columns.index('b01')] = -1
    initial_ls[-1] = -intercepts[1]
    #print(initial_ls)
    matrix.append(initial_ls)

    # 0=w1*stprrel+w2ba13-b28+e
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('stprrel')] = coefs[2][0]
    initial_ls[columns.index('ba13')] =coefs[2][1]
    initial_ls[columns.index('b28')] = -1
    initial_ls[-1] = -intercepts[2]
    #print(initial_ls)
    matrix.append(initial_ls)

    # 0=-b15+w1*stprrel+e
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('stprrel')] = coefs[3][0]
    initial_ls[columns.index('b15')] = -1
    initial_ls[-1] = -intercepts[3]
    #print(initial_ls)
    matrix.append(initial_ls)

    # 0=-stcog/cog3plw1*stmedu+w2*stfedu+w3*b08a+w4*b08b+w5*b09+w6*b01+w7*stprrel+w8*b15+w10*b28+w11*ba13+e
    initial_ls = [0] * (len(columns) + 1)
    initial_ls[columns.index('stmedu')] = coefs[4][0]
    initial_ls[columns.index('stfedu')] = coefs[4][1]
    initial_ls[columns.index('stcog')] = -1
    initial_ls[columns.index('b08a')] = coefs[4][2]
    initial_ls[columns.index('b08b')] = coefs[4][3]
    initial_ls[columns.index('b09')] = coefs[4][4]
    initial_ls[columns.index('b01')] = coefs[4][5]
    initial_ls[columns.index('stprrel')] = coefs[4][6]
    initial_ls[columns.index('b15')] = coefs[4][7]
    initial_ls[columns.index('b28')] = coefs[4][8]
    initial_ls[columns.index('ba13')] = coefs[4][9]
    initial_ls[-1] = -intercepts[4]
    #print(initial_ls)
    matrix.append(initial_ls)

    # print(tuple(matrix))


    eq = Matrix(tuple(matrix))
    vir=[]
    for i in columns:
        vir.append(Symbol(i))
    result = linsolve(eq, vir)
    print("================result===================")
    count=0
    for i in list(result)[0]:
        i=i*(origin[columns[count]].max())
        print(columns[count],":",i)
        count+=1
    print("================result===================")