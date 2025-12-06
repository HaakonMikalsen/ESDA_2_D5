import os 
import matplotlib.ticker as mticker 
import codecs
import csv
import numpy as np
import matplotlib.pyplot as plt







dir_path = os.path.dirname(os.path.realpath(__file__))

networkFilePath = dir_path+r"/data/networkNew.csv"

dataFile = codecs.open(networkFilePath, encoding="utf-8", errors="ignore")


skipLinesStart = 34
skipLinesEnd = None
f,amplitude= np.array(list(csv.reader(dataFile.readlines()[skipLinesStart:skipLinesEnd]))).T
dataFile.close()

f = np.array([element for element in f],dtype=float)
amplitude = np.array([element for element in amplitude],dtype=float)

# f = np.array([element.replace(" kHz","") for element in f],dtype=float)
# rms = np.array([element.replace(" Ṽ","").replace(" mṼ","e-3") for element in rms],dtype=float)

plt.style.use("seaborn-v0_8-dark")
plt.grid(True, linestyle="--", alpha=0.6)
plt.axhline(0, color="black", linewidth=1)
plt.axvline(0, color="black", linewidth=1)

plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f dB"))
plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f hz"))

plt.xlabel("Frekvens [Hz]", fontsize=12)
plt.ylabel("Amplituderespons [dB]", fontsize=12)

plt.xscale("log")
plt.title(
    f"Amplituderespons til bufferkrets", fontweight="bold"
)
plt.plot(
    f,
    amplitude,
    linewidth=2,
    color="royalblue",
    label="Amplituderespons"
)
plt.axvline(x=35,color="crimson",linestyle="--",label="Knekkfrekvens 35Hz")
# plt.xlim(-100,10**5)
# plt.plot(
#     t * 1000, signal * 1000, linewidth=2, color="crimson", label="Faktisk signal"
# )
#    linestyle="--",

plt.legend(frameon=True, edgecolor="dimgray", facecolor="lavender", fontsize=12)

plt.tight_layout()


plt.savefig("./bilder/frekres.png")
plt.show()
