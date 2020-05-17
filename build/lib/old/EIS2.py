import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as ipyw
from IPython.display import display
import pandas as pd
import fb_1.utilities.stderr as stderr
from fb_1.electrochemistry import AgCl2RHE
from scipy import constants as const
import lmfit


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


def load_datas(data_raw, columns, N_points_min = 0, range_omega = []):

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
            if len(Z) >= N_points_min:
                if len(range_omega) > 0:
                    omega = 2*np.pi*freq
                    idx = (omega >= np.min(range_omega))*(omega <= np.max(range_omega))
                else:
                    idx = (freq < np.inf)
                datas.append(Data(freq = freq[idx], Z = Z[idx], E = E))
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
        self.omega = 2*np.pi*freq
        self.Z = Z
        self.E = E
        self.circuit = None

    def plot(
        self,
        axes = None,
        color = "C0",
        print_result = True,
        partial_circuits = None
        ):

        if axes is None:
            fig, axes = figure_layout()

        style = dict(
            marker = ".",
            linestyle = "none",
            markersize = 2,
            color = color
            )
        axes[0].plot(self.omega, -self.Z.imag/1000, **style)
        axes[1].plot(self.omega, self.Z.real/1000, **style)
        axes[2].plot(self.Z.real/1000, -self.Z.imag/1000, **style)

        if self.circuit is not None:
            self.circuit.plot(
                axes = axes,
                pars = self.fit_result.params,
                color = color,
                range_omega = [np.min(self.omega), np.max(self.omega)],
                partial_circuits = partial_circuits
                )
            if print_result:
                display_pars(self.fit_result.params)

    def fit(self, circuit = None, pars = dict(), print_result = True):

        if type(circuit).__name__ == "Circuit":
            self.circuit = circuit
            self.fit_result = circuit.fit(
                self.omega,
                self.Z,
                pars = pars,
                print_result = print_result
                )
            self.pars = self.fit_result.params
        else:
            raise ValueError()


class Dataset():

    def __init__(
        self,
        file,
        pH = None,
        E_ref = 0,
        area = 0.25,
        N_points_min = 0,
        range_omega = [],
        ref_name = "ref"
        ):

        self.file = file
        self.extensions_supported = ["mpt"]
        self.Es = []
        self.pH = pH
        self.E_ref = E_ref
        self.N_points_min = N_points_min
        self.range_omega = range_omega
        self.area = area # area in cm2
        self.ref_name = ref_name
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
        self.datas = load_datas(
            data_raw,
            ext2columns[file_extension],
            N_points_min = self.N_points_min,
            range_omega = self.range_omega
            )
        for data in self.datas:
            self.Es.append(data.E)
            data.Z *= self.area
        self.Es = np.array(self.Es)
        if self.pH is None:
            self.Es = self.Es - self.E_ref
            self.E_label = r"E [V vs E$\rm _{%s}$]"%self.ref_name
            self.E_unit = r"V vs E$\rm _{%s}$"%self.ref_name
        else:
            self.Es = AgCl2RHE(self.Es, pH = self.pH)
            self.E_label = "E [V vs RHE]"
            self.E_unit = "V vs RHE"


    def fit(
        self,
        circuit,
        pars = dict(),
        print_result = False,
        consecutive = True
        ):

        for i, data in enumerate(self.datas):
            if i > 0 and consecutive:
                prev_pars = self.datas[i-1].pars
                init_pars = dict()
                for key in prev_pars:
                    p = prev_pars[key]
                    param_dict = dict(
                        value = p.value,
                        vary = p.vary,
                        min = p.min,
                        max = p.max
                        )
                    init_pars.update({key: param_dict})
            else:
                init_pars = pars
                
            data.fit(
                circuit = circuit,
                pars = init_pars,
                print_result = print_result
                )

        self.pars = dict()
        for key in data.pars:
            elem, label = key.split("_")
            name = r"%s$\rm_{%s}$"%(elem, label)
            scale = 1
            unit = ""
            if elem == "R":
                scale = 1e-3
                unit = r"k$\rm\Omega\cdot$cm$^{2}$"
            elif elem == "C":
                scale = 1e6
                unit = r"$\rm\mu$F$\cdot$cm$^{-2}$"

            y = list()
            for data in self.datas:
                floatstd = stderr.param2floatstd(data.pars[key])
                y.append(floatstd)

            par = Parameter(
                name = name,
                x = self.Es,
                y = y,
                unit = unit,
                scale = scale,
                xlabel = self.E_label
                )
            self.pars.update({key: par})


    def plot_i(self, i, print_result, print_figure, partial_circuits):
        title = f"{self.Es[i]:.3f} {self.E_unit}"
        self.datas[i].plot(
            print_result = print_result,
            partial_circuits = partial_circuits
            )
        plt.title(title)
        if print_figure:
            plt.savefig(
                self.file.split(".")[0] + "_" + title + ".png",
                dpi = 300,
                bbox_inches='tight',
                transparent=True
                )


    def plot(
        self,
        axes = None,
        interact = False,
        print_result = True,
        partial_circuits = None
        ):

        if interact:

            ipyw.interact(
                self.plot_i,
                print_result = print_result,
                print_figure = False,
                i=ipyw.IntSlider(
                    min=0,
                    max=len(self.datas)-1,
                    step=1,
                    value=0,
                    continuous_update=False
                    ),
                partial_circuits = ipyw.fixed(partial_circuits)
                )

        else:

            if axes is None:
                fig, axes = figure_layout()

            cmap = plt.get_cmap("rainbow")
            for i, data in enumerate(self.datas):
                color = cmap(float(i)/(len(self.datas)-1))
                data.plot(
                    axes = axes,
                    color = color,
                    print_result = False,
                    )

            # Hack to get colorbar for plot in matplotlib
            Z = [[0,0],[0,0]]
            Es = np.linspace(np.min(self.Es), np.max(self.Es), 150)
            dmy = axes[2].contourf(Z, Es, cmap=cmap, linestyle = "none")
            plt.colorbar(
                dmy,
                orientation = "horizontal",
                ticks = make_ticks(self.Es),
                label = self.E_label
                )


class Parameter():

    def __init__(self, x, y, name = "", unit = "", scale = 1, xlabel = ""):

        self.name = name
        self.unit = unit
        self.scale = scale
        self.x = x
        self.y = y
        self.fit_x = None
        self.fit_y = None
        self.model_func = None
        self.fit_result = None
        self.xlabel = xlabel
        self.update()
        self.build_ylabel()

    def update(self):

        self.values = list()
        self.stderrs = list()
        for y in self.y:
            self.values.append(y.value)
            if y.stderr is not None:
                self.stderrs.append(y.stderr)
            else:
                self.stderrs.append(0)
        self.values = np.array(self.values)
        self.stderrs = np.array(self.stderrs)

    def fit(self, pars = dict(), range_x = [], print_result = True):

        if self.model_func is not None:

            idx, min_x, max_x = lim_x(self.x, range_x)

            x = self.x[idx]
            y = self.values[idx]

            model = lmfit.Model(self.model_func, nan_policy='omit')
            params = model.make_params()

            for key in pars:
                params[key].set(**pars[key])

            self.fit_result = model.fit(y, params, x=x)
            self.pars = self.fit_result.params
            self.fit_x = np.linspace(min_x, max_x, 200)
            self.fit_y = self.model_func(
                x = self.fit_x,
                **self.fit_result.params.valuesdict()
                )

            if print_result:
                display_pars(self.fit_result.params)


    def build_ylabel(self):

        self.ylabel = f"{self.name}"
        if self.unit != "":
            self.ylabel += f" [{self.unit}]"


    def plot(
        self,
        fig = None,
        range_x = [],
        label = "",
        marker = ".",
        errorbar = True
        ):

        if fig is None:
            fig = plt.figure()

        plt.xlabel(self.xlabel)
        self.build_ylabel()
        plt.ylabel(self.ylabel)

        idx, *dmy = lim_x(self.x, range_x)

        if errorbar:
            l = plt.errorbar(
                self.x[idx],
                self.values[idx]*self.scale,
                yerr=self.stderrs[idx]*self.scale,
                marker = marker,
                label = label
                )
        else:
            l = plt.plot(
                self.x[idx],
                self.values[idx]*self.scale,
                marker = marker,
                label = label
                )

        if self.fit_result is not None:
            l[0].set_linestyle("none")
            idx, *dmy = lim_x(self.fit_x, range_x)
            plt.plot(
                self.fit_x[idx],
                self.fit_y[idx]*self.scale,
                color = l[0].get_color()
                )

    def export(self, name, errorbar = True):

        # build columns names
        self.build_ylabel()
        stderr_label = "stderr"
        if self.unit != "":
            stderr_label += f" [{self.unit}]"
        columns = [self.xlabel, self.ylabel]

        # create data
        data = np.array([
                self.x,
                self.values
            ])
        if errorbar:
            columns.append(stderr_label)
            data = np.vstack((data, self.stderrs))

        # create dataframe
        df = pd.DataFrame(columns = columns, data = data.T)
        df.to_csv(name + ".csv", index = None, header=True)

        # export fit
        if self.fit_x is not None:
            data_fit = np.array([
                self.fit_x,
                self.fit_y
            ])
            df = pd.DataFrame(columns = columns[0:2], data = data_fit.T)
            df.to_csv(name + "_fit.csv", index = None, header=True)

        # export results
        if self.fit_result is not None:
            df_res = display_pars(self.fit_result.params)
            df_res.to_csv(name + "_fit_results.csv", header=True)

    def __add__(self, other):
        return self.operator("add", other)

    def __radd__(self, other):
        return self.operator("radd", other)

    def __sub__(self, other):
        return self.operator("sub", other)

    def __rsub__(self, other):
        return self.operator("rsub", other)

    def __mul__(self, other):
        return self.operator("mul", other)

    def __rmul__(self, other):
        return self.operator("rmul", other)

    def __div__(self, other):
        return self.operator("div", other)

    def __rdiv__(self, other):
        return self.operator("rdiv", other)

    def __truediv__(self, other):
        return self.operator("div", other)

    def __rtruediv__(self, other):
        return self.operator("rdiv", other)

    def __pow__(self, other):
        return self.operator("pow", other)

    def __rpow__(self, other):
        return self.operator("rpow", other)

    def log(self):
        return self.operator("log", other = None)

    def log10(self):
        return self.operator("log10", other = None)

    def exp(self):
        return self.operator("exp", other = None)

    def sin(self):
        return self.operator("sin", other = None)

    def cos(self):
        return self.operator("cos", other = None)

    def tan(self):
        return self.operator("tan", other = None)

    def operator(self, name, other):

        y_res = list()
        for i in range(len(self.y)):
            if isinstance(other, Parameter):
                y = self.y[i].operator(name, other.y[i])
            elif isinstance(other, (int, float)):
                y = self.y[i].operator(name, other)
            y_res.append(y)

        result = Parameter(x = self.x, y = y_res, xlabel = self.xlabel)
        result.model_func = self.model_func

        return result


def calc_C(Q, n, R):

    C = (R*Q)**(1/n)/R
    C.name = "C" + Q.name[1:]
    C.scale = 1e6
    C.unit = r"$\rm\mu$F$\cdot$cm$^{-2}$"

    return C


def calc_MS(C):

    MS = 1/C**2
    MS.name = r"1/%s$^2$"%C.name
    MS.unit = r"F$^{-2}\cdot$cm$^{4}$"
    MS.model_func = f_MS

    return MS
    

def f_MS(x, E_fb, N, eps, f_r, C_dl):

    k = const.k
    q = const.e
    eps_0 = const.epsilon_0
    T = const.zero_Celsius

    y_MS = -2*(x - E_fb - k*T/q)/(q*eps*eps_0*N*f_r**2)
    idx = y_MS <= 0

    y = y_MS + 1/C_dl**2
    y[idx] = 1/C_dl**2

    return y


def calc_DOS(C):

    DOS = C/const.e
    DOS.name = "DOS"
    DOS.unit = r"$eV^{-1} \cdot cm^{-2}$"
    DOS.model_func = f_DOS

    return DOS


def f_DOS(x, N_SS, E_SS, width, slope_bkg, const_bkg):

    gaussian = (N_SS / (np.sqrt(2*np.pi) * width)) * np.exp(-(x-E_SS)**2 / (2*width**2))
    bkg = slope_bkg*x + const_bkg

    y = gaussian + bkg

    return y


def calc_W(MS):

    N = MS.pars["N"]*1e6
    eps = MS.pars["eps"]
    E_fb = MS.pars["E_fb"]
    E = np.linspace(np.min(MS.x), np.max(MS.x), 200)

    eps0 = const.epsilon_0
    q = const.e

    Vbi = E_fb - E
    idx = Vbi/N > 0
    W = E*0
    W[idx] = np.sqrt(2*eps*eps0*Vbi[idx]/(q*N))*1e9

    y = list()
    for val in W:
        y.append(stderr.FloatStd(val, 0))

    W = Parameter(E, y, name = "W", unit = "nm", scale = 1, xlabel = MS.xlabel)

    return W


def figure_layout():

    labels = {
        "omega": r"$\rm \omega\;[rad \cdot s^{-1}]$",
        "real": r"$\rm Re(Z)\;[k\Omega \cdot cm^{2}]$",
        "imag": r"$\rm -Im(Z)\;[k\Omega \cdot cm^{2}]$"
    }
    
    width = 18/2.54 # 18 cm to inches
    fig = plt.figure(figsize=(width, width/2))
    ax = list()
    grid = (2, 2)
    ax.append(plt.subplot2grid(grid, (0, 0)))
    ax.append(plt.subplot2grid(grid, (1, 0)))
    ax.append(plt.subplot2grid(grid, (0, 1), rowspan = 2))
    plt.subplots_adjust(hspace = 0)
    plt.subplots_adjust(wspace = 0.25)

    ax[0].set_ylabel(labels["imag"])
    ax[1].set_ylabel(labels["real"])
    ax[1].set_xlabel(labels["omega"])
    ax[2].set_ylabel(labels["imag"])
    ax[2].set_xlabel(labels["real"])

    ax[0].set_xscale("log")
    ax[1].set_xscale("log")
    ax[0].set_xticks([])
    ax[2].set_aspect('equal', 'box')

    return fig, ax
    

def display_pars(pars):

    index = list()
    columns = ["value", "min", "max", "stderr", "vary"]
    data = list()
    for name in pars:
        index.append(name)
        values = list()
        for attr in columns:
            if attr is "vary" or None:
                values.append(f"{getattr(pars[name], attr)}")
            else:
                values.append(f"{getattr(pars[name], attr):.3g}")
        data.append(values)

    df = pd.DataFrame(index = index, columns = columns, data = data)
    display(df)
    return df

def lim_x(x, range_x):

    # Limit data to range of interest
    if len(range_x) > 0:
        min_x = np.min(range_x)
        max_x = np.max(range_x)
    else:
        min_x = np.min(x)
        max_x = np.max(x)
    idx = (x >= min_x)*(x <= max_x)

    return idx, min_x, max_x


def make_ticks(x):

    min_x = np.min(x)
    max_x = np.max(x)

    # step if 10 intervals
    step = (max_x-min_x)/7

    # find power of ten
    exp10_x = int(np.floor(np.log10(abs(step))))

    # find mantissa
    mant_x = step/10**exp10_x

    # find closest to mantissa in 2,5,10
    step_vals = np.array([1, 2, 5])
    idx = (np.abs(step_vals - mant_x)).argmin()

    # recalculate step
    step_label = step_vals[idx]*10**exp10_x

    # recalculate min and max
    decimals = exp10_x + 1
    decimals = -decimals
    min_x_label = np.round(min_x, decimals = decimals)
    max_x_label = np.round(max_x, decimals = decimals)

    # generate the ticks
    ticks = np.arange(min_x_label, max_x_label + step_label, step_label)
    ticks[np.abs(ticks) < 1e-15] = 0

    return ticks