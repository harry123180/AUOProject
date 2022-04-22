# Python code to
# demonstrate readlines()



# Using readlines()
file1 = open('all10000.txt', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
for line in Lines:
    count += 1
    a = line.strip()
    print(a.split()[1])
    #print("Line{}: {}".format(count, line.strip()))