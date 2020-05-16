This example showcases the use of the EZ module in order to fit electrochemical impedance spectroscopy data recorded at different potential using an equivalent circuit.

### Equivalent circuit definition


```python
from EZ import EC

R_sol = EC.R("S")
R_b = EC.R("Bulk")
Q_b = EC.Q("SC")
R_s = EC.R("SS")
Q_s = EC.Q("SS")

circ = R_sol + Q_b/(R_b + Q_s/R_s)
circ.print()
```


<p align='center'><img src = EIS_files/EIS_2_0.svg
></p>


```python
pars = {
    "R_S": dict(value = 0.025, vary = False),
    "R_Bulk": dict(value = 2),
    "R_SS": dict(value = 10),
    "Q_SC": dict(value = 1e-2),
    "Q_SS": dict(value = 1e-1),
    "n_SC": dict(value = 0.9, vary = False),
    "n_SS": dict(value = 0.8, vary = False)
}
circ.plot(
    partial_circuits = [Q_b/R_b, Q_s/R_s],
    pars = pars
)
```


<p align='center'><img src = EIS_files/EIS_3_0.svg
></p>

### Loading and plotting the EIS data


```python
from EZ.data import Dataset

ds = Dataset(
    folder = "data/EIS CFO pH14 light",
    pH = 14,
    area = 0.25
)
ds.set_freq_range([-np.inf, 1e4])
ds.plot()
```


<p align='center'><img src = EIS_files/EIS_5_0.svg
></p>

### Fitting and displaying fit results


```python
ds.fit(circ, pars = pars)
ds.plot()
```


<p align='center'><img src = EIS_files/EIS_7_0.svg
></p>
