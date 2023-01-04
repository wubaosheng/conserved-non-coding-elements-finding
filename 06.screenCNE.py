#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :06.screenLossCNE.py
@说明        :
@时间        :2022/12/08 11:02:51
@作者        :Wu Baosheng
@版本        :1.0
'''
import os,re,sys
import pandas as pd
def conservation(input_file,output_file,min_length=50,threshold=0.8):
    ac = 0
    seq = []
    seqence= {}
    len_flag = []
    with open(input_file,'r') as fs:
        for line in fs:
            line = line.strip()
            if len(seq) !=0 and len(line) == 0:
                seqence[ac]=seq
            if len(line) == 0:
                ac+=1
                seq=[]
                len_flag = []
            else:
                seq.append(line.split())
                len_flag.append(len(line.split()[-1]))
    fs.close()


    table = open(output_file,'w')
    final_list = list()
    for x in seqence:
        conserve = 0 
        conserve_ratio = 0
        seqence_length = len(seqence[x][0][-1])
        if seqence_length >= min_length:
            for counter in range(seqence_length):
                tmp = []
                for y in seqence[x]:
                    tmp.append(y[-1][counter].upper())
                if len(set(tmp))==1:
                    conserve+=1
                else:
                    pass
            #print(f'{seqence_length}--{conserve}')
            conserve_ratio = conserve/seqence_length
            final_list.append([x,conserve_ratio])
        else:
            pass

    score_new = sorted(final_list, key=lambda item:(float(item[1])),reverse=True)
    for i in score_new:
        if i[1] >=threshold:
            str_x = str(i[0])
            str_conserve_ratio = str(i[1])
            table.writelines(str(">") + str_x + "\t" + str(str_conserve_ratio) + '\n') 
            for t in seqence[i[0]]:
                table.writelines(str(' '.join(t[1:-1]).ljust(65," ") + t[-1]) +'\n')
            table.writelines(str('\n'))
        else:
            pass
    return None
if __name__ == '__main__':
    conservation(input_file='05.getLossCNE.py.reindeer.out',output_file=f'{sys.argv[0]}.out',threshold=0.75)

