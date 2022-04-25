import numpy as np

from scipy.fftpack import fft,ifft

import matplotlib.pyplot as plt

from matplotlib.pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei'] #顯示中文

mpl.rcParams['axes.unicode_minus']=False #顯示負號

#採樣點選擇1400個，因為設置的信號頻率分量最高為600赫茲，根據採樣定理知採樣頻率要大於信號頻率2倍，所以這裡設置採樣頻率為1400赫茲（即一秒內有1400個採樣點，一樣意思的）

x=np.linspace(0,1,1400)

#設置需要採樣的信號，頻率分量有200，400和600

y=7*np.sin(2*np.pi*200*x) + 5*np.sin(2*np.pi*400*x)+3*np.sin(2*np.pi*600*x)

fft_y=fft(y) #快速傅立葉變換

N=1400

x = np.arange(N) # 頻率個數

half_x = x[range(int(N/2))] #取一半區間

abs_y=np.abs(fft_y) # 取複數的絕對值，即複數的模(雙邊頻譜)

angle_y=np.angle(fft_y) #取複數的角度

normalization_y=abs_y/N #歸一化處理（雙邊頻譜）

normalization_half_y = normalization_y[range(int(N/2))] #由於對稱性，只取一半區間（單邊頻譜）

plt.subplot(231)

plt.plot(x,y)

plt.title('原始波形')

plt.subplot(232)

plt.plot(x,fft_y,'black')

plt.title('雙邊振幅譜(未求振幅絕對值)',fontsize=9,color='black')

plt.subplot(233)

plt.plot(x,abs_y,'r')

plt.title('雙邊振幅譜(未歸一化)',fontsize=9,color='red')

plt.subplot(234)

plt.plot(x,angle_y,'violet')

plt.title('雙邊相位譜(未歸一化)',fontsize=9,color='violet')

plt.subplot(235)

plt.plot(x,normalization_y,'g')

plt.title('雙邊振幅譜(歸一化)',fontsize=9,color='green')

plt.subplot(236)

plt.plot(half_x,normalization_half_y,'blue')

plt.title('單邊振幅譜(歸一化)',fontsize=9,color='blue')

plt.show()



