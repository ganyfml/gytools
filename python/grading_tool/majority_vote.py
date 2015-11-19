import os
import xlrd
import xlwt

class smart_dict(dict):
    def __missing__(self, key):
        return 0

files = []
week = raw_input("Which week you want to grade > ")
path = "~/Desktop/Week\ " + week + "/"
result_path = path + 'Week ' + week + '.xlsx'

if not os.path.exists(path):
    print "Folder not exist, program exit"
    quit()

for f in os.listdir(path): 
    if f.split('.')[-1] == 'xlsx':
        files.append(f)

data_map = smart_dict() 
for file in files:
    worksheet = xlrd.open_workbook(path + file).sheet_by_index(0)
    data = [worksheet.cell_value(row, 2) for row in range(worksheet.nrows)]
    for index, value in enumerate(data):
        content = value.encode('ascii','ignore').lower()
        if 'n' in content:
            data_map[index] -= 1
        elif 'y' in content:
           data_map[index] += 1
        data_map[-index] += 1

result = xlwt.Workbook()
worksheet = result.add_sheet("Combined Sheet")
for index in range(1, len(data_map)):
    current_key = data_map.keys()[index]
    if current_key < 0:
        continue
    num_totalAnswer = data_map[-current_key]
    num_totalVoteNo = (num_totalAnswer - data_map[current_key])/2

    relevant = 'Yes (' + str(num_totalAnswer - num_totalVoteNo) + '/' + str(num_totalAnswer) + ')'
    if data_map[current_key] < 0:
        relevant = 'No (' + str(num_totalVoteNo) + '/' + str(num_totalAnswer) + ')' 
    
    if abs(data_map[current_key]) <= 3:
        relevant += ' (Talk)'
    worksheet.write(data_map.keys()[index], 4, relevant)
result.save(path + "result_test.xls")
