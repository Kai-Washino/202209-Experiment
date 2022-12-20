#2022年8月の実験結果を可視化，解析するためのプログラム

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from matplotlib import patches

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
    # make_linegraph_4part(result_list, player_num, turn_list, title_list)
    # make_bargraph(result_list, player_num, turn_list, title_list) 
    # make_average_linegraph(result_list, player_num, turn_list, title_list)

def make_linegraph_1part(result_list, player_num, turn_list, title_list):
    #result_listは1列の表示するグラフ，player_numはプレイヤーの人数，turu_listはにおいを噴射した時間，title_listはタイトル名
    plt.rcParams["font.size"] = 5
    fig_1part = plt.figure()
    subplot_area = []
    all_data = []
    x = ['0', '5', '10', '15', '20', '25', '30', '35', '40']
    separete = player_num // 3 + 2
    # subplot_area.append(fig_1part.add_subplot(separete, separete, i+1))
    turn1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn3 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn4 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    all_average = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(player_num):
        subplot_area.append(fig_1part.add_subplot(3, separete, i+1))
        y = []
        for j in range(9):
            y.append(result_list[i].iloc[j])
            # print(result_list[i].iloc[j])
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
        # subplot_area[i].legend(frameon=False, loc = 'upper right')
        subplot_area[i].set_ylim(0, 0.65)
        plt.tick_params(labelsize=5)
        if(odor_time[0] == 5.0):
            # print("5")
            for i in range(9):
                turn1[i] += y[i]
                all_average[i] += y[i]
        elif(odor_time[0] == 60.0):
            # print("60")
            for i in range(9):
                turn2[i] += y[i]
                all_average[i] += y[i]
        elif(odor_time[0] == 10.0):
            # print("10")
            for i in range(9):
                turn3[i] += y[i]
                all_average[i] += y[i]
        else:
            # print("30")
            for i in range(9):
                turn4[i] += y[i]
                all_average[i] += y[i]

    for i in range(9):
        turn1[i] = turn1[i]/player_num*3
        turn2[i] = turn2[i]/player_num*3
        turn3[i] = turn3[i]/player_num*3
        turn4[i] = turn4[i]/player_num*3
        all_average[i] = all_average[i]/player_num
    
    
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

    plt.rcParams["font.size"] = 15
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Yu Gothic'
    plt.xlabel('時間 [分]', fontname='Yu Gothic', fontsize=17)
    plt.ylabel('唾液分泌量 [g]', fontname='Yu Gothic', fontsize=17)    

    ######### 群ごとにわける#############################
    # plt.plot(x, turn1, lw=2, label = "5-10-30-60群")
    # plt.plot(x, turn2, lw=2, label = "60-30-10-5群")
    # plt.plot(x, turn3, lw=2, label = "10-60-5-30群")
    # plt.plot(x, turn4, lw=2, label = "30-5-60-10群")
    # plt.plot(x, all_average, lw=2, label = "全ての群の平均")plt.legend(loc = 'upper right', frameon=False)
    # plt.ylim(0, 0.75)
    # addP(plt, 3.5, 0.40, 3.5, 0.06, "*")
    # addP(plt, 4.5, 0.36, 2.5, 0.02, "*")
    # plt.text(0, 0.70, "* : p < 0.05", fontname='Yu Gothic', fontsize=17)

    ######### 群ごとにわけない###########################
    plt.plot(x, all_average, lw=2)
    plt.ylim(0, 0.55)
    addP(plt, 3.5, 0.40, 3.5, 0.06, "*")
    addP(plt, 4.5, 0.36, 2.5, 0.02, "*")
    plt.text(0, 0.50, "* : p < 0.05", fontname='Yu Gothic', fontsize=17)
    ####################################################
    
    
    plt.tight_layout()
    plt.show()

def make_linegraph_4part(result_list, player_num, turn_list, title_list):
    #result_listは1列の表示するグラフ，player_numはプレイヤーの人数，turu_listはにおいを噴射した時間，title_listはタイトル名

    plt.rcParams["font.size"] = 5
    x = ['0', '5', '10']
    average_turn1 = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    average_turn2 = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    average_turn3 = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    average_turn4 = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    average_all = [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]
    sec5_list = []
    sec10_list = []
    sec30_list = []
    sec60_list = []
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
        subplot_area[i].legend(frameon=False, loc = 'upper right')
        subplot_area[i].set_ylim(0, 0.65)
        if(odor_time[0] == 5.0):
            sec5_list.append(y1)
            sec10_list.append(y2)
            sec30_list.append(y3)
            sec60_list.append(y4)
            for i in range(3):
                average_all[0][i] += y1[i]
                average_all[1][i] += y2[i]
                average_all[2][i] += y3[i]
                average_all[3][i] += y4[i]
                average_turn1[0][i] += y1[i]
                average_turn1[1][i] += y2[i]
                average_turn1[2][i] += y3[i]
                average_turn1[3][i] += y4[i]
        elif(odor_time[0] == 60.0):
            sec5_list.append(y4)
            sec10_list.append(y3)
            sec30_list.append(y2)
            sec60_list.append(y1)
            for i in range(3):
                average_all[3][i] += y1[i]
                average_all[2][i] += y2[i]
                average_all[1][i] += y3[i]
                average_all[0][i] += y4[i]
                average_turn2[0][i] += y1[i]
                average_turn2[1][i] += y2[i]
                average_turn2[2][i] += y3[i]
                average_turn2[3][i] += y4[i]
            
        elif(odor_time[0] == 10.0):
            sec5_list.append(y3)
            sec10_list.append(y1)
            sec30_list.append(y4)
            sec60_list.append(y2)
            for i in range(3):
                average_all[1][i] += y1[i]
                average_all[3][i] += y2[i]
                average_all[0][i] += y3[i]
                average_all[2][i] += y4[i]
                average_turn3[0][i] += y1[i]
                average_turn3[1][i] += y2[i]
                average_turn3[2][i] += y3[i]
                average_turn3[3][i] += y4[i]
        else:
            sec5_list.append(y2)
            sec10_list.append(y4)
            sec30_list.append(y1)
            sec60_list.append(y3)
            for i in range(3):
                average_all[2][i] += y1[i]
                average_all[0][i] += y2[i]
                average_all[3][i] += y3[i]
                average_all[1][i] += y4[i]
                average_turn4[0][i] += y1[i]
                average_turn4[1][i] += y2[i]
                average_turn4[2][i] += y3[i]
                average_turn4[3][i] += y4[i]
    for i in range(4):
        for j in range(3):
            average_all[i][j] = average_all[i][j]/player_num
            average_turn1[i][j] = average_turn1[i][j]/3
            average_turn2[i][j] = average_turn2[i][j]/3
            average_turn3[i][j] = average_turn3[i][j]/3
            average_turn4[i][j] = average_turn4[i][j]/3
    
    subplot_area.append(fig_3part.add_subplot(3, separete, player_num+1))
    subplot_area[player_num].plot(x, average_all[0], label = "5.0", color = "red", lw =1)
    subplot_area[player_num].plot(x, average_all[1], label = "10.0", color = "blue", lw =1)
    subplot_area[player_num].plot(x, average_all[2], label = "30.0", color = "green", lw =1)
    subplot_area[player_num].plot(x, average_all[3], label = "60.0", color = "pink", lw =1)
    subplot_area[player_num].set_title("all_average average")
    subplot_area[player_num].set_xlabel('time [minutes]')
    subplot_area[player_num].set_ylabel('saliva volume [g]')
    subplot_area[player_num].legend(loc = 'upper right', frameon=False)
    subplot_area[player_num].set_ylim(0, 0.65)

    subplot_area.append(fig_3part.add_subplot(3, separete, player_num+1+1))
    subplot_area[player_num+1].plot(x, average_turn1[0], label = "5.0", color = "red", lw =1)
    subplot_area[player_num+1].plot(x, average_turn1[1], label = "10.0", color = "blue", lw =1)
    subplot_area[player_num+1].plot(x, average_turn1[2], label = "30.0", color = "green", lw =1)
    subplot_area[player_num+1].plot(x, average_turn1[3], label = "60.0", color = "pink", lw =1)
    subplot_area[player_num+1].set_title("turn1 average")
    subplot_area[player_num+1].set_xlabel('time [minutes]')
    subplot_area[player_num+1].set_ylabel('saliva volume [g]')
    subplot_area[player_num+1].legend(loc = 'upper right', frameon=False)
    subplot_area[player_num+1].set_ylim(0, 0.65)

    subplot_area.append(fig_3part.add_subplot(3, separete, player_num+3+1))
    subplot_area[player_num+2].plot(x, average_turn2[3], label = "5.0", color = "red", lw =1)
    subplot_area[player_num+2].plot(x, average_turn2[2], label = "10.0", color = "blue", lw =1)
    subplot_area[player_num+2].plot(x, average_turn2[1], label = "30.0", color = "green", lw =1)
    subplot_area[player_num+2].plot(x, average_turn2[0], label = "60.0", color = "pink", lw =1)
    subplot_area[player_num+2].set_title("turn2 average")
    subplot_area[player_num+2].set_xlabel('time [minutes]')
    subplot_area[player_num+2].set_ylabel('saliva volume [g]')
    subplot_area[player_num+2].legend(loc = 'upper right', frameon=False)
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
    subplot_area[player_num+4].legend(frameon=False, loc = 'upper right')
    subplot_area[player_num+4].set_ylim(0, 0.65)

    plt.tight_layout()
    plt.show()

    plt.rcParams["font.size"] = 15
    labels = ['5秒', '10秒', '30秒', '60秒']
    margin = 0.2  #0 <margin< 1
    totoal_width = 1 - margin

    #標準誤差の計算
    error_5_before_list = []
    error_5_now_list = []
    error_5_after_list = []
    error_10_before_list = []
    error_10_now_list = []
    error_10_after_list = []
    error_30_before_list = []
    error_30_now_list = []
    error_30_after_list = []
    error_60_before_list = []
    error_60_now_list = []
    error_60_after_list = []
    for i in range(player_num):
        error_5_before_list.append(sec5_list[i][0])
        error_5_now_list.append(sec5_list[i][1])
        error_5_after_list.append(sec5_list[i][2])
        error_10_before_list.append(sec10_list[i][0])
        error_10_now_list.append(sec10_list[i][1])
        error_10_after_list.append(sec10_list[i][2])
        error_30_before_list.append(sec30_list[i][0])
        error_30_now_list.append(sec30_list[i][1])
        error_30_after_list.append(sec30_list[i][2])
        error_60_before_list.append(sec60_list[i][0])
        error_60_now_list.append(sec60_list[i][1])
        error_60_after_list.append(sec60_list[i][2])
    sem5_before = pd.Series(error_5_before_list).sem()
    sem5_now = pd.Series(error_5_now_list).sem()
    sem5_after = pd.Series(error_5_after_list).sem()
    sem10_before = pd.Series(error_10_before_list).sem()
    sem10_now = pd.Series(error_10_now_list).sem()
    sem10_after = pd.Series(error_10_after_list).sem()
    sem30_before = pd.Series(error_30_before_list).sem()
    sem30_now = pd.Series(error_30_now_list).sem()
    sem30_after = pd.Series(error_30_after_list).sem()
    sem60_before = pd.Series(error_60_before_list).sem()
    sem60_now = pd.Series(error_60_now_list).sem()
    sem60_after = pd.Series(error_60_after_list).sem()

    #前も後もいる場合
    data = [0, 0, 0]
    x = np.array([1, 2, 3, 4])
    for i in range(3): 
        data[i] = average_all[0][i], average_all[1][i], average_all[2][i], average_all[3][i]
    err = [sem5_before, sem10_before, sem30_before, sem60_before], [sem5_now, sem10_now, sem30_now, sem60_now], [sem5_after, sem10_after, sem30_after, sem60_after]
    label = ["におい噴射の5分前", "におい噴射中", "におい噴射の5分後"]

    #前だけいる場合
    data = [0, 0]
    x = np.array([1, 2, 3, 4])
    for i in range(2): 
        data[i] = average_all[0][i], average_all[1][i], average_all[2][i], average_all[3][i]
    err = [sem5_before, sem10_before, sem30_before, sem60_before], [sem5_now, sem10_now, sem30_now, sem60_now]
    label = ["におい噴射の5分前", "におい噴射中"]
    
    for i, h in enumerate(data):
        pos = x - totoal_width *( 1- (2*i+1)/len(data))/2
        plt.bar(pos, h, label = label[i], width = totoal_width/len(data), yerr=err[i], capsize=10)

    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Yu Gothic'
    plt.xticks(x, labels, fontname='Yu Gothic', fontsize=17)
    plt.yticks(fontname='Yu Gothic', fontsize=17)
    plt.xlabel('においの噴射時間', fontname='Yu Gothic', fontsize=17)
    plt.ylabel('唾液分泌量 [g]', fontname='Yu Gothic', fontsize=17)
    plt.legend(frameon=False, loc = 'upper right', prop={"family":"Yu Gothic"})
    #検定結果表示
    addP(plt, 2, 0.35, 0.2, 0.02, "**")
    addP(plt, 4, 0.35, 0.2, 0.02, "*")
    plt.text(0.5, 0.445, "* : p < 0.05   ** : p < 0.01", fontname='Yu Gothic', fontsize=17)

    plt.ylim(bottom=0, top=0.5)
    plt.tight_layout()
    plt.show()  

    #UWW2022用のグラフ作成
    plt.rcParams["font.size"] = 25
    data_UWW = [[0, 0], [0, 0], [0, 0], [0, 0]]
    err_UWW = [sem5_before, sem5_now,], [sem10_before, sem10_now], [sem30_before, sem30_now],[sem60_before, sem60_now]
    for i in range(4):
        for j in range(2):
            data_UWW[i][j] = average_all[i][j]
    print(data_UWW)
    subplot_cnt = [141, 142, 143, 144]
    title_name = ["(a) 5秒間","(b) 10秒間", "(c) 30秒間", "(d) 60秒間"]
    label = ["噴射5分前", "噴射中"]
    for i in range(4):
        plt.subplot(subplot_cnt[i])
        plt.ylim(0,0.5)
        plt.bar(label, data_UWW[i], yerr=err_UWW[i], capsize=10, color = ["darkturquoise", "tomato"])
        if(i == 0):
            plt.ylabel('唾液分泌量 [g]', fontname='Yu Gothic', fontsize=25)
            plt.tick_params(labelbottom=False)
        elif(i == 1):
            addP(plt, 0.5, 0.35, 0.5, 0.02, "**")
            plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
        elif(i == 2):
            plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
        else:
            addP(plt, 0.5, 0.35, 0.5, 0.02, "*")
            plt.legend(frameon=False, loc = 'upper right', prop={"family":"Yu Gothic"})
            plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
        plt.title(title_name[i], y=-0.15, fontsize=25)
        
    plt.text(-8, 0.52, "* : p < 0.05   ** : p < 0.01", fontname='Yu Gothic', fontsize=25)
    box1 = {
        'facecolor' : 'darkturquoise',
        'edgecolor' : 'black',
        'boxstyle' : 'square, pad=0.8',
        'linewidth' : 0
    }
    box2 = {
        'facecolor' : 'tomato',
        'edgecolor' : 'none',
        'boxstyle' : 'square, pad=1',
        'linewidth' : 0
    }
    x = -1
    y = 0.6
    plt.text(x=x, y=y, s ='          ', bbox=box1, fontsize='8')
    plt.text(x=x+0.61, y=y-0.015, s= label[0], fontname='Yu Gothic', fontsize=25)
    plt.text(x=x, y=y-0.06, s ='          ', bbox=box2, fontsize='8')
    plt.text(x=x+0.61, y=y-0.075, s= label[1], fontname='Yu Gothic', fontsize=25)

    plt.subplots_adjust(left=0.15, right=0.95, bottom=0.1, top=0.8)
    #     bbox=box2)
    plt.show()
    plt.rcParams["font.size"] = 17
 
    #検定用
    output = sec60_list
    # for i in range(player_num):
        # print(output[i][0])
        # print(output[i][1])
        # print(output[i][2])


def make_bargraph(result_list, player_num, turn_list, title_list):
    # relative_list_before2nowは1つ前からにおい噴射の変化量，relative_list_before2afterは1つ前からにおい噴射後の変化量
    plt.rcParams["font.size"] = 5
    relative_list_before2now = [[0 for i in range(5)] for j in range(player_num)]
    relative_list_before2after= [[0 for i in range(5)] for j in range(player_num)]
    relative_list_now2after= [[0 for i in range(5)] for j in range(player_num)]
    absolute_list= [[0 for i in range(5)] for j in range(player_num)]
    error5 = []
    error10 = []
    error30 = []
    error60 = []
    
    turn1 = 0
    turn2 = 0
    turn3 = 0
    turn4 = 0
    for i in range(player_num):
        y = []
        for j in range(9):
            y.append(result_list[i].iloc[j])
        print(turn_list[i].at[0,0])
        if(turn_list[i].at[0,0] == 5.0):
            graph_list = 0 + turn1
            turn1 += 1
        elif(turn_list[i].at[0,0] == 30.0):
            graph_list = 3 + turn2
            turn2 += 1
        elif(turn_list[i].at[0,0] == 60.0):
            graph_list = 6 + turn3
            turn3 += 1
        else:
            graph_list = 9 + turn4
            turn4 += 1
        print(graph_list)

        odor_time = []
        for j in range(4):
            odor_time.append(turn_list[i].at[0,j])

        relative_list_before2now[graph_list][0] = title_list[i]
        relative_list_before2after[graph_list][0] = title_list[i]
        relative_list_now2after[graph_list][0] = title_list[i]
        absolute_list[graph_list][0] = title_list[i]
        for j in range(4):
            if(odor_time[j] == 5.0):
                relative_list_before2now[graph_list][1] = y[1 + 2*j] - y[2*j]
                relative_list_before2after[graph_list][1] = y[2 + 2*j] - y[2*j]
                relative_list_now2after[graph_list][1] = y[2 + 2*j] - y[1+2*j]
                absolute_list[graph_list][1] = y[1 + 2*j]
            elif(odor_time[j] == 10.0):
                relative_list_before2now[graph_list][2] = y[1 + 2*j] - y[2*j]
                relative_list_before2after[graph_list][2] = y[2 + 2*j] - y[2*j]
                relative_list_now2after[graph_list][2] = y[2 + 2*j] - y[1+2*j]
                absolute_list[graph_list][2] = y[1 + 2*j]
            elif(odor_time[j] == 30.0):
                relative_list_before2now[graph_list][3] = y[1 + 2*j] - y[2*j]
                relative_list_before2after[graph_list][3] = y[2 + 2*j] - y[2*j]
                relative_list_now2after[graph_list][3] = y[2 + 2*j] - y[1+2*j]
                absolute_list[graph_list][3] = y[1 + 2*j]
            else:
                relative_list_before2now[graph_list][4] = y[1 + 2*j] - y[2*j]
                relative_list_before2after[graph_list][4] = y[2 + 2*j] - y[2*j]
                relative_list_now2after[graph_list][4] = y[2 + 2*j] - y[1+2*j]
                absolute_list[graph_list][4] = y[1 + 2*j]
    
    x = np.array([1, 2, 3, 4])
    labels = ['5秒', '10秒', '30秒', '60秒']
    
    margin = 0.2  
    totoal_width = 1 - margin
    average_list = [0, 0, 0, 0]

    # data_list = absolute_list #絶対値
    data_list = relative_list_before2now #におい噴射中と直前の変化量
    # data_list = relative_list_before2after #におい噴射中の次と直前の変化量
    # data_list = relative_list_now2after #におい噴射中と直後の次の変化量

    name_anonymous = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J" ,"K", "L"]
    for i in range(player_num):
        temp_data = data_list[i]
        name = temp_data.pop(0)

        #検定用
        # print(temp_data[0])
        # print(temp_data[1])
        # print(temp_data[2])
        # print(temp_data[3])
        error5.append(temp_data[0])
        error10.append(temp_data[1])
        error30.append(temp_data[2])
        error60.append(temp_data[3])

        pos = x - totoal_width *( 1- (2*i+1)/player_num)/2
        # plt.bar(pos, temp_data, width = totoal_width/player_num, label = name)
        plt.bar(pos, temp_data, width = totoal_width/player_num, label = name_anonymous[i])


        for j in range(4):
            average_list[j] = average_list[j] + temp_data[j]

    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams["font.family"] = 'Yu Gothic'   # 使用するフォント
    plt.rcParams["font.size"] = 15                 # 文字の大きさ

    plt.xticks(x, labels, fontname='Yu Gothic', fontsize=17)
    # print(average_list)
    plt.yticks(fontname='Yu Gothic', fontsize=17)
    plt.xlabel('においの噴射時間', fontname='Yu Gothic', fontsize=17)
    plt.ylabel('唾液分泌量の変化量 [g]', fontname='Yu Gothic', fontsize=17)
    plt.text(1, average_list[0]/player_num, '-',horizontalalignment="center", fontname='Yu Gothic', fontsize=30)
    plt.text(2, average_list[1]/player_num, '-',horizontalalignment="center", fontname='Yu Gothic', fontsize=30)
    plt.text(3, average_list[2]/player_num, '-',horizontalalignment="center", fontname='Yu Gothic', fontsize=30)
    plt.text(4, average_list[3]/player_num, '-',horizontalalignment="center", fontname='Yu Gothic', fontsize=30)
    plt.text(0.5, 0.45, '- : 平均値', fontname='Yu Gothic', fontsize=17)
    print(average_list[2]/player_num)
    plt.legend(frameon=False, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, prop={"family":"Yu Gothic"})
    plt.ylim(bottom=-0.18, top=0.5)
    # plt.legend(frameon=False, loc = 'upper right')
    plt.tight_layout()
    plt.show()

    plt.rcParams["font.size"] = 15
    labels = ['5秒', '10秒', '30秒', '60秒']
    margin = 0.2  #0 <margin< 1
    totoal_width = 1 - margin

    #標準誤差の計算
    sem5 = pd.Series(error5).sem()
    sem10 = pd.Series(error10).sem()
    sem30 = pd.Series(error30).sem()
    sem60 = pd.Series(error60).sem()
    err = sem5, sem10, sem30, sem60
    # print(err)
    x = np.array([1, 2, 3, 4])

    for i in range(4):
        plt.bar(i+1, average_list[i]/player_num, width = totoal_width, yerr=err[i], capsize=10)
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Yu Gothic'
    plt.xticks(x, labels, fontname='Yu Gothic', fontsize=17)
    plt.yticks(fontname='Yu Gothic', fontsize=17)
    plt.xlabel('においの噴射時間', fontname='Yu Gothic', fontsize=17)
    plt.ylabel('唾液分泌量の変化量 [g]', fontname='Yu Gothic', fontsize=17)
    plt.ylim(bottom=-0.05, top=0.2)
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
    plt.legend(frameon=False, loc = 'upper right')
    plt.show()


def addP(plt, p_xplace, p_yplace, p_width, p_height, p_text):
    plt.plot([p_xplace-p_width, p_xplace + p_width],[p_yplace, p_yplace], color="black")
    plt.plot([p_xplace-p_width, p_xplace-p_width],[p_yplace, p_yplace - p_height], color="black")
    plt.plot([p_xplace + p_width, p_xplace + p_width],[p_yplace, p_yplace - p_height], color="black")
    plt.text(p_xplace, p_yplace, p_text, horizontalalignment="center")
    

if __name__ == '__main__':
    main()