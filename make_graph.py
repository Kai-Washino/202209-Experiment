#2022年8月の実験結果を可視化，解析するためのプログラム

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def main():
    path = "C:\\Users\\S2\\Documents\\実験\\2022年度9月 唾液分泌\\result"
    folder_list = glob.glob(path + '\\*')
    title_list = os.listdir(path)

    csv_list = []
    for name in folder_list:
        csv_list.append(glob.glob(name+'\\*.csv')[0])

    df_list = []
    for csv_name in csv_list:
        df_list.append(pd.read_csv(csv_name, header=None))


    turn_list=[]
    result_list=[]
    for df in df_list:
        turn_list.append(df.iloc[:1])
        df = df.drop(0)
        labels = ['before','after','no need']
        labels_dict = {num: label for num, label in enumerate(labels)}
        df = df.rename(columns = labels_dict)
        del df['no need']
        result_list.append(df['after']-df['before'])
    player_num = len(csv_list) 
    make_linegraph_1part(result_list, player_num, turn_list, title_list)
    make_linegraph_4part(result_list, player_num, turn_list, title_list)
    make_bargraph(result_list, player_num, turn_list, title_list) 
    make_average_linegraph(result_list, player_num, turn_list, title_list)

def make_linegraph_1part(result_list, player_num, turn_list, title_list):
    #result_listは1列の表示するグラフ，player_numはプレイヤーの人数，turu_listはにおいを噴射した時間，title_listはタイトル名
    plt.rcParams["font.size"] = 5
    fig_1part = plt.figure()
    subplot_area = []
    x = ['0', '5', '10', '15', '20', '25', '30', '35', '40']
    separete = player_num // 3 + 2
    # subplot_area.append(fig_1part.add_subplot(separete, separete, i+1))
    turn1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn3 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn4 = [0, 0, 0, 0, 0, 0, 0, 0, 0]


    for i in range(player_num):
        subplot_area.append(fig_1part.add_subplot(3, separete, i+1))

        y = []
        for j in range(9):
            y.append(result_list[i].iloc[j])
        
        odor_time = []
        for j in range(4):
            odor_time.append(turn_list[i].at[0,j])

        # print(odor_time)
        marker_name = ['','','','']
        for j in range(4):
            if(odor_time[j] == 60.0):
                marker_name[j] = "60"
            elif(odor_time[j] == 30.0):
                marker_name[j] = "30"
            elif(odor_time[j] == 10.0):
                marker_name[j] = "10"
            elif(odor_time[j] == 5.0):
                marker_name[j] = "5"
            else:
                marker_name[j] = "No"
            subplot_area[i].text(1 + j*2 ,y[2 + 2*j], marker_name[j], fontsize=5)
        # print(marker_name)

        subplot_area[i].plot(x, y, lw=1)
        subplot_area[i].set_title(title_list[i])

        # subplot_area[i].set_xlabel('time [minutes]')
        # subplot_area[i].set_ylabel('saliva volume [g]')
        # subplot_area[i].legend(loc = 'upper right')
        subplot_area[i].set_ylim(0, 0.65)
        plt.tick_params(labelsize=5)
        print(odor_time[0])
        if(odor_time[0] == 5.0):
            for i in range(9):
                turn1[i] += y[i]
        elif(odor_time[0] == 60.0):
            for i in range(9):
                turn2[i] += y[i]
        elif(odor_time[0] == 10.0):
            for i in range(9):
                turn3[i] += y[i]
        else:
            for i in range(9):
                turn4[i] += y[i]

    for i in range(9):
        turn1[i] = turn1[i]/player_num*2
        turn2[i] = turn2[i]/player_num*2
    
    marker = [5, 10, 30, 60]
    marker2 = [10, 60, 5, 30]

    subplot_area.append(fig_1part.add_subplot(3, separete, player_num + 1))
    for i in range(4):
        subplot_area[player_num].text(1 + i*2 ,turn1[2 + 2*i], marker[i], fontsize=5)
    subplot_area[player_num].plot(x, turn1, lw=1)
    subplot_area[player_num].set_title("turn1")
    subplot_area[player_num].set_ylim(0, 0.65)

    subplot_area.append(fig_1part.add_subplot(3, separete,  player_num + 2))
    for i in range(4):
        subplot_area[player_num+1].text(1 + i*2 ,turn2[2 + 2*i], marker[3 - i], fontsize=5)
    subplot_area[player_num+1].plot(x, turn2, lw=1)
    subplot_area[player_num+1].set_title("turn2")
    subplot_area[player_num+1].set_ylim(0, 0.65)

    subplot_area.append(fig_1part.add_subplot(3, separete,  player_num + 3))
    for i in range(4):
        subplot_area[player_num+2].text(1 + i*2 ,turn3[2 + 2*i], marker2[i], fontsize=5)
    subplot_area[player_num+2].plot(x, turn3, lw=1)
    subplot_area[player_num+2].set_title("turn3")
    subplot_area[player_num+2].set_ylim(0, 0.65)

    subplot_area.append(fig_1part.add_subplot(3, separete,  player_num + 4))
    for i in range(4):
        subplot_area[player_num+3].text(1 + i*2 ,turn4[2 + 2*i], marker2[3 - i], fontsize=5)
    subplot_area[player_num+3].plot(x, turn4, lw=1)
    subplot_area[player_num+3].set_title("turn4")
    subplot_area[player_num+3].set_ylim(0, 0.65)
    plt.tight_layout()
    plt.show()

def make_linegraph_4part(result_list, player_num, turn_list, title_list):
    #result_listは1列の表示するグラフ，player_numはプレイヤーの人数，turu_listはにおいを噴射した時間，title_listはタイトル名

    x = ['0', '5', '10']
    average_turn1 = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    average_turn2 = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    average_turn3 = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    average_turn4 = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    average_all = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    fig_3part = plt.figure()
    subplot_area = []
    separete = player_num // 3 + 3
    for i in range(player_num):
        subplot_area.append(fig_3part.add_subplot(3, separete, i+1))
        y1 = []
        y2 = []
        y3 = []
        y4 = []
        for j in range(3):
            y1.append(result_list[i].iloc[0+j])
            y2.append(result_list[i].iloc[2+j])
            y3.append(result_list[i].iloc[4+j])
            y4.append(result_list[i].iloc[6+j])
        
        odor_time = []
        for j in range(4):
            odor_time.append(turn_list[i].at[0,j])

        color = ['red', 'red', 'red', 'red']
        for j in range(4):
            if(odor_time[j] == 5.0):
                color[j] = "red"
            elif(odor_time[j] == 10.0):
                color[j] = "blue"
            elif(odor_time[j] == 30.0):
                color[j] = "green"
            else:
                color[j] = "pink"

        subplot_area[i].plot(x, y1, label = str(odor_time[0]), color = color[0], lw =1)
        subplot_area[i].plot(x, y2, label = str(odor_time[1]), color = color[1], lw =1)
        subplot_area[i].plot(x, y3, label = str(odor_time[2]), color = color[2], lw =1)
        subplot_area[i].plot(x, y4, label = str(odor_time[3]), color = color[3], lw =1)
        subplot_area[i].set_title(title_list[i])
        subplot_area[i].set_xlabel('time [minutes]')
        subplot_area[i].set_ylabel('saliva volume [g]')
        subplot_area[i].legend(loc = 'upper right')
        subplot_area[i].set_ylim(0, 0.65)
        if(odor_time[0] == 5.0):
            for i in range(3):
                average_all[0][i] =+ y1[i]
                average_all[1][i] =+ y2[i]
                average_all[2][i] =+ y3[i]
                average_all[3][i] =+ y4[i]
                average_turn1[0][i] =+ y1[i]
                average_turn1[1][i] =+ y2[i]
                average_turn1[2][i] =+ y3[i]
                average_turn1[3][i] =+ y4[i]
        elif(odor_time[0] == 60.0):
            for i in range(3):
                average_all[3][i] =+ y1[i]
                average_all[2][i] =+ y2[i]
                average_all[1][i] =+ y3[i]
                average_all[0][i] =+ y4[i]
                average_turn2[0][i] =+ y1[i]
                average_turn2[1][i] =+ y2[i]
                average_turn2[2][i] =+ y3[i]
                average_turn2[3][i] =+ y4[i]
        elif(odor_time[0] == 10.0):
            for i in range(3):
                average_all[1][i] =+ y1[i]
                average_all[3][i] =+ y2[i]
                average_all[0][i] =+ y3[i]
                average_all[2][i] =+ y4[i]
                average_turn3[0][i] =+ y1[i]
                average_turn3[1][i] =+ y2[i]
                average_turn3[2][i] =+ y3[i]
                average_turn3[3][i] =+ y4[i]
        else:
            for i in range(3):
                average_all[2][i] =+ y1[i]
                average_all[0][i] =+ y2[i]
                average_all[3][i] =+ y3[i]
                average_all[1][i] =+ y4[i]
                average_turn4[0][i] =+ y1[i]
                average_turn4[1][i] =+ y2[i]
                average_turn4[2][i] =+ y3[i]
                average_turn4[3][i] =+ y4[i]
    
    subplot_area.append(fig_3part.add_subplot(3, separete, player_num+1))
    subplot_area[player_num].plot(x, average_all[0], label = "5.0", color = "red", lw =1)
    subplot_area[player_num].plot(x, average_all[1], label = "10.0", color = "blue", lw =1)
    subplot_area[player_num].plot(x, average_all[2], label = "30.0", color = "green", lw =1)
    subplot_area[player_num].plot(x, average_all[3], label = "60.0", color = "pink", lw =1)
    subplot_area[player_num].set_title("all average")
    subplot_area[player_num].set_xlabel('time [minutes]')
    subplot_area[player_num].set_ylabel('saliva volume [g]')
    subplot_area[player_num].legend(loc = 'upper right')
    subplot_area[player_num].set_ylim(0, 0.65)

    subplot_area.append(fig_3part.add_subplot(3, separete, player_num+1+1))
    subplot_area[player_num+1].plot(x, average_turn1[0], label = "5.0", color = "red", lw =1)
    subplot_area[player_num+1].plot(x, average_turn1[1], label = "10.0", color = "blue", lw =1)
    subplot_area[player_num+1].plot(x, average_turn1[2], label = "30.0", color = "green", lw =1)
    subplot_area[player_num+1].plot(x, average_turn1[3], label = "60.0", color = "pink", lw =1)
    subplot_area[player_num+1].set_title("turn1 average")
    subplot_area[player_num+1].set_xlabel('time [minutes]')
    subplot_area[player_num+1].set_ylabel('saliva volume [g]')
    subplot_area[player_num+1].legend(loc = 'upper right')
    subplot_area[player_num+1].set_ylim(0, 0.65)

    subplot_area.append(fig_3part.add_subplot(3, separete, player_num+3+1))
    subplot_area[player_num+2].plot(x, average_turn2[3], label = "5.0", color = "red", lw =1)
    subplot_area[player_num+2].plot(x, average_turn2[2], label = "10.0", color = "blue", lw =1)
    subplot_area[player_num+2].plot(x, average_turn2[1], label = "30.0", color = "green", lw =1)
    subplot_area[player_num+2].plot(x, average_turn2[0], label = "60.0", color = "pink", lw =1)
    subplot_area[player_num+2].set_title("turn2 average")
    subplot_area[player_num+2].set_xlabel('time [minutes]')
    subplot_area[player_num+2].set_ylabel('saliva volume [g]')
    subplot_area[player_num+2].legend(loc = 'upper right')
    subplot_area[player_num+2].set_ylim(0, 0.65)

    subplot_area.append(fig_3part.add_subplot(3, separete, player_num+4+1))
    subplot_area[player_num+3].plot(x, average_turn3[2], label = "5.0", color = "red", lw =1)
    subplot_area[player_num+3].plot(x, average_turn3[0], label = "10.0", color = "blue", lw =1)
    subplot_area[player_num+3].plot(x, average_turn3[3], label = "30.0", color = "green", lw =1)
    subplot_area[player_num+3].plot(x, average_turn3[1], label = "60.0", color = "pink", lw =1)
    subplot_area[player_num+3].set_title("turn3 average")
    subplot_area[player_num+3].set_xlabel('time [minutes]')
    subplot_area[player_num+3].set_ylabel('saliva volume [g]')
    subplot_area[player_num+3].legend(loc = 'upper right')
    subplot_area[player_num+3].set_ylim(0, 0.65)

    subplot_area.append(fig_3part.add_subplot(3, separete, player_num+5+1))
    subplot_area[player_num+4].plot(x, average_turn4[1], label = "5.0", color = "red", lw =1)
    subplot_area[player_num+4].plot(x, average_turn4[3], label = "10.0", color = "blue", lw =1)
    subplot_area[player_num+4].plot(x, average_turn4[0], label = "30.0", color = "green", lw =1)
    subplot_area[player_num+4].plot(x, average_turn4[2], label = "60.0", color = "pink", lw =1)
    subplot_area[player_num+4].set_title("turn4 average")
    subplot_area[player_num+4].set_xlabel('time [minutes]')
    subplot_area[player_num+4].set_ylabel('saliva volume [g]')
    subplot_area[player_num+4].legend(loc = 'upper right')
    subplot_area[player_num+4].set_ylim(0, 0.65)

    plt.tight_layout()
    plt.show()

def make_bargraph(result_list, player_num, turn_list, title_list):

    # relative_list_before2nowは1つ前からにおい噴射の変化量，relative_list_before2afterは1つ前からにおい噴射後の変化量

    relative_list_before2now = []
    relative_list_before2after = []
    relative_list_now2after = []
    absolute_list = []
    

    for i in range(player_num):
        y = []
        relative_list_before2now.append([title_list[i], 0, 0, 0, 0])
        relative_list_before2after.append([title_list[i], 0, 0, 0, 0])
        relative_list_now2after.append([title_list[i], 0, 0, 0, 0])
        absolute_list.append([title_list[i], 0, 0, 0, 0])
        for j in range(9):
            y.append(result_list[i].iloc[j])

        odor_time = []
        for j in range(4):
            odor_time.append(turn_list[i].at[0,j])

         
        for j in range(4):
            if(odor_time[j] == 5.0):
                relative_list_before2now[i][1] = y[1 + 2*j] - y[2*j]
                relative_list_before2after[i][1] = y[2 + 2*j] - y[2*j]
                relative_list_now2after[i][1] = y[2 + 2*j] - y[1+2*j]
                absolute_list[i][1] = y[1 + 2*j]
            elif(odor_time[j] == 10.0):
                relative_list_before2now[i][2] = y[1 + 2*j] - y[2*j]
                relative_list_before2after[i][2] = y[2 + 2*j] - y[2*j]
                relative_list_now2after[i][2] = y[2 + 2*j] - y[1+2*j]
                absolute_list[i][2] = y[1 + 2*j]
            elif(odor_time[j] == 30.0):
                relative_list_before2now[i][3] = y[1 + 2*j] - y[2*j]
                relative_list_before2after[i][3] = y[2 + 2*j] - y[2*j]
                relative_list_now2after[i][3] = y[2 + 2*j] - y[1+2*j]
                absolute_list[i][3] = y[1 + 2*j]
            else:
                relative_list_before2now[i][4] = y[1 + 2*j] - y[2*j]
                relative_list_before2after[i][4] = y[2 + 2*j] - y[2*j]
                relative_list_now2after[i][4] = y[2 + 2*j] - y[1+2*j]
                absolute_list[i][4] = y[1 + 2*j]
    
    x = np.array([1, 2, 3, 4])
    labels = ['5秒', '10秒', '30秒', '60秒']
    
    margin = 0.2  
    totoal_width = 1 - margin
    average_list = [0, 0, 0, 0]

    # data_list = absolute_list #絶対値
    # data_list = relative_list_before2now #におい噴射直後と直前の変化量
    # data_list = relative_list_before2after #におい噴射直後の次と直前の変化量
    data_list = relative_list_now2after #におい噴射直後と直後の次の変化量
    # print(data_list)

    name_anonymous = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j" ,"k"]
    for i in range(player_num):
        temp_data = data_list[i]
        name = temp_data.pop(0)

        #検定用
        print(temp_data[0])
        print(',')
        print(temp_data[1])
        print(',')
        print(temp_data[2])
        # print(temp_data[0] + ',')
        # print(temp_data[1] + ',')
        # print(temp_data[2] + ',')

        pos = x - totoal_width *( 1- (2*i+1)/player_num)/2
        plt.bar(pos, temp_data, width = totoal_width/player_num, label = name)
        # plt.bar(pos, temp_data, width = totoal_width/player_num, label = name_anonymous[i])


        for j in range(4):
            average_list[j] = average_list[j] + temp_data[j]

    plt.rcParams["font.family"] = 'Meiryo'   # 使用するフォント
    plt.rcParams["font.size"] = 12                 # 文字の大きさ

    plt.xticks(x, labels, fontname='Meiryo', fontsize=20)
    # print(average_list)
    plt.yticks(fontname='Meiryo', fontsize=20)

    
    plt.plot(1, average_list[0]/player_num, '*',markersize=20)
    plt.plot(2, average_list[1]/player_num, '*',markersize=20)
    plt.plot(3, average_list[2]/player_num, '*',markersize=20)
    plt.plot(4, average_list[3]/player_num, '*',markersize=20)
    plt.legend(loc = 'upper right')
    plt.tight_layout()
    plt.show()
    
def make_average_linegraph(result_list, player_num, turn_list, title_list):
    #result_listは1列の表示するグラフ，player_numはプレイヤーの人数，turu_listはにおいを噴射した時間，title_listはタイトル名
    plt.rcParams["font.size"] = 5
    fig_1part = plt.figure()
    subplot_area = []
    x = ['0', '5', '10', '15', '20', '25', '30', '35', '40']
    separete = player_num // 3 + 1
    # print(separete)
    # subplot_area.append(fig_1part.add_subplot(separete, separete, i+1))
    y = [0]*9
    sum = [0]*9

    for i in range(9):
        for j in range(player_num):
            sum[i] = sum[i] + result_list[j].iloc[i]
        y[i] = sum[i]/player_num
       
    # print(average_list)

    plt.plot(x, y, lw=1)
    plt.legend(loc = 'upper right')
    plt.show()

if __name__ == '__main__':
    main()