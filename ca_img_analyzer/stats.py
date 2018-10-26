import numpy as np
from scipy import integrate


def auc(df, column, rule="trapezoid"):
    """
    this function calculates the area under the
    curve for a certain `column' in a dataframe `df'
    ------------------------------------
    parameters:
        df     = input data frame
        column = column in `df' to use for
                 calculations
        rule   = 'trapezoidal' or 'simpson'
    """
    arr = np.array(df[column])

    # AUC using the trapezoidal rule
    if rule is "trapezoidal":
        area = np.trapz(arr, dx=5)
        print("area =", area)

    # Compute the area using the composite Simpson's rule.
    if rule is "simpson":
        area = integrate.simps(arr, dx=5)
        print("area =", area)
