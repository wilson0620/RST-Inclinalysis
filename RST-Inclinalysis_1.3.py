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


def plot(Base, Select, Adjust = True): #Base only one file, Select need to be list-like multiple or single file.
    
    if Adjust == True:
        try:
            Adj_file = pd.read_csv('Adjust.csv')
            A_Adjust = np.array(Adj_file['A_Adjust'])
            B_Adjust = np.array(Adj_file['B_Adjust'])
        except FileNotFoundError:
            print('Adjust file not exist.')
            return
        except:
            print('Unexpected error when reading Adjust file. (Wrong formet?)')
            return
        
    max_depth = Base['Depth'][0]
    
    for data in Select:
        select_depth = data['Depth'][0]
        
        if select_depth < max_depth:
            print("Error in %s : Base file cannot shorter then Select file." %data['Time_String'])
            return
        
        data['Cumulate_line_A'] = compare(Base['Data_A'], data['Data_A'])
        data['Cumulate_line_B'] = compare(Base['Data_B'], data['Data_B'])
        data['Cumulate_line_depth'] = [-0.5 * i for i in range(1, len(data['Cumulate_line_A'])+1)]
        
        if Adjust == True:
            try:
                data['Cumulate_line_A'] += A_Adjust
                data['Cumulate_line_B'] += B_Adjust
            except NameError:
                print('Error in %s : Adjust file not exist.'%data['Time_String'])
            except:
                print('Error in %s : Unexpected error.'%data['Time_String'])



    Base_line_Y = np.arange(0, max_depth - Base['Interval'], -1 * Base['Interval'])
    Base_line_X = np.zeros(len(Base_line_Y)) 
    style = ['r-', 'b--', 'g-.', 'y:', 'c-', 'm--', 'r-.', 'b:', 'g-', 'y--', 'c-.', 'm:']
    plt.figure(figsize=(11,15.5))
    time_sequence = []

    
    plt.subplot(1, 2, 1)
    plt.title('A Direction', fontsize=40)
    plt.xlabel('Displacement (mm)', fontsize=20)
    plt.ylabel('Depth (m)', fontsize=20)
    
    max_displacement = []
    for data in Select:
        max_displacement.append(max(map(abs, data['Cumulate_line_A'])))
    
    max_displacement = max(max_displacement)
    if max_displacement <= 60:
        plt.xlim(-60, 60)
    elif max_displacement <= 100:
        plt.xlim(-100, 100)
    else:
        pass
    
    for data in range(len(Select)):
        plt.plot(Select[data]['Cumulate_line_A'], Select[data]['Cumulate_line_depth'], style[data], label = Select[data]['Time_String'])
        
    plt.plot(Base_line_X, Base_line_Y, 'k-', label = Base['Time_String'])
    plt.legend(loc='lower left')
    
    
    
    plt.subplot(1, 2, 2)
    plt.title('B Direction', fontsize=40)
    plt.xlabel('Displacement (mm)', fontsize=20)
    plt.ylabel('Depth (m)', fontsize=20)
    
    max_displacement = []
    for data in Select:
        max_displacement.append(max(map(abs, data['Cumulate_line_B'])))
    
    max_displacement = max(max_displacement)
    if max_displacement <= 60:
        plt.xlim(-60, 60)
    elif max_displacement <= 100:
        plt.xlim(-100, 100)
    else:
        pass
    
    for data in range(len(Select)):
        plt.plot(Select[data]['Cumulate_line_B'], Select[data]['Cumulate_line_depth'], style[data], label = Select[data]['Time_String'])
    plt.plot(Base_line_X, Base_line_Y, 'k-', label = Base['Time_String'])
    plt.legend(loc='lower left')
    plt.show()
    
    return max_displacement

B = reading('B1(1).csv')
S = reading(file_path)
S2 = reading('B1(64).csv')





