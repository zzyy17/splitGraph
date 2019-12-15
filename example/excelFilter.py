#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author: zhou_me
@file: excelFilter.py.py
@time: 2019/12/14
@contact: zhou_me@worksap.co.jp
@site:
@software: PyCharm
"""
import os
import pandas as pd
import sys
import xlwt

input_excel_dir = 'G:\qian\code\data'
splitValue = 5  # define the distance value


def init():
    """"
    load the input xls files, return the list of file name
    """
    print('[log] Current input directory: ' + input_excel_dir)
    result_list_files = []
    files = os.listdir(input_excel_dir)
    for i in files:
        if os.path.splitext(i)[1] == '.xls':
            result_list_files.append(i)
            # print(i)

    return result_list_files


def isValidPoint(pData, tData, result):
    if pData.shape[0] > tData.shape[0]:
        for r1 in range(0, len(pData)):
            px = pData.iloc[r1]['x']
            py = pData.iloc[r1]['y']
            # print("[1]: ", px, py)
            for r2 in range(0, len(tData)):
                tx = tData.iloc[r2]['x']
                ty = tData.iloc[r2]['y']
                if (px - tx) * (px - tx) + (py - ty) * (py - ty) <= splitValue * splitValue:
                    result += 1
                    # print('[2]:', tx, ty)
                    break

    else:
        for r1 in range(0, len(tData)):
            tx = tData.iloc[r1]['x']
            ty = tData.iloc[r1]['y']
            for r2 in range(0, len(tData)):
                px = pData.iloc[r2]['x']
                py = pData.iloc[r2]['y']
                if (px - tx) * (px - tx) + (py - ty) * (py - ty) <= splitValue * splitValue:
                    result += 1
                    break

    return result


def process():
    files = init()
    numberOfPro = set()
    result_df = pd.DataFrame(columns=['Files', 'Numbers'])

    for file in files:
        # print(file[1:])
        numberOfPro.add(file[1:])

    for p in numberOfPro:
        try:
            tPro = pd.read_excel(input_excel_dir + '\\' + 't' + p)
            pPro = pd.read_excel(input_excel_dir + '\p' + p)
        except IOError:
            print('Can not find ', input_excel_dir + '/t' + p + '/', input_excel_dir + '/p' + p)

        pData = pPro[1:]
        tData = tPro[1:]
        pData = pData.rename(columns={'Detailed': 'x', 'Unnamed: 1': 'y'})
        tData = tData.rename(columns={'Detailed': 'x', 'Unnamed: 1': 'y'})
        result = isValidPoint(pData, tData, 0)
        newRow = {'Files': p.split('.')[0], 'Numbers': result}
        result_df.loc[len(result_df)] = newRow
        #print(result_df)
        output_dir = input_excel_dir + '/result'
        is_exists = os.path.exists(output_dir)
        if not is_exists:
            try:
                os.makedirs(output_dir)
            except OSError as exception:
                print(exception)
                sys.exit(0)
        result_df.to_excel(output_dir + '/result.xls', index=False)


if __name__ == '__main__':
    process()
