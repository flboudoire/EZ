import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

class Data():
    def __init__(self, freq, Z, E = float('nan')):
        self.freq = freq
        self.Z = Z
        self.E = E

def load_raw(file, delimiter = "\t"):
    data_raw = []
    with open(file, "r", encoding="cp1252") as f:
        for line in f:
            row = []
            try:
                for val in line.split(delimiter):
                    row.append(float(val))
                if len(row) > 0:
                    data_raw.append(row)
            except ValueError:
                continue
    return np.array(data_raw)

def load_datas(data_raw, columns):
    datas = []
    c_freq = columns[0]
    c_reZ = columns[1]
    c_imZ = abs(columns[2])
    sign_Im = 1.
    if columns[2] < 0:
        sign_Im = -1.
    if len(columns) == 4:
        c_E = columns[3]
        precision = 2 # rounding precision for E
        Es = data_raw[:, c_E] # get all E values
        Es_round = np.round(Es, precision) # round E values
        Es = list(set(Es_round)) # get all possible E values after rounding
        Es.sort()
        for E in Es:
            data_raw_E = data_raw[Es_round == E, :]
            freq = data_raw_E[:, c_freq]
            Z = data_raw_E[:, c_reZ] + sign_Im*1j*data_raw_E[:, c_imZ]
            idx = freq > 0
            freq = freq[idx]
            Z = Z[idx]
            datas.append(Data(freq = freq, Z = Z, E = E))
    else:
        freq = data_raw[:, c_freq]
        Z = data_raw[:, c_reZ] + 1j*data_raw[:, c_imZ]
        idx = freq > 0
        freq = freq[idx]
        Z = Z[idx]
        datas.append(Data(freq = freq, Z = Z))
    return datas

if __name__ == "__main__":
    folder = sys.argv[1]
    if not os.path.exists(folder):
        os.mkdir(folder)
    data_raw = load_raw(folder+".mpt", "\t")
    datas = load_datas(data_raw, [0, 1, -2, 6])
    for data in datas:
        content = pd.DataFrame(
            np.array([data.freq, np.real(data.Z), np.imag(data.Z)]).T,
            columns = ["Frequency [Hz]", "Re(Z) [Ohm]", "Im(Z) [Ohm]"]
            )
        str_E = fr"{data.E:.3f}".replace(".", "_")
        content.to_csv(rf"{folder}/{str_E} V vs Ag_AgCl.csv", index=False)