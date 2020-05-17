import numpy as np


def param2floatstd(p=None):
    if p is not None:
        result = FloatStd(value=p.value, stderr=p.stderr)
    else:
        result = None
    return result


def array2floatstd(a=None):
    if a is not None:
        result = FloatStd(value=np.mean(a), stderr=np.std(a))
    else:
        result = None
    return result


class FloatStd:
    def __init__(self, value=0., stderr=0.):
        self.value = value
        self.stderr = stderr

    def __add__(self, other):
        return self.operator("add", other)

    def __radd__(self, other):
        return self.operator("radd", other)

    def __sub__(self, other):
        return self.operator("sub", other)

    def __rsub__(self, other):
        return self.operator("rsub", other)

    def __mul__(self, other):
        return self.operator("mul", other)

    def __rmul__(self, other):
        return self.operator("rmul", other)

    def __div__(self, other):
        return self.operator("div", other)

    def __rdiv__(self, other):
        return self.operator("rdiv", other)

    def __truediv__(self, other):
        return self.operator("div", other)

    def __rtruediv__(self, other):
        return self.operator("rdiv", other)

    def __pow__(self, other):
        return self.operator("pow", other)

    def __rpow__(self, other):
        return self.operator("rpow", other)

    def log(self):
        return self.operator("log", other=None)

    def log10(self):
        return self.operator("log10", other=None)

    def exp(self):
        return self.operator("exp", other=None)

    def sin(self):
        return self.operator("sin", other=None)

    def cos(self):
        return self.operator("cos", other=None)

    def tan(self):
        return self.operator("tan", other=None)

    def operator(self, name, other):

        # Calculations of stderr assuming uncorrelated variables
        # Equations from https://en.wikipedia.org/wiki/Propagation_of_uncertainty

        A = self.value
        sA = self.stderr

        if isinstance(other, FloatStd):
            B = other.value
            sB = other.stderr
        elif isinstance(other, (int, float)):
            B = other
            sB = 0
        elif other is None and name in ["log", "log10", "exp", "sin", "cos", "tan"]:
            pass
        else:
            return NotImplemented

        if name == "sub":
            F = A - B
        elif name == "rsub":
            F = B - A
        elif name == "div":
            F = A / B
        elif name == "rdiv":
            F = B / A
        elif name == "pow":
            F = A**B
        elif name == "rpow":
            F = B**A
        elif name == "add" or name == "radd":
            F = A + B
        elif name == "mul" or name == "rmul":
            F = A * B
        elif name == "log":
            F = np.log(A)
        elif name == "log10":
            F = np.log10(A)
        elif name == "exp":
            F = np.exp(A)
        elif name == "sin":
            F = np.sin(A)
        elif name == "cos":
            F = np.cos(A)
        elif name == "tan":
            F = np.tan(A)

        if name == "sub" or name == "rsub" or name == "add" or name == "radd":
            sF = np.sqrt(sA**2 + sB**2)
        elif name == "div" or name == "rdiv" or name == "mul" or name == "rmul":
            sF = np.abs(F) * np.sqrt((sA / A)**2 + (sB / B)**2)
        elif name == "pow":
            sF = np.abs(F) * np.sqrt((B / A * sA)**2 + (np.log(A) * sB)**2)
        elif name == "rpow":
            sF = np.abs(F) * np.sqrt((A / B * sB)**2 + (np.log(B) * sA)**2)
        elif name == "log":
            sF = np.abs(sA / A)
        elif name == "log10":
            sF = np.abs(sA / (A * np.log(10)))
        elif name == "exp":
            sF = np.exp(sA)
        elif name == "sin":
            sF = np.sin(sA)
        elif name == "cos":
            sF = np.cos(sA)
        elif name == "tan":
            sF = np.tan(sA)

        result = FloatStd(value=F, stderr=sF)

        return result
