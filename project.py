import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import typing
import numba as nb


def filter_debt(data: pd.DataFrame) -> pd.DataFrame:
    """
    filter general consumer data with only people who have debt
    :param data: general consumer data
    :return: borrower data

    >>> a = pd.read_csv("SCFP2010.csv")
    >>> a["HDEBT"].unique()
    array([1, 0], dtype=int64)
    >>> b = filter_debt(a)
    >>> b["HDEBT"].unique()
    array([1], dtype=int64)
    """
    return data[data["HDEBT"] == 1]


def group_by_case(data: pd.DataFrame) -> pd.DataFrame:
    """ get mean value of income, debt, debt to income ratio column, group by case id.
    :param data: general consumer data
    :return: aggregated consumer data, group by case id, return average income, average debt, average debt/income ratio
    >>> a = {"YY1":[1, 1, 1, 2, 3],"INCOME":[20, 30, 40, 50, 60],"DEBT": [10, 10, 20, 30, 10],"DEBT2INC": [2, 3, 2, 5/3, 6]}
    >>> a = pd.DataFrame(a)
    >>> b = group_by_case(a)
    >>> b["INCOME"][1]
    30.0
    >>> b["DEBT"][3]
    10.0
    """
    return data.groupby('YY1').agg({"INCOME": "mean", "DEBT": "mean", "DEBT2INC": "mean"})


def de_inflation(data: pd.DataFrame) -> pd.DataFrame:
    """ de_inflation consumer data in 2019 to the level in 2010 based on CPI(Consumer price index)
    :param data: aggregated consumer data with column income, debt
    :return: aggregated consumer data with column deinflation income, debt
    >>> a = {"INCOME":[100, 200, 1450],"DEBT":[20, 1402, 8872], "DEBT2INC": [0, 0, 0]}
    >>> a = pd.DataFrame(a)
    >>> b = de_inflation(a)
    >>> b["deinf_INCOME"]
    0      85.295268
    1     170.590536
    2    1236.781384
    Name: deinf_INCOME, dtype: float64
    >>> b["deinf_DEBT"]
    0      17.059054
    1    1195.839656
    2    7567.396167
    Name: deinf_DEBT, dtype: float64
    """
    CPI_2019 = 255.7
    CPI_2010 = 218.1
    inf_rate = CPI_2019 / CPI_2010
    data["deinf_INCOME"] = data["INCOME"] / inf_rate
    data["deinf_DEBT"] = data["DEBT"] / inf_rate
    data["deinf_DEBT2INC"] = data["DEBT2INC"]
    return data


def draw_outliers(datas: typing.List, title: str):
    """ draw three subplots of box charts of given data series.
    :param datas: list of corresponding data series in the order of [loan club, general borrowers in 2010, general borrowers in 2019]
    :param title: given title
    :return: a painting
    """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8, 5))
    plt.subplots_adjust(wspace=2, hspace=0.5)
    for i in range(len(datas)):
        data = datas[i]
        data.plot(ax=axes[i], kind='box', sym='r+')
    axes[0].set_xlabel("Loan Club")
    axes[1].set_xlabel("General Borrower in 2010")
    axes[2].set_xlabel("General Borrower in 2019")
    plt.suptitle(title)


def cut_by_category(data: pd.core.series.Series, bins: typing.List, labels: typing.List) -> pd.core.series.Series:
    """ cut data series into categories based on given bins, return the percentage of each category
    :param data: original numerial data series
    :param bins: classification level for each category
    :param labels: category name
    :return: percentage of each category
    >>> a = {"INCOME":[100, 200, 1450, 2334, 556, 439, 3749, 3888, 20]}
    >>> a = pd.DataFrame(a)
    >>> a = a["INCOME"]
    >>> bins = [0, 500, 1000, 2000, np.inf]
    >>> labels = ["<500", "500-1000", "1000-2000", ">2000"]
    >>> cut_by_category(a, bins, labels)
    <500         0.444444
    >2000        0.333333
    500-1000     0.111111
    1000-2000    0.111111
    Name: INCOME, dtype: float64
    """
    income_groups = pd.cut(data, bins=bins, labels=labels)
    income_ratio = income_groups.value_counts(dropna=True, normalize=True)
    return income_ratio


def calculate_concat_ratio(data1: pd.core.series.Series,
                            data2: pd.core.series.Series,
                            data3: pd.core.series.Series,
                            bins: typing.List,
                            labels: typing.List,
                            rename_map: dict,
                            calculate: bool) -> pd.DataFrame:
    """ calculate the percentage of each category of three data series input based on given bins, and then concat the
    three ratio series, return as well-named dataframe
    :param data1: original numerial data series1
    :param data2: original numerial data series2
    :param data3: original numerial data series3
    :param bins: classification level for each category
    :param labels: category name
    :param rename_map: rename maping (key: original column name, value: preferred column name in output dataframe)
    :param calculate: if true, calculate the proportion first, if false, just concat
    :return:
    >>> a = pd.DataFrame({"a_INCOME":[100, 200, 1450, 2334, 556, 439, 3749, 3888, 20]})["a_INCOME"]
    >>> b = pd.DataFrame({"b_INCOME":[100, 200, 1450, 2334, 556, 439, 3749, 3888, 20, 484, 588, 88]})["b_INCOME"]
    >>> c = pd.DataFrame({"c_INCOME":[10, 20, 150, 234, 56, 439, 3749, 3888, 20, 49, 599, 2]})["c_INCOME"]
    >>> bins = [0, 500, 1000, 2000, np.inf]
    >>> labels = ["<500", "500-1000", "1000-2000", ">2000"]
    >>> rename_map = {"a_INCOME":"a", "b_INCOME":"b", "c_INCOME":"c"}
    >>> calculate_concat_ratio(a, b, c, bins, labels, rename_map, True)
                      a         b         c
    <500       0.444444  0.500000  0.750000
    >2000      0.333333  0.250000  0.166667
    500-1000   0.111111  0.166667  0.083333
    1000-2000  0.111111  0.083333  0.000000
    """
    if calculate:
        ratio1 = cut_by_category(data1, bins, labels)
        ratio2 = cut_by_category(data2, bins, labels)
        ratio3 = cut_by_category(data3, bins, labels)
    else:
        ratio1, ratio2, ratio3 = data1, data2, data3
    concat_ratio_table = pd.concat([ratio1, ratio2, ratio3], axis=1)
    concat_ratio_table.rename(columns=rename_map, inplace=True)
    return concat_ratio_table


def remove_outlier(datas: typing.List, boundary: int) -> typing.List:
    """ remove point value less than boundary in each data series in input list
    :param datas: List of data series
    :param boundary: the boundary value that the output value should be less than
    :return: List of data series after processing
    >>> a = pd.DataFrame({"a":[100, 200, 1450, 2334, 556, 439, 3749, 3888, 20]})["a"]
    >>> b = pd.DataFrame({"b":[1, 20000, 3235, 4, -1, 00000, 999, 1000]})["b"]
    >>> c = remove_outlier([a, b], 1000)
    >>> c[0]
    0    100
    1    200
    4    556
    5    439
    8     20
    Name: a, dtype: int64
    >>> c[1]
    0      1
    3      4
    4     -1
    5      0
    6    999
    Name: b, dtype: int64
    """
    ans = []
    for data in datas:
        data = data[data<boundary]
        data.plot(kind="hist", bins=20, alpha=0.5, legend=True)
        ans.append(data)
    return ans
