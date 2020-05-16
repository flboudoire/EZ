### Model equation definition


```python
from EZ.model import Equation

J_bulk = r"J_e/(1+(1j*omega*tau_e))"
J_surf = r"J_r/(1+(1j*omega*tau_r))"
expression = fr"{J_bulk} + {J_surf}"
model = Equation(expression)
model.print()
```


$\displaystyle \rm Z(\omega) = \frac{J_{e}}{i \omega \tau_{e} + 1} + \frac{J_{r}}{i \omega \tau_{r} + 1}$



```python
pars = {
    "J_e":   dict(value = -0.3),
    "J_r":   dict(value = 0.2),
    "tau_e": dict(value = 2e-4),
    "tau_r": dict(value = 2e-3)
}
model.plot(
    partial_models=[J_bulk, J_surf],
    pars=pars,
    range_omega=[1e1, 1e6]
)
```


<p align='center'><img src = IMPS_files/IMPS_2_0.svg
></p>

### Loading and plotting the IMPS data


```python
from EZ.data import Dataset

ds = Dataset(
    folder="data/IMPS CFO pH14",
    pH=14,
    area=0.25
)
ds.plot()
```


<p align='center'><img src = IMPS_files/IMPS_4_0.svg
></p>

### Fitting and displaying fit results


```python
ds.fit(model, pars=pars)
ds.plot()
```


<p align='center'><img src = IMPS_files/IMPS_6_0.svg
></p>
