### Model equation definition


```python
from EZ.model import Equation

expression = "J_e/(1+(1j*omega*tau_e)) + J_r/(1+(1j*omega*tau_r))"
model = Equation(expression)
model.print()
```


<p>:math:`\displaystyle \rm Z(\omega) = \frac{J_{e}}{i \omega \tau_{e} + 1} + \frac{J_{r}}{i \omega \tau_{r} + 1}`</p>


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


<p align='center'><img src = IMPS_files/IMPS_3_0.svg
></p>
