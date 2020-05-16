### Model equation definition

$$\rm J(\omega) = \frac{J_e}{\rm 1+i\omega\tau_e} - \frac{J_r}{\rm 1+i\omega\tau_r}$$


```python
def J(omega, J_e, J_r, tau_e, tau_r):
    J_bulk = J_e/(1+(1j*omega*tau_e))
    J_rec = J_r/(1+(1j*omega*tau_r))
    return J_bulk - J_rec
```

### Loading and plotting the IMPS data


```python
from EZ.data import Dataset

ds = Dataset(
    folder = "data/IMPS CFO pH14",
    pH = 14,
    area = 0.25
)
ds.plot()
```


<p align='center'><img src = IMPS_files/IMPS_4_0.svg
></p>
