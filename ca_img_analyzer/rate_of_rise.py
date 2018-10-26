# rate_of_rise.py is part of the `ca_img_analyzer' package:
# github.com/DanielSchuette/ca_img_analyzer
#
# this code is MIT licensed
#
# if you find a bug or want to contribute, please
# use the GitHub repository or write an email:
# d.schuette(at)online.de
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Workbook(object):
    """
    class 'Workbook' holds data of (potentially multiple)
    Excel spread sheets and comprises methods to modify/
    manipulate this data; Workbook does not inherit from
    anything but object.
    The following methods can be called on Workbook:
        - calc_derivative()
        - plot_derivatives()
        - get_max_derivatives()
        - plot_max_derivatives()
        - concat_covslips()
    """

    def __init__(self,
                 path,
                 h=1,
                 order=None,
                 kind="box",
                 plot_style=None,
                 verbose=False,
                 debug=False):
        """
        takes a valid file path to a .xlsx file and reads it in;
        also iterates over the different sheets in that workbook
        and appends their names to a newly initialized list.
        -----------------------------
        parameters:
            TODO!
        """
        # read the excel workbook in
        self.raw_data = pd.read_excel(path, sheet_name=None)

        # append individual names to a list of sheet names
        self.sheet_names = []
        for idx, name in enumerate(self.raw_data):
            if verbose:
                print("number {}: {}".format(idx + 1, name))
            self.sheet_names.append(name)
        if len(self.sheet_names) < 2:
            print("""did not get more than one spread sheet to read;
                     is that correct?""")

        # create empty list to hold dataframes with derivates
        # and various data formats
        self.derivative_df_list = []
        self.derivatives_table = pd.DataFrame()
        self.derivatives_compiled = self.derivatives_table.copy()

        # shorten input for debugging purposes
        if debug:
            self.sheet_names = self.sheet_names[0:3]

        # assign a value for 'h'
        self.h = h

        # assign a value for 'order', 'plot_style' and 'kind'
        self.order = order
        self.plot_style = plot_style
        self.kind = kind

    def calc_derivative(self, no_rows=None, verbose=False):
        """
        calculates derivatives and creates a class member
        'derivative_df_list' that holds all dataframes with the
        respective derivatives and that can be used for plotting.
        """
        # iterate over spread sheets (i.e. dataframes),
        # calculate derivatives and append results to the
        # newly created list of derivate-holding dataframes
        for name in self.sheet_names:
            __df = pd.DataFrame()
            # create a temporary dataframe
            # consistently and reliably skipping a sheet is
            # difficult to implement; just don't do it!
            if name != "Sheet1":
                __df = self.raw_data[name]
                if verbose:
                    print("created temporary {} with dim: {}".format(
                        type(__df), __df.shape))
            else:
                print("skipped sheet: {}".format(name))
                continue

            # loop over columns of temporary dataframe and calculate
            # derivates that are then copy to new dataframe and appended
            # to a list of dataframes for further use if rows=None,
            # use all rows for calculations; if a tuple is given,
            # use the specified starting and end point, for example
            # (100, 200) to start at row 100 and stop at row 200
            if not no_rows:
                rows = (0, __df.shape[0])
                if verbose:
                    print("rows: ", rows[0], rows[1])
            else:
                rows = no_rows
            cols = __df.shape[1]
            __derivative_df = pd.DataFrame()

            # iterate over columns
            for i in range(cols):
                if verbose:
                    print(i)
                __derivative_list = []

                # iterate over rows
                for j in range(rows[0], rows[1]):
                    if j == 0:
                        __derivative_list.append(
                            ((__df.iloc[(j + 1), i]) -
                             (__df.iloc[j, i])) / (2 * self.h))
                    elif j == (rows[1] - 1):
                        __derivative_list.append(
                            ((__df.iloc[j, i]) -
                             (__df.iloc[(j - 1), i])) / (2 * self.h))
                    else:
                        if verbose:
                            print(j)
                        __derivative_list.append(
                            ((__df.iloc[(j + 1), i]) -
                             (__df.iloc[(j - 1), i])) / (2 * self.h))

                # for first col, create new data frame;
                # otherwise, concatenate two list and dataframe
                if __derivative_df.empty:
                    if verbose:
                        print("create new tmp df")
                    __derivative_df = pd.DataFrame(__derivative_list)
                else:
                    if verbose:
                        print("append to tmp df")
                    __derivative_df = pd.concat(
                        [__derivative_df,
                         pd.DataFrame(__derivative_list)],
                        axis=1)

            # append temporary data frame to a list of
            # derivative-holding dataframes
            if verbose:
                print(__derivative_df)
            self.derivative_df_list.append(__derivative_df)

    def plot_derivatives(self, spread_sheet=None):
        """
        plots derivatives (optionally, only for a certain spread sheet);
        call only after calling 'calc_derivatives()'
        """
        # check if derivatives are already calculated
        if not self.derivative_df_list:
            print("call 'calc_derivatives()' first!")
            return

        # plot derivates
        for idx, _df in enumerate(self.derivative_df_list):
            # names are not save! they rely on an ordered input!
            # try to avoid empty sheets like 'Sheet1', especially
            # if that empty sheet is not the first sheet
            # (i.e 'idx+1')!
            print("{} max value: {},\n\t\tmean value: {}, median: {}".format(
                self.sheet_names[idx], np.max(_df.max()), np.mean(_df.max()),
                np.median(_df.max())))

            # disable matplotlib.pyplot warning
            plt.rcParams.update({'figure.max_open_warning': 0})

            # create a plot
            _df.plot(legend=False, title=self.sheet_names[idx])

    def get_max_derivatives(self, limit=None):
        """
        get_max_derivatives pulls column-wise max derivatives out
        of self.derivative_df_list and puts them into class member
        self.derivatives_table to make plotting easier:
        #################################
        ## max_derivative ## coverslip ##
        ## 0.124          ## wt        ##
        ## 0.634          ## wt        ##
        ## ...            ## ...       ##
        #################################
        """
        # check if derivates are already calculated
        if not self.derivative_df_list:
            print("call 'calc_derivates()' first!")
            return

        # iterate over derivative dataframes and return their
        # column-wise max values in a new 'long' dataframe
        _df = pd.DataFrame()
        for idx, _tmp in enumerate(self.derivative_df_list):
            _names_list = []
            for i in range(_tmp.shape[1]):
                _names_list.append(self.sheet_names[(idx)])
            if limit:
                _dict = {
                    "max_derivative": _tmp.max()[_tmp.max() > limit],
                    "coverslip":
                    _names_list[0:np.sum(list(_tmp.max() > limit))]
                }
            else:
                _dict = {
                    "max_derivative": _tmp.max(),
                    "coverslip": _names_list
                }
            if idx == 0:
                _df = pd.DataFrame(_dict)
            else:
                _df = pd.concat([_df, pd.DataFrame(_dict)], axis=0)

        # write long dataframe with max derivatives to data frame
        self.derivatives_table = _df

    def plot_max_derivatives(self, column=None):
        """
        plot_max_derivatives plots the maximum derivatives
        per column (== cell) across multiple dataframes
        (== spread sheet) in the input workbook; seaborn deprication
        warning of factor plot can be ignored for now, because boxplots
        don't work as nicely with catplot as compared to factorplot.
        """
        # check if data frame of max derivatives is already calculated
        if self.derivatives_table.empty and self.derivatives_compiled.empty:
            print("""call 'calc_derivates()',
                     'concat_covslip()' and 'get_max_derivatives()' first!""")
            return
        if not column:
            print("provide a valid column id")
            return
        if self.kind is "point":
            fp = sns.catplot(
                x=column,
                y="max_derivative",
                data=self.derivatives_compiled,
                height=8,
                aspect=1.8,
                order=self.order,
                s=15)
        elif self.kind is "box":
            fp = sns.catplot(
                x=column,
                y="max_derivative",
                data=self.derivatives_compiled,
                kind=self.kind,
                height=8,
                aspect=1.8,
                saturation=0.5,
                fliersize=8,
                linewidth=4,
                width=0.7,
                order=self.order)
        else:
            fp = sns.catplot(
                x=column,
                y="max_derivative",
                data=self.derivatives_compiled,
                kind=self.kind,
                height=8,
                aspect=1.8,
                saturation=0.5,
                linewidth=4,
                order=self.order,
                ci=95)

        # modify plot aesthetics
        fp.despine(top=False, right=False)
        plt.grid(b=True, which="major")
        plt.xlabel("Coverslip Labels", fontsize=20)
        plt.ylabel("Maximum Derivatives", fontsize=20)
        plt.xticks(fontsize=16, rotation=90)
        plt.yticks(fontsize=16)
        plt.title(
            "Maximum Derivates Across Multiple Cells and Coverslips",
            fontsize=24)

    def concat_covslips(self, exclude=False, threshold=(0.4, 0.6)):
        """
        concat_covslips concatenates control and wildtype coverslips
        that were stimulated with different concentrations of agonist;
        it uses regex to identify concentrations and genotypes and
        declares a new class member self.derivatives_compiled that is a
        long format dataframe similar to self.derivatives_table but with
        an additional column that contains new names:
        ###################################################
        ## max_derivative ## coverslip ## coverslip type ##
        ## 0.124          ## wt1 30µM  ## wt 30µM        ##
        ## 0.634          ## wt2 10µM  ## wt 10µM        ##
        ## ...            ## ...       ## ...            ##
        ###################################################
        """
        # define regex patterns to match 'CTRL ...' and 'WT ...',
        # '... 30µM' and '... 10µM'; the patterns match the entire string so
        # make sure to adjust them if the input format changes!
        ctrl_pattern = re.compile("^CTRL[0-9A-Za-zµ ]*$")
        wt_pattern = re.compile("^WT[0-9A-Za-zµ ]*$")
        ten_pattern = re.compile("^[0-9A-Za-z ]*10µM$")
        thirty_pattern = re.compile("^[0-9A-Za-z ]*30µM$")

        # initialize an empty list to hold names while iterating over
        # [i, 1] of self.derivatives.compiled
        self.derivatives_compiled = self.derivatives_table.copy()
        new_col_names = []
        for i in range(self.derivatives_compiled.shape[0]):

            # try matching control pattern
            if ctrl_pattern.match(self.derivatives_compiled.iloc[i, 1]):

                # try matching 30µM and 10µM patterns
                if ten_pattern.match(self.derivatives_compiled.iloc[i, 1]):
                    new_col_names.append("CTRL 10µM")
                elif thirty_pattern.match(
                        self.derivatives_compiled.iloc[i, 1], ):
                    new_col_names.append("CTRL 30µM")
                else:
                    raise Exception("could not match an agonist pattern")

            # try matching wildtype pattern
            elif wt_pattern.match(self.derivatives_compiled.iloc[i, 1]):

                # try matching 30µM and 10µM patterns
                if ten_pattern.match(self.derivatives_compiled.iloc[i, 1]):

                    if exclude:
                        # exclude wt values below a certain threshold
                        threshold_ten = 0.3  # currently not used
                        if self.derivatives_compiled.iloc[i, 0] < threshold[0]:
                            new_col_names.append("EXCLUDED")
                            continue
                        else:
                            new_col_names.append("WT 10µM")
                    else:
                        new_col_names.append("WT 10µM")

                elif thirty_pattern.match(
                        self.derivatives_compiled.iloc[i, 1], ):

                    if exclude:
                        # exclude wt values below a certain threshold
                        threshold_thirty = 0.6  # currently not used
                        if self.derivatives_compiled.iloc[i, 0] < threshold[0]:
                            new_col_names.append("EXCLUDED")
                        else:
                            new_col_names.append("WT 30µM")
                    else:
                        new_col_names.append("WT 30µM")

                else:
                    raise Exception("could not match an agonist pattern")

            # else, raise an exception
            else:
                raise Exception("could not match a genotype pattern")

        # add new column to dataframe
        self.derivatives_compiled["coverslip type"] = new_col_names
