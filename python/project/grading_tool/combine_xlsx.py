from os import listdir
import xlrd
import xlwt

files = []
week = raw_input("Which week you want to grade > ")
path = "~/Desktop/Week" + week + "/"
result = xlwt.Workbook()
result_sheet = result.add_sheet("Combined Sheet")

for f in listdir(path): 
    if f.split('.')[-1] == 'xlsx':
        files.append(f)

current_col = 4
for file in files:
    worksheet = xlrd.open_workbook(path + file).sheet_by_index(0)
    for col_index in range(2,4): 
        data = [worksheet.cell_value(row, col_index) for row in range(worksheet.nrows)]
        data[0] = file.split('_')[-1].split('.')[0]
        for index, value in enumerate(data):
            result_sheet.write(index, current_col, value)
        current_col += 1

result.save(path + "combined_file.xls")
