import csv
csv_columns = ['No','Name','Country']
red_values = [82014, 135086, 139003]
ir_values =  [82000, 123334, 123450]
def Mean(x ):
    total =0
    for i in range(len(x)):
        total += x
    return total/len(x)


dict_data = [
{'Name': '路人A', '心跳': None, '脈搏': None,},
{'Name': '路人B', '心跳': None, '脈搏': None},
{'Name': '路人C', '心跳': None, '脈搏': None},
{'Name': '路人E', '心跳': None, '脈搏': None},
]

dict_data = [
{'Name': '路人A', '心跳':2, '脈搏': None,},
{'Name': '路人B', '心跳': None, '脈搏': None},
{'Name': '路人C', '心跳': None, '脈搏': None},
{'Name': '路人E', '心跳': None, '脈搏': None},
]


if(name == '路人A'):

    result = dict_data('路人A')
    心跳 = dict_data()
csv_file = "Names.csv"
try:
    with open(csv_file, 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
except IOError:
    print("I/O error")