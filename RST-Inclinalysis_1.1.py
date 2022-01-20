'''
其實我不是很會寫程式 Q Q
'''
import pandas as pd
import numpy as np
import time
from matplotlib import pyplot as plt

file_path = 'B1(65).csv'

def reading(file_path):
    data = pd.read_csv(file_path, skiprows=17)
    info_read = pd.read_csv(file_path, names=['0', '1', '2'], nrows= 16)
    struct_time = time.strptime("%s %s"%(info_read['1'][7], info_read['2'][7]), '%m/%d/%Y %H:%M:%S')
    
    info = {'Site' : info_read['1'][3],
            'Borehole' : info_read['1'][4],
            'Time_stamp' : int(time.mktime(struct_time)),
            'Time_String' : time.strftime('%Y-%m-%d', struct_time),
            'Depth' : [float(info_read['1'][8]), float(info_read['2'][8])],
            'Interval' : float(info_read['1'][9]),
            'Data_A' : (data['Face A+']-data['Face A-'])/2,
            'Data_B' : (data['Face B+']-data['Face B-'])/2,
            'Check_sum_A' : data['Face A+']+data['Face A-'],
            'Check_sum_B' : data['Face B+']+data['Face B-']}

    return info


def compare(Base, Select): #輸入兩個Data列表
    if len(Select) > len(Base):
        print("Base file cannot shorter then Select file.")
        return
    
    if len(Base) > len(Select):
        Select = np.hstack((Select, Base[len(Select):]))
    
    def cumulate(input_list):
        cumulated_list = []
        for i in range(len(input_list)):
            cumulated_list.append(sum(input_list[i:len(input_list)]))
        return np.array(cumulated_list) 
    
    return cumulate(Select-Base)


def plot(Base, Select):
    max_depth = Base['Depth'][0]
    select_depth = Select['Depth'][0]
    
    if select_depth < max_depth:
        print("Base file cannot shorter then Select file.")
        return
    
    Select_line_X = compare(Base['Data_A'], Select['Data_A'])
    Select_line_Y = [-0.5 * i for i in range(1, len(Select_line_X)+1)]
    
    Base_line_Y = np.arange(0, max_depth + Base['Interval'], -1 * Base['Interval'])
    Base_line_X = np.zeros(len(Base_line_Y))
    
    plt.plot(Base_line_X, Base_line_Y, 'k-')
    plt.plot(Select_line_X, Select_line_Y)
    plt.show()
    
    return Select_line_X, Select_line_Y









