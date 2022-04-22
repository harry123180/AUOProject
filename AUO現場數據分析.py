path = 'all10000.txt'
f = open(path, 'r')
a = f.read()
print(len(a))
b = a.split()
print(len(b))

for line in f.readlines():
    print(line)
    print("?")
f.close()