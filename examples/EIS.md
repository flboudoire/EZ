This example showcases the use of the EZ module in order to fit electrochemical impedance spectroscopy data recorded at different potential using an equivalent circuit.

### Equivalent circuit definition


```python
from EZ.model import Q, R

R_sol = R("S")
R_b = R("Bulk")
Q_b = Q("SC")
R_s = R("SS")
Q_s = Q("SS")

model = R_sol + Q_b/(R_b + Q_s/R_s)
model.print()
```

    /usr/lib/python3.8/site-packages/EZ/data.py:256: SyntaxWarning: "is" with a literal. Did you mean "=="?
      if attr is "vary" or None:



<p align='center'><img src = EIS_files/EIS_2_1.svg
></p>


```python
pars = {
    "R_S":    dict(value = 0.025, vary = False),
    "R_Bulk": dict(value = 2),
    "R_SS":   dict(value = 10),
    "Q_SC":   dict(value = 1e-2),
    "Q_SS":   dict(value = 1e-1),
    "n_SC":   dict(value = 0.9, vary = False),
    "n_SS":   dict(value = 0.8, vary = False)
}
model.plot(
    partial_models=[Q_b/R_b, Q_s/R_s],
    pars=pars
)
```


<p align='center'><img src = EIS_files/EIS_3_0.svg
></p>

### Loading and plotting the EIS data


```python
from EZ.data import Dataset

ds = Dataset(
    folder="data/EIS CFO pH14 light",
    pH=14,
    area=0.25
)
ds.set_freq_range([-np.inf, 1e4])
ds.plot()
```


<p align='center'><img src = EIS_files/EIS_5_0.svg
></p>

### Fitting and displaying fit results


```python
ds.fit(model, pars=pars)
ds.plot()
```


<p align='center'><img src = EIS_files/EIS_7_0.svg
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
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>value (fixed)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>R_S</th>
      <td>0.025</td>
    </tr>
    <tr>
      <th>n_SC</th>
      <td>0.900</td>
    </tr>
    <tr>
      <th>n_SS</th>
      <td>0.800</td>
    </tr>
  </tbody>
</table>
</div>



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
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>E [V vs RHE]</th>
      <th>Q_SC value</th>
      <th>Q_SC stderr</th>
      <th>R_Bulk value</th>
      <th>R_Bulk stderr</th>
      <th>Q_SS value</th>
      <th>Q_SS stderr</th>
      <th>R_SS value</th>
      <th>R_SS stderr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0.725</th>
      <td>0.00921</td>
      <td>7.52e-05</td>
      <td>3.36</td>
      <td>0.0324</td>
      <td>0.0533</td>
      <td>0.000576</td>
      <td>6.5</td>
      <td>0.0318</td>
    </tr>
    <tr>
      <th>0.745</th>
      <td>0.00867</td>
      <td>0.000115</td>
      <td>3.44</td>
      <td>0.0474</td>
      <td>0.0571</td>
      <td>0.000823</td>
      <td>7.59</td>
      <td>0.0488</td>
    </tr>
    <tr>
      <th>0.765</th>
      <td>0.00846</td>
      <td>0.000137</td>
      <td>3.53</td>
      <td>0.0534</td>
      <td>0.0618</td>
      <td>0.000917</td>
      <td>8.81</td>
      <td>0.06</td>
    </tr>
    <tr>
      <th>0.785</th>
      <td>0.00828</td>
      <td>0.000147</td>
      <td>3.38</td>
      <td>0.0515</td>
      <td>0.0623</td>
      <td>0.000751</td>
      <td>10.9</td>
      <td>0.0673</td>
    </tr>
    <tr>
      <th>0.805</th>
      <td>0.0084</td>
      <td>0.000249</td>
      <td>3.26</td>
      <td>0.0796</td>
      <td>0.0635</td>
      <td>0.00106</td>
      <td>12.5</td>
      <td>0.119</td>
    </tr>
    <tr>
      <th>0.825</th>
      <td>0.0087</td>
      <td>0.000168</td>
      <td>3.42</td>
      <td>0.0514</td>
      <td>0.0696</td>
      <td>0.000679</td>
      <td>15</td>
      <td>0.103</td>
    </tr>
    <tr>
      <th>0.845</th>
      <td>0.0091</td>
      <td>0.000237</td>
      <td>3.29</td>
      <td>0.0658</td>
      <td>0.0726</td>
      <td>0.000883</td>
      <td>15.8</td>
      <td>0.149</td>
    </tr>
    <tr>
      <th>0.865</th>
      <td>0.00941</td>
      <td>0.000185</td>
      <td>3.16</td>
      <td>0.0466</td>
      <td>0.0749</td>
      <td>0.000609</td>
      <td>17.3</td>
      <td>0.125</td>
    </tr>
    <tr>
      <th>0.885</th>
      <td>0.0102</td>
      <td>0.000192</td>
      <td>3.27</td>
      <td>0.046</td>
      <td>0.0829</td>
      <td>0.000687</td>
      <td>17.6</td>
      <td>0.145</td>
    </tr>
    <tr>
      <th>0.905</th>
      <td>0.0113</td>
      <td>0.000231</td>
      <td>3.28</td>
      <td>0.0506</td>
      <td>0.0914</td>
      <td>0.00085</td>
      <td>18.1</td>
      <td>0.191</td>
    </tr>
    <tr>
      <th>0.925</th>
      <td>0.012</td>
      <td>0.000289</td>
      <td>2.95</td>
      <td>0.0542</td>
      <td>0.0892</td>
      <td>0.000804</td>
      <td>20</td>
      <td>0.228</td>
    </tr>
    <tr>
      <th>0.945</th>
      <td>0.0143</td>
      <td>0.000258</td>
      <td>3.01</td>
      <td>0.044</td>
      <td>0.0974</td>
      <td>0.00071</td>
      <td>20.3</td>
      <td>0.206</td>
    </tr>
    <tr>
      <th>0.965</th>
      <td>0.0167</td>
      <td>0.000241</td>
      <td>2.68</td>
      <td>0.0338</td>
      <td>0.0929</td>
      <td>0.000419</td>
      <td>25.4</td>
      <td>0.197</td>
    </tr>
    <tr>
      <th>0.985</th>
      <td>0.0225</td>
      <td>0.000248</td>
      <td>2.7</td>
      <td>0.0299</td>
      <td>0.103</td>
      <td>0.000391</td>
      <td>26.6</td>
      <td>0.204</td>
    </tr>
    <tr>
      <th>1.005</th>
      <td>0.0317</td>
      <td>0.000306</td>
      <td>2.49</td>
      <td>0.0291</td>
      <td>0.11</td>
      <td>0.000378</td>
      <td>26.6</td>
      <td>0.194</td>
    </tr>
    <tr>
      <th>1.025</th>
      <td>0.0419</td>
      <td>0.000421</td>
      <td>2.43</td>
      <td>0.034</td>
      <td>0.124</td>
      <td>0.000507</td>
      <td>24.4</td>
      <td>0.215</td>
    </tr>
    <tr>
      <th>1.045</th>
      <td>0.0462</td>
      <td>0.00061</td>
      <td>2.32</td>
      <td>0.0432</td>
      <td>0.135</td>
      <td>0.000744</td>
      <td>23.7</td>
      <td>0.304</td>
    </tr>
    <tr>
      <th>1.065</th>
      <td>0.0467</td>
      <td>0.000411</td>
      <td>2.21</td>
      <td>0.0263</td>
      <td>0.144</td>
      <td>0.000533</td>
      <td>21.8</td>
      <td>0.184</td>
    </tr>
    <tr>
      <th>1.085</th>
      <td>0.0458</td>
      <td>0.00044</td>
      <td>2.1</td>
      <td>0.0259</td>
      <td>0.15</td>
      <td>0.000568</td>
      <td>22.8</td>
      <td>0.22</td>
    </tr>
    <tr>
      <th>1.105</th>
      <td>0.045</td>
      <td>0.000399</td>
      <td>2.05</td>
      <td>0.0218</td>
      <td>0.163</td>
      <td>0.000581</td>
      <td>21.8</td>
      <td>0.21</td>
    </tr>
    <tr>
      <th>1.125</th>
      <td>0.0446</td>
      <td>0.00114</td>
      <td>1.96</td>
      <td>0.0541</td>
      <td>0.192</td>
      <td>0.00216</td>
      <td>18.6</td>
      <td>0.572</td>
    </tr>
  </tbody>
</table>
</div>

