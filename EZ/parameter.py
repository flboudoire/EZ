import numpy as np
import EZ.stderr as stderr

class Parameter():

    def __init__(self, x, y, name="", unit="", scale=1, xlabel=""):

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

    def fit(self, pars=dict(), range_x=[], print_result=True):

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
                x=self.fit_x,
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
        fig=None,
        range_x=[],
        label="",
        marker=".",
        errorbar=True
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
                self.values[idx] * self.scale,
                yerr=self.stderrs[idx] * self.scale,
                marker=marker,
                label=label
            )
        else:
            l = plt.plot(
                self.x[idx],
                self.values[idx] * self.scale,
                marker=marker,
                label=label
            )

        if self.fit_result is not None:
            l[0].set_linestyle("none")
            idx, *dmy = lim_x(self.fit_x, range_x)
            plt.plot(
                self.fit_x[idx],
                self.fit_y[idx] * self.scale,
                color=l[0].get_color()
            )

    def export(self, name, errorbar=True):

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
        df = pd.DataFrame(columns=columns, data=data.T)
        df.to_csv(name + ".csv", index=None, header=True)

        # export fit
        if self.fit_x is not None:
            data_fit = np.array([
                self.fit_x,
                self.fit_y
            ])
            df = pd.DataFrame(columns=columns[0:2], data=data_fit.T)
            df.to_csv(name + "_fit.csv", index=None, header=True)

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
        return self.operator("log", other=None)

    def log10(self):
        return self.operator("log10", other=None)

    def exp(self):
        return self.operator("exp", other=None)

    def sin(self):
        return self.operator("sin", other=None)

    def cos(self):
        return self.operator("cos", other=None)

    def tan(self):
        return self.operator("tan", other=None)

    def operator(self, name, other):

        y_res = list()
        for i in range(len(self.y)):
            if isinstance(other, Parameter):
                y = self.y[i].operator(name, other.y[i])
            elif isinstance(other, (int, float)):
                y = self.y[i].operator(name, other)
            y_res.append(y)

        result = Parameter(x=self.x, y=y_res, xlabel=self.xlabel)
        result.model_func = self.model_func

        return result


def calc_C(Q, n, R):

    C = (R * Q)**(1 / n) / R
    C.name = "C" + Q.name[1:]
    C.scale = 1e6
    C.unit = r"$\rm\mu$F$\cdot$cm$^{-2}$"

    return C


def calc_MS(C):

    MS = 1 / C**2
    MS.name = r"1/%s$^2$" % C.name
    MS.unit = r"F$^{-2}\cdot$cm$^{4}$"
    MS.model_func = f_MS

    return MS


def f_MS(x, E_fb, N, eps, f_r, C_dl):

    k = const.k
    q = const.e
    eps_0 = const.epsilon_0
    T = const.zero_Celsius

    y_MS = -2 * (x - E_fb - k * T / q) / (q * eps * eps_0 * N * f_r**2)
    idx = y_MS <= 0

    y = y_MS + 1 / C_dl**2
    y[idx] = 1 / C_dl**2

    return y


def calc_DOS(C):

    DOS = C / const.e
    DOS.name = "DOS"
    DOS.unit = r"$eV^{-1} \cdot cm^{-2}$"
    DOS.model_func = f_DOS

    return DOS


def f_DOS(x, N_SS, E_SS, width, slope_bkg, const_bkg):

    gaussian = (N_SS / (np.sqrt(2 * np.pi) * width)) * \
        np.exp(-(x - E_SS)**2 / (2 * width**2))
    bkg = slope_bkg * x + const_bkg

    y = gaussian + bkg

    return y


def calc_W(MS):

    N = MS.pars["N"] * 1e6
    eps = MS.pars["eps"]
    E_fb = MS.pars["E_fb"]
    E = np.linspace(np.min(MS.x), np.max(MS.x), 200)

    eps0 = const.epsilon_0
    q = const.e

    Vbi = E_fb - E
    idx = Vbi / N > 0
    W = E * 0
    W[idx] = np.sqrt(2 * eps * eps0 * Vbi[idx] / (q * N)) * 1e9

    y = list()
    for val in W:
        y.append(stderr.FloatStd(val, 0))

    W = Parameter(E, y, name="W", unit="nm", scale=1, xlabel=MS.xlabel)

    return W


def figure_layout():

    labels = {
        "omega": r"$\rm \omega\;[rad \cdot s^{-1}]$",
        "real": r"$\rm Re(Z)\;[k\Omega \cdot cm^{2}]$",
        "imag": r"$\rm -Im(Z)\;[k\Omega \cdot cm^{2}]$"
    }

    width = 18 / 2.54  # 18 cm to inches
    fig = plt.figure(figsize=(width, width / 2))
    ax = list()
    grid = (2, 2)
    ax.append(plt.subplot2grid(grid, (0, 0)))
    ax.append(plt.subplot2grid(grid, (1, 0)))
    ax.append(plt.subplot2grid(grid, (0, 1), rowspan=2))
    plt.subplots_adjust(hspace=0)
    plt.subplots_adjust(wspace=0.25)

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
            if attr == "vary" or None:
                values.append(f"{getattr(pars[name], attr)}")
            else:
                values.append(f"{getattr(pars[name], attr):.3g}")
        data.append(values)

    df = pd.DataFrame(index=index, columns=columns, data=data)
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
    idx = (x >= min_x) * (x <= max_x)

    return idx, min_x, max_x


def make_ticks(x):

    min_x = np.min(x)
    max_x = np.max(x)

    # step if 10 intervals
    step = (max_x - min_x) / 7

    # find power of ten
    exp10_x = int(np.floor(np.log10(abs(step))))

    # find mantissa
    mant_x = step / 10**exp10_x

    # find closest to mantissa in 2,5,10
    step_vals = np.array([1, 2, 5])
    idx = (np.abs(step_vals - mant_x)).argmin()

    # recalculate step
    step_label = step_vals[idx] * 10**exp10_x

    # recalculate min and max
    decimals = exp10_x + 1
    decimals = -decimals
    min_x_label = np.round(min_x, decimals=decimals)
    max_x_label = np.round(max_x, decimals=decimals)

    # generate the ticks
    ticks = np.arange(min_x_label, max_x_label + step_label, step_label)
    ticks[np.abs(ticks) < 1e-15] = 0

    return ticks
