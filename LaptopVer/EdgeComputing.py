import numpy as np
from scipy.signal import butter, lfilter, freqz


def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
    description:
        lowpass filter
        parameter:
            data: numpy array 
            cutoff: cutoff frequency
            fs: sampling rate
            order: lowpass filter order
        return:filtered signal
            type:list
    """
    try:
        if(isinstance(data,list)):
            data = np.array(data)
    except:
        print("Low Pass Filater input Value Type Error!")
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    
    return y.tolist()
def Mean(original_signal):
    """
    description:
        the Mean() function will return average value of orignal_signal
        parameter :
            original_signal:
                type:list integer or float
        return:
            average of original_signal:
                type:float 

    """
    return sum(original_signal)/len(original_signal)
def Standard_Deviation(original_signal):
    """
    drscription:
    the Standard_Deviation() function will return value of Standard Deviation
        parameter:
            original_signal:
                type:list integer or float
        return:
            Standard Deviation of original_signal
                type:float
    """
    avg = Mean(original_signal)
    total = 0
    for i in range(len(original_signal)):
        total = total + pow((original_signal[i]-avg),2)
    return total/len(original_signal)
def RMS(original_signal):
    """
    description:
    The RMS() function will return Root Mean Square value of original_signal
        parameter:
            original_signal:
                type:list integer or float
        return: 
            RMS
                type:float
    """
    return np.sqrt(np.mean(y**2))

def Kurtosis(original_signal):
    num = 0
    for i in range(len(original_signal)):
        num = num + pow((original_signal[i]-Mean(original_signal)),4)
    return num/(4*Standard_Deviation(original_signal))

de