day = 28
hours = 10
for j in range(82):
    hours= hours+1
    if(hours==24):
        hours =0
        day+=1
    path = 'G:\\AUOdata\\00_' + str(day) + '_' + str(hours) + '.txt'
    if(hours<10):
        path = 'G:\\AUOdata\\00_' + str(day) + '_' + '0'+str(hours)+ '.txt'
    print(day,hours)
    new_path = 'G:\\AUOdata\\output'+str(j)+'.txt'
    try:
        f = open(path, 'r')
        nf =open(new_path,'w')
        #print(f.read())
        cnt =0
        for i in f.readlines():
            if(cnt%2==0):
                nf.write(i)
                #print(i)
            cnt+=1
        f.close()
        nf.close()
    except:
        pass