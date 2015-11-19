import os
import xlrd
import xlwt

class smart_dict(dict):
    def __missing__(self, key):
        return 0

week = raw_input("Which week you want to grade > ")
path = "/home/gany/Desktop/Week " + week + "/"
answer_path = path + 'combined_file.xls'
grade_path = path + 'grade.mkd'

files = []

#Check if the path exists
if not os.path.exists(path):
    print "Folder not exist, program exit"
    quit()

#Collect all the students` files
for f in os.listdir(path): 
    if f.split('.')[-1] == 'xlsx':
        files.append(f)

#Get the right result from combination.xls
answer_map = smart_dict()
answer = xlrd.open_workbook(answer_path).sheet_by_index(0)
data = [answer.cell_value(row, 2) for row in range(answer.nrows)]
for index, value in enumerate(data):
    content = value.encode('ascii','ignore').lower()
    if content:
        if 'n' in content[0]:
            answer_map[index] = 'n'
        elif 'y' in content[0]:
            answer_map[index] = 'y'

#Collect the num of wrong answers for each student
grade_file = open(grade_path, 'w')
for index in range(0, len(files)):
    grade_file.write('#' + files[index].split('.')[0].split('_')[1] + '\n' + '- Wrong question index: ')
    worksheet = xlrd.open_workbook(path + files[index]).sheet_by_index(0)
    data = [worksheet.cell_value(row, 2) for row in range(worksheet.nrows)]
    current_num_wrong = 0
    for index, value in enumerate(data):
        content = value.encode('ascii','ignore').lower()
        if answer_map[index] != 0:
            if (not content) or (answer_map[index] not in content):
                current_num_wrong += 1
                grade_file.write(str(index + 1) + ',')
    grade_file.write('\n- num of wrong: ' + str(current_num_wrong) + '\n\n')
