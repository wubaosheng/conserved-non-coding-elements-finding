# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author : wubaosheng 2020-06-19
import os, re, sys
import pandas as pd
import numpy as np

root = os.getcwd()
target_list = ["tuna","yellowTuna","blueTuna"]
ac = ""
seq = ""
seq_dir = {}
wind=20   #####used for count conserved sites,this can be changed by different values,such as 10,30
score = []
span = 5
conservative = 0
counter = 0
flag = 0
score_dir = ()
final_list = []
flag_list = []
seq_len = 0
with open(root + "/01.transform.pl.out", "r") as fs:
    for line in fs:
        if line.startswith(">") and len(line.strip().split()[-1]) > (wind + 2* span):
            line_list = line.strip().split()
            ac = line_list[0]
            seq = line_list[-1].upper()
            seq_len = len(seq)
            seq_dir[ac] = seq
            seq = ""
            ac = ""
        if line.startswith("<") and seq_dir != {}:
            tmp_list = []
            adjusted_list = []
            counter += 1
            print(counter)
            ingroup = []
            outgroup = []
            for species_id in seq_dir.keys():
                species = species_id.lstrip(">").split(".")[0]
                if species in target_list:
                    ingroup.append(species_id)
                else:
                    outgroup.append(species_id)
            length = max([len(seq_dir[x]) for x in seq_dir.keys()])
            in_seq = [seq_dir[x] for x in ingroup]
            out_seq = [seq_dir[x] for x in outgroup]
            for i in np.arange(length):
                ingroup_set = set([x[i] for x in in_seq])
                outgroup_set = set([x[i] for x in out_seq])
                if len(ingroup_set) == len(outgroup_set) ==1:
                    if ingroup_set == outgroup_set:
                        tmp_list.append("0")
                    else:
                        tmp_list.append("1")
                    #score+= 5 ** flag
                elif len(outgroup_set) ==1 and len(ingroup_set) !=1:
                    tmp_list.append("2")
                elif len(ingroup_set) ==1 and len(outgroup_set) !=1:
                    tmp_list.append("3")
                else:
                    tmp_list.append("4")
            (count_0,count_1,coun_2)=(0,0,0)
            if (length-2*span) >wind:
                for j in np.arange(span,length-wind-span+1):
                    count_0 = tmp_list[j-span: j].count("0") + tmp_list[j+wind: j+wind+span].count("0")
                    count_1 = tmp_list[j: j+wind].count("1")
                    count_2 = tmp_list[j: j+wind].count("2")
                    info_count = [count_1,count_0]
                    adjusted_list.append(info_count)
                score = sorted(adjusted_list, key=lambda x:(x[0],x[1]),reverse=True)[0]
                #conservative = "%.4f" %(count_1/length)
                    
            else:
                pass
            score_dir = (seq_dir,score[0],score[1],tmp_list)
            final_list.append(score_dir)
            seq_dir = {}
            print("the final score:%s" %(score))
            score = []
        else:
            pass
print("Please wait patiently while writing results........................................................")
score_new = sorted(final_list, key=lambda item:(int(item[1]),int(item[2])),reverse=True)
fs.close()
table = open(root + "/%s.out" %(sys.argv[0]),"w")
for i in score_new:
    table.writelines(str("the final score:{},{}".format(str(i[1]),str(i[2])).ljust(56," ") + str("".join(i[-1])) +"\n"))
    for j in i[0]:
        table.writelines(str(j.ljust(50, " ")) + "\t" + str(i[0][j]) + "\n")
    table.writelines("\n")
table.close()
