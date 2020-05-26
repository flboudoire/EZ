import numpy as np
import matplotlib.pyplot as plt

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

class Data():
    def __init__(self, freq, Z, E = float('nan')):
        self.freq = freq
        self.Z = Z
        self.E = E

class Dataset():

    def __init__(self, file):
        self.file = file
        self.extensions_supported = ["mpt"]
        self.Es = []
        file_extension = self.file.split(".")[1]
        if file_extension in self.extensions_supported:
            self.load(file_extension)
            self.is_loaded = True
        else:
            print("Unsuported file format")
            self.is_loaded = False

    def load(self, file_extension):
        ext2delim = {
            "mpt": "\t"
        }
        data_raw = load_raw(self.file, ext2delim[file_extension])
        ext2columns = {
            "mpt": [0, 1, -2, 6]
        } # [freq, Re(Z), Im(Z), E (if needed)]
        self.datas = load_datas(data_raw, ext2columns[file_extension])
        for data in self.datas:
            self.Es.append(data.E)