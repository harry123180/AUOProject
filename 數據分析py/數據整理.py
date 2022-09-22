path = 'G:\\AUOdata\\00_28_10.txt'
f = open(path, 'r')
#print(f.read())
cnt =0
for i in f.readlines():
    if(cnt%2==0):
        print(i)
    cnt+=1
f.close()