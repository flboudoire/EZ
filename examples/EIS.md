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


<p align='center'><img src = EIS_files/EIS_2_0.svg
></p>


```python
pars = {
    "R_S":    dict(value = 0.025, vary = False),
    "R_Bulk": dict(value = 25),
    "R_SS":   dict(value = 100),
    "Q_SC":   dict(value = 1e-3),
    "Q_SS":   dict(value = 1e-2),
    "n_SC":   dict(value = 0.9, vary = False),
    "n_SS":   dict(value = 0.8, vary = False)
}
model.plot(
    partial_models=[Q_b/R_b, Q_s/R_s],
    pars=pars,
    range_omega = [1e-3, 1e4]
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
      <th>Q_SC</th>
      <th>Q_SC std</th>
      <th>R_Bulk</th>
      <th>R_Bulk std</th>
      <th>Q_SS</th>
      <th>Q_SS std</th>
      <th>R_SS</th>
      <th>R_SS std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0.725</th>
      <td>0.00226</td>
      <td>2.18e-05</td>
      <td>13.4</td>
      <td>0.151</td>
      <td>0.0132</td>
      <td>0.000166</td>
      <td>26.1</td>
      <td>0.149</td>
    </tr>
    <tr>
      <th>0.745</th>
      <td>0.00213</td>
      <td>3.02e-05</td>
      <td>13.7</td>
      <td>0.199</td>
      <td>0.0142</td>
      <td>0.000215</td>
      <td>30.5</td>
      <td>0.206</td>
    </tr>
    <tr>
      <th>0.765</th>
      <td>0.00208</td>
      <td>3.51e-05</td>
      <td>14.1</td>
      <td>0.219</td>
      <td>0.0154</td>
      <td>0.000235</td>
      <td>35.3</td>
      <td>0.248</td>
    </tr>
    <tr>
      <th>0.785</th>
      <td>0.00204</td>
      <td>3.73e-05</td>
      <td>13.5</td>
      <td>0.21</td>
      <td>0.0155</td>
      <td>0.000192</td>
      <td>43.6</td>
      <td>0.277</td>
    </tr>
    <tr>
      <th>0.805</th>
      <td>0.00207</td>
      <td>6.17e-05</td>
      <td>13</td>
      <td>0.317</td>
      <td>0.0159</td>
      <td>0.000264</td>
      <td>50.1</td>
      <td>0.48</td>
    </tr>
    <tr>
      <th>0.825</th>
      <td>0.00214</td>
      <td>4.25e-05</td>
      <td>13.7</td>
      <td>0.209</td>
      <td>0.0174</td>
      <td>0.000173</td>
      <td>60</td>
      <td>0.424</td>
    </tr>
    <tr>
      <th>0.845</th>
      <td>0.00224</td>
      <td>5.91e-05</td>
      <td>13.2</td>
      <td>0.264</td>
      <td>0.0181</td>
      <td>0.000222</td>
      <td>63.1</td>
      <td>0.602</td>
    </tr>
    <tr>
      <th>0.865</th>
      <td>0.00231</td>
      <td>4.66e-05</td>
      <td>12.6</td>
      <td>0.189</td>
      <td>0.0187</td>
      <td>0.000156</td>
      <td>69.2</td>
      <td>0.513</td>
    </tr>
    <tr>
      <th>0.885</th>
      <td>0.00252</td>
      <td>4.85e-05</td>
      <td>13.1</td>
      <td>0.187</td>
      <td>0.0207</td>
      <td>0.000176</td>
      <td>70.4</td>
      <td>0.595</td>
    </tr>
    <tr>
      <th>0.905</th>
      <td>0.00277</td>
      <td>5.82e-05</td>
      <td>13.1</td>
      <td>0.205</td>
      <td>0.0228</td>
      <td>0.000217</td>
      <td>72.5</td>
      <td>0.783</td>
    </tr>
    <tr>
      <th>0.925</th>
      <td>0.00294</td>
      <td>7.19e-05</td>
      <td>11.8</td>
      <td>0.217</td>
      <td>0.0223</td>
      <td>0.000203</td>
      <td>80.2</td>
      <td>0.925</td>
    </tr>
    <tr>
      <th>0.945</th>
      <td>0.00351</td>
      <td>6.53e-05</td>
      <td>12</td>
      <td>0.179</td>
      <td>0.0244</td>
      <td>0.000182</td>
      <td>81.4</td>
      <td>0.848</td>
    </tr>
    <tr>
      <th>0.965</th>
      <td>0.0041</td>
      <td>6.22e-05</td>
      <td>10.7</td>
      <td>0.14</td>
      <td>0.0233</td>
      <td>0.00011</td>
      <td>102</td>
      <td>0.83</td>
    </tr>
    <tr>
      <th>0.985</th>
      <td>0.0055</td>
      <td>6.83e-05</td>
      <td>10.8</td>
      <td>0.132</td>
      <td>0.0258</td>
      <td>0.000109</td>
      <td>106</td>
      <td>0.913</td>
    </tr>
    <tr>
      <th>1.005</th>
      <td>0.00775</td>
      <td>9.38e-05</td>
      <td>9.88</td>
      <td>0.142</td>
      <td>0.0277</td>
      <td>0.000117</td>
      <td>107</td>
      <td>0.969</td>
    </tr>
    <tr>
      <th>1.025</th>
      <td>0.0102</td>
      <td>0.000134</td>
      <td>9.58</td>
      <td>0.171</td>
      <td>0.031</td>
      <td>0.000163</td>
      <td>97.5</td>
      <td>1.11</td>
    </tr>
    <tr>
      <th>1.045</th>
      <td>0.0112</td>
      <td>0.000179</td>
      <td>9.15</td>
      <td>0.2</td>
      <td>0.0338</td>
      <td>0.000219</td>
      <td>94.9</td>
      <td>1.44</td>
    </tr>
    <tr>
      <th>1.065</th>
      <td>0.0113</td>
      <td>0.000146</td>
      <td>8.69</td>
      <td>0.148</td>
      <td>0.0361</td>
      <td>0.000191</td>
      <td>87.1</td>
      <td>1.06</td>
    </tr>
    <tr>
      <th>1.085</th>
      <td>0.0111</td>
      <td>0.000146</td>
      <td>8.29</td>
      <td>0.136</td>
      <td>0.0376</td>
      <td>0.000191</td>
      <td>91.1</td>
      <td>1.19</td>
    </tr>
    <tr>
      <th>1.105</th>
      <td>0.0109</td>
      <td>0.000137</td>
      <td>8.12</td>
      <td>0.119</td>
      <td>0.0408</td>
      <td>0.000203</td>
      <td>87.1</td>
      <td>1.18</td>
    </tr>
    <tr>
      <th>1.125</th>
      <td>0.0108</td>
      <td>0.000296</td>
      <td>7.79</td>
      <td>0.225</td>
      <td>0.0481</td>
      <td>0.000571</td>
      <td>74.2</td>
      <td>2.42</td>
    </tr>
  </tbody>
</table>
</div>

