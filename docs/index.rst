
EZ - Z vs E made easy
=====================

A python module to load, fit and plot impedance spectroscopy data. The datasets contain the impedance evolution as a function of the frequency of a perturbation (e.g. potential or light bias), recorded at different applied potentials. This data can be fitted using a model equivalent circuit or a custom model equation.

.. toctree::

   EIS
   IMPS
   docs

Installation
-----------

Using pip:

.. code:: bash

    pip install EZ

Or download the EZ folder on `Github <https://github.com/flboudoire/EZ>`_ and add it to your python path.

Examples
--------

- :ref:`EIS<EIS>`: Loading, plotting and fitting electrochemical impedance spectroscopy data using an equivalent circuit model.

- :ref:`IMPS<IMPS>`: Loading, plotting and fitting intensity modulated photocurrent spectroscopy data using a model equation.

Dependencies
------------

This code relies on the use of the scipy, numpy, pandas and matplotlib packages. It also uses the `lmfit package <https://lmfit.github.io/lmfit-py/intro.html>`_ (Matt Newville et al., LMFIT: Non-Linear Least-Square Minimization and Curve-Fitting for Python) and the `SchemDraw package <https://schemdraw.readthedocs.io/en/latest/>`_.

License
-------

Licensed under the `MIT License <https://github.com/flboudoire/EZ/blob/master/LICENSE>`_.