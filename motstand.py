import os 
import matplotlib.ticker as mticker 
import codecs
import csv
import numpy as np
import matplotlib.pyplot as plt



RK =8200
RL = 180


def Ri(v1,v0):
    if (v0==v1):
        return 0
    return RK*v1/(v0-v1)
def Ro(v1,v2):
    return RL*(v1-v2)/(v2)


def averagePeak(signal):
    peaks = []
    for i in range(1, len(signal)-1):
        if signal[i-1] < signal[i] and signal[i] > signal[i+1]:
            if signal[i]>0:
                peaks.append((signal[i]))
    return np.mean(peaks)


dir_path = os.path.dirname(os.path.realpath(__file__))+"/data/scopedata"
file_list = os.listdir(dir_path)

amplitudeData = []
for file_name in file_list:

    dataFile = codecs.open(dir_path+"/"+file_name, encoding="utf-8", errors="ignore")

    unitScale = (file_name.find("mv")<file_name.find("V"))*1 +(file_name.find("mv")>file_name.find("V"))*(1/1000)

    unitIndex = max(file_name.find("mv"),file_name.find("V"))
    # print(unit)
    # print(file_name[:unitIndex])

    Av0 = float(file_name[:unitIndex].strip())*unitScale
    print(Av0)

    skipLinesStart = 34
    skipLinesEnd = -2
    t,v2_data,v1_data= np.array(list(csv.reader(dataFile.readlines()[skipLinesStart:skipLinesEnd]))).T
    dataFile.close()

    t = np.array([element for element in t],dtype=float)-2
    v1_data = np.array([element for element in v1_data],dtype=float)-2
    v2_data = np.array([element for element in v2_data],dtype=float)

    # if Av0 == 0.5:
    #     plt.plot(t,v1_data)
    #     plt.show()

    Av1 = averagePeak(v1_data)
    Av2 = averagePeak(v2_data)

    # Av1 = min(Av1,Av0)
    # Av2 = min(Av2,Av0)
    amplitudeData.append({
        "V0":Av0,
        "V1":Av1,
        "V2":Av2,
        }
    )

amplitudeData = sorted(amplitudeData,key=lambda x: x["V0"])
for point in amplitudeData:
    v0 = point["V0"]
    v1 =point["V1"]
    v2 = point["V2"]
    print(f"|{v0:.3f}|{v1:.3f}|{v2:.3f}|{abs(v2-v0):.3f}|{(v2/v0):.3f}|{Ri(v1,v0):.3f}|{Ro(v1,v2):.3f}|")