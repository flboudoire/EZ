Detailed example, fitting with a model equivalent circuit
=========================================================

This example demonstrates how to use the EZ module to fit an equivalent
circuit to an impedance vs angular frequency response, measured
experimentally at different applied bias. In this example
electrochemical impedance spectroscopy (EIS) data is analyzed.

.. raw:: html

   <p id="EC-def">

.. raw:: html

   </p>

Equivalent circuit definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An equivalent circuit can be defined using the classes **R, C, Q** and
**W**. **R** correspond to a resistance, **C** a capacitance, **Q** a
constant phase element and **W** a Warburg element. In this example we
only use **R** and **Q**. We initialize all the elements in the circuit
with a unique label:

.. code:: ipython3

    from EZ.model import Q, R
    
    R_sol = R("S")
    R_b = R("Bulk")
    Q_b = Q("SC")
    R_s = R("SS")
    Q_s = Q("SS")

Then we can define a model equivalent circuit using these elements.
Adding elements is equivalent to connecting them in series and dividing
elements is equivalent to connecting them in parallel. Blocks of
elements can be constituted using parentheses.

.. code:: ipython3

    model = R_sol + Q_b/(R_b + Q_s/R_s)

The circuit can be displayed using its **print** method:

.. code:: ipython3

    model.print()



.. image:: EIS_files/EIS_9_0.svg
  :align: center

.. raw:: html

   <p id="EC-eval">

.. raw:: html

   </p>

Evaluation of the equivalent circuit impedance vs angular frequency behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The EZ module allows to evaluate an equivalent circuit impedance vs
angular frequency characteristics. To this mean we need to initialize
the parameters of the elements (R and Q) defined above. Depending on the
kind of element a different number of parameter has to be initialized. A
resistance for example has one parameter, its resistance value, named
with “R\_” and the label of the considered element. A constant phase
element has two parameters, a pseudo-capacitance (“Q\_” + label) and a
non-ideality factor (“n\_” + label). All the parameters are initialized
using a dictionary whose keys are the parameter name and whose values
are dictionnaries holding the variables used for initialization. These
variables have to contain a value and can also contain additional
information on the parameter that will be used at the fitting step.

.. raw:: html

   <p id="pars-def">

.. raw:: html

   </p>

.. code:: ipython3

    pars = {
        "R_S":    dict( value = 0.025, vary = False ),
        "R_Bulk": dict( value = 10,    min = 0      ),
        "R_SS":   dict( value = 50,    min = 0      ),
        "Q_SC":   dict( value = 1e-3,  min = 0      ),
        "Q_SS":   dict( value = 1e-2,  min = 0      ),
        "n_SC":   dict( value = 0.9,   vary = False ),
        "n_SS":   dict( value = 0.8,   vary = False )
    }

The model impedance vs angular frequency is evaluated and displayed in
Bode and Nyquist plots using its **plot** method. A range of frequencies
can be passed via the **range_omega** argument. Moreover, a list of
additional circuits can be passed via the **partial_models** argument.
It allows to vizualise the contribution of some components to the
overall impedance characteristic. These models impedances are overlayed
in the Bode plots. In the Nyquist plot the regions where a partial
circuit impedance absolute value is larger is highlighted with a
corresponding color. Here for example we use this visualization to show
the parts of the circuit influencing respectively the low and high
frequencies responses, corresponding respectively to the surface and
bulk of an electrode.

.. code:: ipython3

    model.plot(
        partial_models=[Q_b/R_b, Q_s/R_s],
        pars=pars,
        range_omega = [1e-2, 1e4]
    )



.. image:: EIS_files/EIS_16_0.svg
  :align: center

.. raw:: html

   <p id="load-plot">

.. raw:: html

   </p>

Loading and plotting the EIS data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data loading, plotting and fitting is done using an object of class
**Dataset**. This object initialization requires at least the path to
the folder where the files are stored. To be loaded these files should
be formatted properly. The files used in this example can be found
`here <https://github.com/flboudoire/EZ/tree/master/examples/data/EIS%20CFO%20pH14%20light>`__,
and the details on how to format the files for proper loading are
documented `here <files.html>`__. Optional arguments passed in this
example are the pH to convert to RHE and electrode area to normalize the
impedance.

.. code:: ipython3

    from EZ.data import Dataset
    
    ds = Dataset(
        folder="data/EIS CFO pH14 light",
        pH=14,
        area=0.25
    )

In this example we recorded the impedance at frequencies up to 10 MHz.
Since there is no relevant impedance trend above 10 kHz change the
dataset range of frequencies using the **set_freq_range** method. Then
the dataset is plotted using the plot method where the data is
represented as full circles.

.. code:: ipython3

    ds.set_freq_range([1e-10, 1e4])
    ds.plot()



.. image:: EIS_files/EIS_22_0.svg
  :align: center

Fitting and exporting fit results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The fit is performed using the **fit** method. This method requires two
arguments, the model used for the fit, defined here as an `equivalent
circuit <#EC-def>`__, and a dictionary setting the model parameters
initial guess and constraints. In this dictionnary, declared
`previously <#pars-def>`__, we fixed some parameters (**R_S**, **n_SC**
and **n_SS**) by setting the variable **vary** to **False**. We also set
the remaining parameters to be positive by setting the variable **min**
to 0. Maximum values could be used also using the variable **max**.

.. code:: ipython3

    ds.fit(model, pars=pars)

Once the fit is performed, using the **plot** method also displays an
evaluation of the fit as a full line of the same color as the
corresponding data:

.. code:: ipython3

    ds.plot()



.. image:: EIS_files/EIS_27_0.svg
  :align: center

The raw data and corresponding fit can be exported using the **export**
method. The resulting exported files for this example can be consulted
`here <https://github.com/flboudoire/EZ/tree/master/examples/data/EIS%20CFO%20pH14%20light%20-%20analysis>`__.

.. code:: ipython3

    ds.export()

The parameters fitted value and standard error can be exported using the
**export_result** method. The resulting exported files for this example
can be consulted
`here <https://github.com/flboudoire/EZ/tree/master/examples/data/EIS%20CFO%20pH14%20light%20-%20fit%20results>`__.
Passing the argument **show=True** to this method also displays these
values as shown below.

.. code:: ipython3

    ds.export_result(show=True)



.. raw:: html

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



.. raw:: html

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

