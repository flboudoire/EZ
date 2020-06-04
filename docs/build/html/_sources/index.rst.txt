
EZ - Z vs E made easy
=====================

A python module to load, fit and plot impedance spectroscopy data. The datasets contain the impedance evolution as a function of the frequency of a perturbation (e.g. potential or light bias), recorded at different applied potentials. This data can be fitted using a model equivalent circuit or a custom model equation.

Installation
------------

Using pip:

.. code:: bash

    pip install echem-EZ

Or download the EZ folder on `Github <https://github.com/flboudoire/EZ>`_ and add it to your python path.

Examples
--------

- :ref:`Detailed example, fitting with a model equivalent circuit<Detailed example, fitting with a model equivalent circuit>`: Loading, plotting and fitting electrochemical impedance spectroscopy data using an equivalent circuit model.

- :ref:`Follow up example, fitting with a model equation<Follow up example, fitting with a model equation>`: Loading, plotting and fitting intensity modulated photocurrent spectroscopy data using a model equation.

Dependencies
------------

This code relies on the use of the sympy, scipy, numpy, pandas and matplotlib packages. It also uses the `lmfit package <https://lmfit.github.io/lmfit-py/intro.html>`_ (Matt Newville et al., LMFIT: Non-Linear Least-Square Minimization and Curve-Fitting for Python) and the `SchemDraw package <https://schemdraw.readthedocs.io/en/latest/>`_.

License
-------

Licensed under the `MIT License <https://github.com/flboudoire/EZ/blob/master/LICENSE>`_.

Contents
--------

.. toctree::

   EIS
   IMPS
   files