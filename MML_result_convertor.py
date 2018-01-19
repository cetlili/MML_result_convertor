import re
import sys


last_line = '\n'
mo_temp = ''
ne_temp = ''
report_temp = ''
recode_temp = ''
locell_temp = ''
para_temp = ''
mo = []
ne = []
report = []
recode = []
locell = []
para = []
k1 = 'MML Command-----'
k2 = 'NE :'
k3 = 'Report :'
k4 = 'RETCODE ='
k5 = 'LOCALCELLID'

p1 = re.compile(r'MML Command-----[A-Z]{3} ((?<!:)\w+)')
p2 = re.compile('NE :(.*)')
p3 = re.compile('Report :(.*)')
p4 = re.compile('RETCODE = [0-9]+ (.*)')
p5 = re.compile('LOCALCELLID=(.*?),.*')
# p6 = re.compile(r'((?<=:)(LOCALCELLID=[0-9]?.*|.*))')
p6 = re.compile(r'.*LOCALCELLID=[0-9]+,(.*)')
p7 = re.compile(':(.*);')
# file_name = 'MML_Task_Result_small cell_20170719_094746.txt'


file_name = input('Please input file name (input absolute path if MML result file is not in same folder of exe file,type q to quit:')
csvfilename = file_name.split(sep=".")[0] + ".csv"
if file_name.lower() =='q':
    sys.exit()

try:
    file = open(file_name, "r")
    t = False
except IOError:
    file_name=input("Error: File does not appear to exist,please check the file name and try again")
    sys.exit()

# with open(file_name) as file:
for i, line in enumerate(file):

    if line in ['\n', '\r\n'] and last_line not in ['\n', '\r\n']:

        # pack up all data

        if mo_temp:
            mo.append(mo_temp)
            if not locell_temp:
                locell.append(' ')
            else:
                locell.append(locell_temp[0])
            if not para_temp:
                para.append(' ')
            else:
                para.append(para_temp[0])
        if ne_temp:
            ne.append(ne_temp)
        if report_temp:
            report.append(report_temp)

            if not recode_temp:
                recode.append('No recode')
            else:
                recode.append(recode_temp)
        mo_temp = ''
        ne_temp = ''
        report_temp = ''
        recode_temp = ''
        locell_temp = ''
        para_temp = ''
        # print(i,mo,ne)

    if k2 in line:
        ne_temp = p2.findall(line)[0]
        # print(i,ne_temp)

    if k1 in line:
        mo_temp = p1.findall(line)[0]
        locell_temp = p5.findall(line)
        if k5 in line:
            pp = p6
        else:
            pp = p7
        para_temp = pp.findall(line)
        # print(i, mo_temp, para_temp)

    if k3 in line:
        report_temp = p3.findall(line)[0]
        # print(i,report_temp)
    if k4 in line:
        recode_temp = p4.findall(line)[0]
        # print(recode_temp)
    last_line = line
file.close()
ne.insert(0, "NE Name")
mo.insert(0, 'MO Name')
report.insert(0, 'Report')
recode.insert(0, 'Return code')
locell.insert(0, 'Locell ID')
para.insert(0, 'Parameters')
z = zip(ne, mo, locell, para, report, recode)

import csv

with open(csvfilename, 'w', newline='') as csvfile:
    wr = csv.writer(csvfile, dialect='excel')
    wr.writerows(z)
