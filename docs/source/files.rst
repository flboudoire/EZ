
Files formatting
^^^^^^^^^^^^^^^^

For proper loading the impedance vs frequency response files should be formatted according to the following guidelines; the files should:

- be in the same folder

- be comma-separated values (.csv) text files

- have their file name starting with the potential at which the data is recorded, formatted with an underscore to indicate the decimal point

- contain only one header row and three columns:

  - first column is the frequency in Hertz
  - second column is the real part of the impedance
  - third column is the imaginary part of the impedance

Example files can be found on `Github <https://github.com/flboudoire/EZ/tree/master/examples/data/EIS%20CFO%20pH14%20light>`_.