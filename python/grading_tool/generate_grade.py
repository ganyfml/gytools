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

student_name = []
student_num_wrong = []
files = []

if not os.path.exists(path):
    print "Folder not exist, program exit"
    quit()

for f in os.listdir(path): 
    if f.split('.')[-1] == 'xlsx':
        files.append(f)
        student_name.append(f.split('.')[0].split('_')[1])

answer_map = smart_dict()
answer = xlrd.open_workbook(answer_path).sheet_by_index(0)
data = [answer.cell_value(row, 2) for row in range(0, answer.nrows)]
for index, value in enumerate(data):
    content = value.encode('ascii','ignore').lower()
    if content:
        if 'n' in content:
            answer_map[index] = 'n'
        elif 'y' in content:
            answer_map[index] = 'y'
num_question = len(answer_map) - 1; # First row is row description

for index in range(0, len(files)):
    worksheet = xlrd.open_workbook(path + files[index]).sheet_by_index(0)
    data = [worksheet.cell_value(row, 2) for row in range(worksheet.nrows)]
    current_num_wrong = 0
    for index, value in enumerate(data):
        content = value.encode('ascii','ignore').lower()
        #print content + "," + str(answer_map[index])
        if answer_map[index] != 0:
            if (content and (answer_map[index] not in content)) or (('n' or 'y') not in content):
                current_num_wrong += 1
    student_num_wrong.append(current_num_wrong)

grade_file = open(grade_path, 'w')
for index in range(0, len(files)):
    grade_file.write('#' + student_name[index] + '\n')
    grade_file.write('- num of wrong: ' + str(student_num_wrong[index]))
    grade_file.write('\n')
