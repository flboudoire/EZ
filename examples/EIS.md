This example showcases the use of the EZ module in order to fit electrochemical impedance spectroscopy data recorded at different potential using an equivalent circuit.

### Equivalent circuit definition


```python
from EZ import EC

R_sol = EC.R("S")
R_b = EC.R("bulk")
Q_b = EC.Q("bulk")
R_s = EC.R("surf")
Q_s = EC.Q("surf")

circ = R_sol + Q_b/(R_b + Q_s/R_s)
circ.print()

circ_b = Q_b/R_b
circ_s = Q_s/R_s
```


<p align='center'><img src = EIS_files/EIS_2_0.svg
></p>

### Loading and plotting the EIS data


```python
ds = Dataset(
    file = directory + file,
    pH = 7,
    N_points_min = 20,
    range_omega = [-np.inf, 1e5]
)

ds.plot(partial_circuits = [RC_b, RC_s])
```

### Fitting and displaying fit results


```python
ds.fit(EC, pars = pars)
```
