path = 'output.txt'
f = open(path, 'w')
f.write('Hello World')
f.write(123)
f.write(123.45)
f.close()