import os
import matplotlib.ticker as mticker
import codecs
import csv
import numpy as np
import matplotlib.pyplot as plt


RK = 8200
RL = 180


def Ri(v1, v0):
    if v0 == v1:
        return 0
    return (RK * v1) / (v0 - v1)


def Ro(v1, v2):
    return RL * (v1 - v2) / (v2)


import numpy as np


def averagePeak(signal, filter=5):
    signal = np.array(signal)
    signal = signal - np.mean(signal)
    signal = np.abs(signal)
    signalCutOff = np.mean(signal) * np.sqrt(2)
    mask = signal >= signalCutOff

    segments = []
    current_segment = []

    for value, is_high in zip(signal, mask):
        if is_high:
            current_segment.append(value)
        else:
            if current_segment and len(current_segment) >= filter:
                segments.append(current_segment)
                current_segment = []

    # Add last segment if still open
    if current_segment and len(current_segment) >= filter:
        segments.append(current_segment)

    peakVals = []
    for segment in segments:
        peakVals.append(np.max(np.array(segment)))

    continuous = [val for seg in segments for val in seg]
    # plt.plot(continuous)
    # plt.show()

    return np.mean(np.array(peakVals))


def findPeaks(signal):
    peaks = []
    for i in range(1, len(signal) - 1):
        if signal[i - 1] < signal[i] and signal[i] > signal[i + 1]:
            if signal[i] > 0:
                peaks.append(i)
    return peaks


# dir_path = os.path.dirname(os.path.realpath(__file__))+"/data/oldScopeData"
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/data/scopedata"
file_list = os.listdir(dir_path)

amplitudeData = []
for file_name in file_list:

    dataFile = codecs.open(
        dir_path + "/" + file_name, encoding="utf-8", errors="ignore"
    )

    unitScale = (file_name.find("mv") < file_name.find("V")) * 1 + (
        file_name.find("mv") > file_name.find("V")
    ) * (1 / 1000)

    unitIndex = max(file_name.find("mv"), file_name.find("V"))
    # print(unit)
    # print(file_name[:unitIndex])
    Av0 = 0.5
    try:
        Av0 = float(file_name[:unitIndex].strip()) * unitScale
    except:
        pass

    print(Av0)

    skipLinesStart = 34
    skipLinesEnd = -2
    t, v2_data, v1_data = np.array(
        list(csv.reader(dataFile.readlines()[skipLinesStart:skipLinesEnd]))
    ).T
    dataFile.close()

    t = np.array([element for element in t], dtype=float)
    v1_data = np.array([element for element in v1_data], dtype=float)
    v2_data = np.array([element for element in v2_data], dtype=float)

    if Av0 == 0.5:
        plt.style.use("seaborn-v0_8-dark")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.axhline(0, color="black", linewidth=1)
        plt.axvline(0, color="black", linewidth=1)

        plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f mV"))
        plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f ms"))
        plt.title(
            f"Utgangsignal v2(t)", fontweight="bold"
        )
        plt.yticks([-500,-400,-300,-200,-100,0,100,200,300,400,500])
        plt.xlabel("t [ms]", fontsize=12)
        plt.ylabel("Spenning [mV]", fontsize=12)
        # plt.plot(t,v1_data)
        plt.plot(
            (t - t[90])[90:890] * 1000,
            v2_data[90:890] * 1000,
            linewidth=2,
            color="royalblue",
            label="v2",
        )
        plt.legend(frameon=True, edgecolor="dimgray", facecolor="lavender", fontsize=12)
        plt.tight_layout()


        plt.savefig("./bilder/skope.png",dpi=1000)
        plt.show()

    Av1 = averagePeak(v1_data)
    Av2 = averagePeak(v2_data)
    # Av1 = np.max(v1_data-np.mean(v1_data))
    # Av2 = np.max(v2_data-np.mean(v2_data))

    # Av1 = min(Av1,Av0)
    # Av2 = min(Av2,Av0)
    amplitudeData.append(
        {
            "V0": Av0,
            "V1": Av1,
            "V2": Av2,
        }
    )
