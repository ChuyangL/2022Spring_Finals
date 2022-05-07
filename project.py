"""
IS597-PR Final Project:
Analysis changes in Lending data and relationship with state income

Group Members:
1. Yuting Xu (NetID: yutingx4)
2. Zheng Zhang (NetID: zhengz13)
3. Chuyang Li (NetID: chuyangl)

This .py file stores all pre-defined functions that are needed during data analysis.
"""

import os
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import typing
import seaborn as sns
import plotly.express as px


def file_exist(list_of_files: str):
    """
    Examine whether the raw data file exists in the directory. If not, download from corresponding source.
    Only four data files are allowed as correct input.

    :param list_of_files: list of file names (strings) that need to be checked.
    :return: (No returns)

    Doctest 1: Valid input
    >>> file_exist(['data/loans_full_schema.csv'])
    Examine existence of data files:
    File data/loans_full_schema.csv exists.

    Doctest 2: Invalid input
    >>> file_exist(['data/1.csv'])
    Examine existence of data files:
    Invalid file name, try again!
    """
    # Stored file source
    path_dict = {'loans_full_schema.csv': 'https://www.openintro.org/data/csv/loans_full_schema.csv',
                 'qgdpstate0322.xlsx': 'https://www.bea.gov/sites/default/files/2022-03/qgdpstate0322.xlsx',
                 'tabn102.30.xls': 'https://nces.ed.gov/programs/digest/d20/tables/xls/tabn102.30.xls',
                 'interactive_bulletin_charts_all_median.csv': 'https://www.federalreserve.gov/econres/scf/dataviz/download/interactive_bulletin_charts_all_median.csv'
                 }

    print("Examine existence of data files:")
    for file in list_of_files:
        if not os.path.exists(file):
            if file not in path_dict.keys():
                print("Invalid file name, try again!")
            else:
                print("File {} does not exist.".format(file))
                try:
                    open(file, "wb").write(requests.get(path_dict[file]).content)
                    print("File {} downloaded.".format(file))
                except Exception:
                    print("Download failed!")
        else:
            print("File {} exists.".format(file))


def loan_categorize(loans: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize loan records into 3 types: Current, Good, Bad, and insert column to tag their status
    :param loans: Original dataset of loans.
    :return: loans dataset (with loan_category column)
             finished loans dataset (with only finished dataset and has loan_category column)

    >>> file_exist(['data/loans_full_schema.csv'])
    Examine existence of data files:
    File data/loans_full_schema.csv exists.
    >>> loans = pd.read_csv('data/loans_full_schema.csv')

    Doctest 1: Valid Input
    >>> all_loans, finished = loan_categorize(loans=loans)
    >>> all_loans.shape
    (10000, 58)
    >>> finished.shape
    (520, 58)
    """
    good_loans = loans[loans['loan_status'] == 'Fully Paid']
    good_loans.insert(loc=0, column='loan_category', value='Good Loans', allow_duplicates=True)

    bad_loans = loans[loans['loan_status'].isin(['Charged Off', 'Late (31-120 days)'])]
    bad_loans.insert(loc=0, column='loan_category', value='Bad Loans', allow_duplicates=True)

    current_loans = loans[loans['loan_status'].isin(['Current', 'In Grace Period', 'Late (16-30 days)'])]
    current_loans.insert(loc=0, column='loan_category', value='Current Loans', allow_duplicates=True)

    # Merge all dataframes together to create a new loans dataframe
    loans = good_loans.append(bad_loans)
    loans = loans.append(current_loans)

    finished_loans = good_loans.append(bad_loans)

    return loans, finished_loans


def vis_dis_comparison(data: pd.DataFrame, independent: str, category: str, palette: dict):
    """
    Visualize distribution on a single variable divided to groups. The plot will be violin plots.

    :param data: Input dataset to be analyzed.
    :param independent: The target variable.
    :param category: The variable to be grouped by.
    :param palette: Input color palette.
    :return: (No returns)

    >>> file_exist(['data/loans_full_schema.csv'])
    Examine existence of data files:
    File data/loans_full_schema.csv exists.
    >>> loans = pd.read_csv('data/loans_full_schema.csv')
    >>> pal = {"Good Loans": "b", "Bad Loans": ".85"}

    Doctest 1: Invalid Input
    >>> vis_dis_comparison(data=loans, independent='1', category='2', palette=pal)
    Invalid input. Try again!
    """
    try:
        # Initial a new plot
        sns.set_theme(style="whitegrid")

        # Comparison of distribution of each group
        sns.violinplot(data=data, x=category, y=independent,
                       split=True, inner="quart", linewidth=1,
                       palette=palette)
        sns.despine(left=True)
    except Exception:
        print('Invalid input. Try again!')


def vis_dis_cummu(data: pd.DataFrame, independent: str, category: str):
    """
    Visualize cumulative proportion of certain variable.

    :param data: Input dataset to be analyzed.
    :param independent: Variable to be visualized.
    :param category: Variable for group by reference.
    :return: (No returns)

    >>> file_exist(['data/loans_full_schema.csv'])
    Examine existence of data files:
    File data/loans_full_schema.csv exists.
    >>> loans = pd.read_csv('data/loans_full_schema.csv')

    Doctest 1: Invalid Input
    >>> vis_dis_cummu(data=loans, independent='1', category='2')
    Invalid input. Try again!

    Doctest 2: Valid Input
    >>> vis_dis_cummu(data=loans, independent='interest_rate', category='loan_status')
    """
    try:
        # Initial a new plot
        sns.set_theme(style="whitegrid")

        # Cumulative distribution
        sns.displot(data=data,
                    x=independent, hue=category,
                    multiple='fill',
                    kind="kde", height=6,
                    clip=(0, None),
                    palette="ch:rot=-.25,hue=1,light=.75",
                    )
    except Exception:
        print('Invalid input. Try again!')


def plot_counts(data: pd.DataFrame, x: str, category: str):
    """
    Plot counts for multiple independent variables.

    :param data: Input pd.DataFrame.
    :param x: Column used for x axis.
    :param category: Column used for hue.
    :return: (No return)

    >>> file_exist(['data/loans_full_schema.csv'])
    Examine existence of data files:
    File data/loans_full_schema.csv exists.
    >>> loans = pd.read_csv('data/loans_full_schema.csv')

    Doctest 1: Valid Input
    >>> plot_counts(data=loans, x='sub_grade', category='loan_status')

    Doctest 2: Invalid Input
    >>> plot_counts(data=loans, x='sub_grade', category='1')
    Invalid input. Try again!
    """
    try:
        sns.set_theme(style="whitegrid")

        f, ax = plt.subplots(figsize=(15, 5))

        sns.despine(f)

        sns.histplot(
            data,
            x=x, hue=category,
            multiple="stack",
            palette="light:m_r",
            edgecolor=".3",
            linewidth=.5,
            log_scale=False,
        )
    except Exception:
        print('Invalid input. Try again!')


def plot_dis(data: pd.DataFrame, x: str, y: str):
    """
    Plot a 2-dimensional distribution.

    :param data: Input pd.DataFrame.
    :param x: Dimension 1.
    :param y: Dimension 2.
    :return: (No returns)

    >>> file_exist(['data/loans_full_schema.csv'])
    Examine existence of data files:
    File data/loans_full_schema.csv exists.
    >>> loans = pd.read_csv('data/loans_full_schema.csv')

    Doctest 1: Valid Input
    >>> plot_dis(data=loans, x='sub_grade', y='loan_status')

    Doctest 2: Invalid Input
    >>> plot_dis(data=loans, x='sub_grade', y='1')
    Invalid input. Try again!
    """
    try:
        sns.set_theme(style="dark")

        sns.displot(
            data=data, x=x, y=y, kind='hist'
        )
    except Exception:
        print('Invalid input. Try again!')


def geo_dist_usa(data: pd.DataFrame, loc_col: str, vis_col: str):
    """
    Visualize variable on a map of USA.

    :param data: Input dataset.
    :param loc_col: Column that indicate location (code for states).
    :param vis_col: Value variable.
    :return: (No returns)
    """
    fig = px.choropleth(data,
                        locations=loc_col,
                        locationmode='USA-states',
                        scope='usa',
                        color=vis_col,
                        color_continuous_scale='Viridis_r'
                        )
    fig.show()

def filter_debt(data: pd.DataFrame) -> pd.DataFrame:
    """
    filter general consumer data with only people who have debt
    :param data: general consumer data
    :return: borrower data

    >>> a = pd.read_csv("data/SCFP2010.csv")
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


def boxplot_refill(data: pd.Series):
    iqr = data.quantile(0.75) - data.quantile(0.25)
    upper = data.quantile(0.75) + 1.5 * iqr
    lower = data.quantile(0.25) - 1.5 * iqr

    def trans(x):
        if x > upper:
            return pd.NA
        elif x < lower:
            return pd.NA
        else:
            return x

    return data.map(trans)


def delete_outliers(data: pd.DataFrame, col: str) -> pd.DataFrame:
    data[col] = boxplot_refill(data[col])
    data = data.dropna(axis=0, how='any')
    data[col] = data[col].astype(float)
    return data


def open_file(name: str):
    data = pd.read_csv(name)
    df = pd.DataFrame(data, columns=['debt_to_income', 'emp_length'])
    df = df.dropna(axis=0, how='any')
    return [data, df]