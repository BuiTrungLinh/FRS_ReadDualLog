import webbrowser

import gui
from report import *
from pathlib import Path
from os.path import dirname, abspath
import os

outputPath = ''

if __name__ == '__main__':
    gui.start_up()


def process(pathlogfile, pathexpfile):

    try:
        fileLog = open(pathlogfile, 'r')
        fileExpected = open(pathexpfile, 'r')
    except:
        gui.show_msg('Error Message', 'There is a problem with the path, please check it again!')
        return
    Lines = [i.strip() for i in fileLog.readlines()]
    verify(Lines, fileExpected)


def verify(lines, fileExpected):
    countLine = 0
    countData_Passed = 0
    countData_Misread = 0
    refresh = 0
    dataList = []
    dictData = {
        'symID': '',
        'symType': 'Unknown',
        'fullData': '',
        'count': 1,
        'isMisread': False
    }
    # Check current interface in log file
    interface = [s for s in lines if '{Interface:' in s][0].split(':')[-1].strip()[1:-2]

    # Process for expected file
    # Read file
    listExpectedData = []
    for x in fileExpected.readlines():
        listExpectedData.append(x.strip())

    for line in lines:
        countLine += 1
        # Outgoing Barcode Symbolog: 131 -- 1
        # Outgoing Barcode Symbology: SCAN_SDT_RSS14 -- 2
        # Get PIDXScan_ScanData: R40192612309845674
        # print("Line{}: {}".format(count, line.strip()))
        if 'Outgoing Barcode Symbology' in line.strip():
            # print("Line{}: {}".format(countLine, line.strip()))
            refresh += 1
            add_child_data(refresh, dictData, line.strip())
            # if Outgoing Barcode Symbology = 0, meaning don't know syms
            if line.strip()[-1] == '0' and refresh == 1:
                refresh += 1
        elif 'PIDXScan_ECI_Converted_ScanDataLabel' in line.strip():
            if refresh < 2:
                continue
            # print("Line{}: {}".format(countLine, line.strip()))
            refresh += 1
            add_child_data(refresh, dictData, line.strip())

        if refresh == 3:
            refresh = 0
            # print('-------------------------')
            if len(dataList) == 0:
                dataList.append(dictData)
            else:
                data_is_existed = False
                for datas in dataList:
                    if (dictData['symID'] == datas['symID'] and dictData['symType'] == datas['symType']
                            and dictData['fullData'] == datas['fullData']):
                        # update count
                        datas['count'] = datas['count'] + 1
                        # data is existed
                        data_is_existed = True
                        if is_misread(datas['fullData'], listExpectedData):
                            datas['isMisread'] = True
                        break

                if not data_is_existed:
                    if is_misread(dictData['fullData'], listExpectedData):
                        dictData['isMisread'] = True
                    dataList.append(dictData)
            dictData = {
                'symID': '',
                'symType': 'Unknown',
                'fullData': '',
                'count': 1,
                'isMisread': False
            }

    # count total label missread
    for i in range(len(dataList)):
        if dataList[i]['isMisread']:
            countData_Misread += 1
        else:
            # move all data passed to top list
            dataList.insert(0, dataList.pop(i))
            countData_Passed += 1

    # check expected no read
    list_exp_not_found = [i for i in listExpectedData if i not in [j['fullData'] for j in dataList]]
    for tmp_item in list_exp_not_found:
        dictData = {
            'symID': 'Unknown',
            'symType': 'Unknown',
            'fullData': tmp_item,
            'count': 0,
            'isMisread': False
        }
        dataList.insert(0, dictData)

    report_file_path = report_dualtest(dataList, countData_Passed, countData_Misread, len(list_exp_not_found), outputPath, interface)
    link = dirname(abspath(report_file_path)) + '/' + report_file_path.split(r'/')[-1]
    webbrowser.open(link)


def add_child_data(refresh, dict_data, line):
    if refresh == 1:
        # add data for dictData[symID]
        dict_data.update({"symID": line[line.rfind(':') + 2:]})
    elif refresh == 2:
        # add data for dictData[symType]
        dict_data.update({"symType": line[line.rfind(':') + 2:]})
    elif refresh == 3:
        # add data for dictData[fullData]
        dict_data.update({"fullData": line[line.rfind(':') + 2:]})
    return dict_data


def is_misread(data, listExpectedData):
    if data not in listExpectedData:
        return True
