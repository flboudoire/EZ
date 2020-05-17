import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import lmfit
import glob
from collections import OrderedDict
from IPython.display import display, HTML

from EZ.parameter import Parameter
import EZ.stderr as stderr


class Data():

    def __init__(self, file_path):

        self.file_path = file_path
        self.model = None
        self.load()

    def load(self):

        raw_data = np.loadtxt(self.file_path, skiprows=1, delimiter=",")
        self.freq = raw_data[:, 0]
        self.omega = 2 * np.pi * self.freq
        self.Z = raw_data[:, 1] + 1j * raw_data[:, 2]

    def set_freq_range(self, range_freq):

        idx = (self.omega >= min(range_freq)) * (self.omega <= max(range_freq))
        self.freq = self.freq[idx]
        self.omega = self.omega[idx]
        self.Z = self.Z[idx]

    def plot(
        self,
        axes=None,
        color="C0",
        partial_models=None):

        if axes is None:
            fig, axes = figure_layout()

        style = dict(
            marker=".",
            linestyle="none",
            markersize=2,
            color=color
        )
        axes[0].plot(self.omega, -self.Z.imag, **style)
        axes[1].plot(self.omega, self.Z.real, **style)
        axes[2].plot(self.Z.real, -self.Z.imag, **style)

        if self.model is not None:
            self.model.plot(
                axes=axes,
                pars=self.fit_result.params,
                color=color,
                range_omega=[np.min(self.omega), np.max(self.omega)],
                partial_models=partial_models
            )

    def fit(self, model=None, pars=dict()):

        self.model = model
        self.fit_result = model.fit(
            self.omega,
            self.Z,
            pars=pars
        )
        self.pars = self.fit_result.params


class Dataset():

    def __init__(
        self,
        folder,
        pH=None,
        area=1.,
        ref=("Ag/AgCl", 0)):

        self.folder = folder
        self.pH = pH
        self.area = area
        if self.pH is None:
            self.E_label = fr"E [V vs {ref[0]}]"
        else:
            self.E_label = fr"E [V vs RHE]"
        self.load()

    def load(self):

        self.datas = OrderedDict()

        for file_path in glob.glob(fr'{self.folder}/*.csv'):
            E = float(
                file_path
                .split("/")[-1]
                .split(" ")[0]
                .replace("_", ".")
            )
            if self.pH is None:
                E = {k: v for k, v in sorted(self.datas.items())}
            else:
                E += 0.1976 + 0.0591 * self.pH
            E = np.round(E, 3)
            self.datas[E] = Data(file_path)

        self.datas = {k: v for k, v in sorted(self.datas.items())}
        self.Es = [E for E in self.datas]

    def data(self, i):
        return list(self.datas.values())[i]

    def set_freq_range(self, range_freq):
        for E in self.datas:
            self.datas[E].set_freq_range(range_freq)

    def fit(
        self,
        model,
        pars=dict(),
        consecutive=True):

        for i, E in enumerate(self.datas):
            if i > 0 and consecutive:
                prev_pars = list(self.datas.values())[i - 1].pars
                init_pars = dict()
                for key in prev_pars:
                    p = prev_pars[key]
                    param_dict = dict(
                        value=p.value,
                        vary=p.vary,
                        min=p.min,
                        max=p.max
                    )
                    init_pars.update({key: param_dict})
            else:
                init_pars = pars

            self.datas[E].fit(
                model=model,
                pars=init_pars
            )

    def plot(
        self,
        axes=None,
        print_result=True,
        partial_models=None):

        if axes is None:
            fig, axes = figure_layout()

        cmap = plt.get_cmap("rainbow")
        for E in self.datas:
            norm_E = (E - min(self.Es)) / (max(self.Es) - min(self.Es))
            color = cmap(norm_E)
            self.datas[E].plot(
                axes=axes,
                color=color
            )

        # Hack to get colorbar for plot in matplotlib
        Z = [[0, 0], [0, 0]]
        Es = np.linspace(min(self.Es), max(self.Es), 150)
        dmy = axes[2].contourf(Z, Es, cmap=cmap)
        plt.colorbar(
            dmy,
            orientation="horizontal",
            ticks=make_ticks(self.Es),
            label=self.E_label,
            pad=0.17
        )

    def print_result(self, folder = None):

        columns = ["value", "stderr"]
        fit_results = OrderedDict()
        fit_results_fixed = OrderedDict()
        for i, E in enumerate(self.datas):
            row = list()
            pars = self.datas[E].pars
            for name in pars:
                if pars[name].vary:
                    if name not in fit_results: fit_results[name] = list()
                    values = [f"{getattr(pars[name], attr):.3g}" for attr in columns]
                    fit_results[name].append(values)
                else:
                    fit_results_fixed[name] = pars[name].value

        df = pd.DataFrame(
            index = [name for name in fit_results_fixed],
            columns = ["value (fixed)"],
            data = fit_results_fixed.values())
        display(df)

        cols = [fr"{name} {attr}" for name in fit_results for attr in columns]
        df = pd.DataFrame(
            index = self.datas.keys(),
            columns = cols,
            data = np.hstack([v for v in fit_results.values()]))
        df.columns.name = self.E_label
        display(df)


def figure_layout():

    labels = {
        "omega": r"$\omega$ [rad $\cdot$ s$^{-1}$]",
        "real": r"Re(Z)",
        "imag": r"-Im(Z)"
    }

    width = 16 / 2.54  # 18 cm to inches
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

def make_ticks(x):

    # step if 7 intervals
    step = (max(x) - min(x)) / 7

    # find power of ten
    exp10_x = int(np.floor(np.log10(abs(step))))

    # find mantissa
    mant_x = step / 10**exp10_x

    # find closest to mantissa in 2,5,10
    step_vals = np.array([2, 5, 10])
    idx = (np.abs(step_vals - mant_x)).argmin()

    # recalculate step
    step_label = step_vals[idx] * 10**exp10_x

    # recalculate min and max
    decimals = exp10_x + 1
    decimals = -decimals
    min_x_label = np.round(min(x), decimals=decimals)
    max_x_label = np.round(max(x), decimals=decimals)

    # generate the ticks
    ticks = np.arange(min_x_label, max_x_label + step_label, step_label)
    ticks[np.abs(ticks) < 1e-15] = 0

    return ticks
