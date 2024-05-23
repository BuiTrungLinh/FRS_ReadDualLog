import webbrowser

import gui
from report import *
from pathlib import Path
from os.path import dirname, abspath
import os


path_log_file = './files/OPOS_LOG_FILE_0.log'
path_expected_file = './files/ExpectedData.txt'
outputPath = ''

if __name__ == '__main__':
    gui.start_up()


def process(pathlogfile, pathexpfile):
    fileLog = None
    path_log_file = pathlogfile
    path_expected_file = pathexpfile
    try:
        fileLog = open(pathlogfile, 'r')
    except:
        gui.show_msg('Error Message', 'There is a problem with the path, please check it again!')
        return
    Lines = [i.strip() for i in fileLog.readlines()]
    verify(Lines)


def verify(lines):
    interface = 'RS232-STD/USBCOM'
    countLine = 0
    countData = 0
    countData_Passed = 0
    countData_Misread = 0
    refresh = 0
    datasList = []
    dictData = {
        'no': 0,
        'symID': '',
        'symType': 'Unknown',
        'fullData': '',
        'count': 1,
        'isMisread': False
    }
    # Check current interface in log file
    if 'Registry Main Key: SOFTWARE\\OLEforRetail\\ServiceOPOS\\Scanner\\USBScanner' in lines:
        interface = 'USBOEM'
    elif 'Registry Main Key: SOFTWARE\\OLEforRetail\\ServiceOPOS\\Scanner\\SC-COM' in lines:
        interface = 'USBCOM-SC'

    # Process for expected file
    # Read file
    fileExpected = open(path_expected_file)
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
            if len(datasList) == 0:
                datasList.append(dictData)
            else:
                for datas in datasList:
                    if (dictData['symID'] == datas['symID'] and dictData['symType'] == datas['symType']
                            and dictData['fullData'] == datas['fullData']):
                        # update count
                        datas['count'] = datas['count'] + 1
                        if is_misread(datas['fullData'], listExpectedData):
                            datas['isMisread'] = True
                        break
                    if datasList[-1]['fullData'] == datas['fullData']:
                        if is_misread(dictData['fullData'], listExpectedData):
                            dictData.update({'isMisread': True})
                        datasList.append(dictData)
                        countData += 1
                        break
                    #   Check misread
            dictData = {
                'no': 0,
                'symID': '',
                'symType': 'Unknown',
                'fullData': '',
                'count': 1,
                'isMisread': False
            }

    # count total label missread
    for i in range(len(datasList)):
        datasList[i]['no'] = i + 1
        if datasList[i]['isMisread']:
            countData_Misread += 1
        else:
            countData_Passed += 1

    report_file_path = report_dualtest(datasList, countData_Passed, countData_Misread, outputPath, interface)
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
