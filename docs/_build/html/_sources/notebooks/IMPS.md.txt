### Model equation definition


```python
from EZ.model import Equation

J_bulk = r"J_e/(1+(1j*omega*tau_e))"
J_surf = r"J_r/(1+(1j*omega*tau_r))"
expression = fr"{J_bulk} + {J_surf}"
model = Equation(expression)
model.print()
```


:math:`\displaystyle \rm Z(\omega) = \frac{J_{e}}{i \omega \tau_{e} + 1} + \frac{J_{r}}{i \omega \tau_{r} + 1}`



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


```python
ds.print_result()
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class = 'docutils'>
  <thead>
    <tr style="text-align: right;">
      <th>E [V vs RHE]</th>
      <th>J_e</th>
      <th>J_e std</th>
      <th>tau_r</th>
      <th>tau_r std</th>
      <th>tau_e</th>
      <th>tau_e std</th>
      <th>J_r</th>
      <th>J_r std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1.425</th>
      <td>-2.42</td>
      <td>0.0131</td>
      <td>0.000581</td>
      <td>6.58e-06</td>
      <td>3.48e-05</td>
      <td>3.56e-07</td>
      <td>2.38</td>
      <td>0.0139</td>
    </tr>
    <tr>
      <th>1.525</th>
      <td>-2.3</td>
      <td>0.0114</td>
      <td>0.000416</td>
      <td>4.11e-06</td>
      <td>2.74e-05</td>
      <td>2.48e-07</td>
      <td>2.26</td>
      <td>0.0118</td>
    </tr>
    <tr>
      <th>1.625</th>
      <td>-1.16</td>
      <td>0.00741</td>
      <td>0.000332</td>
      <td>4.25e-06</td>
      <td>2.19e-05</td>
      <td>2.58e-07</td>
      <td>1.13</td>
      <td>0.00768</td>
    </tr>
    <tr>
      <th>1.725</th>
      <td>-0.135</td>
      <td>0.0012</td>
      <td>0.000229</td>
      <td>3.63e-06</td>
      <td>2.16e-05</td>
      <td>3e-07</td>
      <td>0.132</td>
      <td>0.0012</td>
    </tr>
    <tr>
      <th>1.825</th>
      <td>-0.00416</td>
      <td>0.000101</td>
      <td>0.000151</td>
      <td>7.19e-06</td>
      <td>1.57e-05</td>
      <td>5.59e-07</td>
      <td>0.00399</td>
      <td>9.95e-05</td>
    </tr>
  </tbody>
</table>
</div>

