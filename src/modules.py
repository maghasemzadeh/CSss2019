import pandas as pd
from typing import List
import plotly.express as px
import plotly.graph_objects as go
import logger
import re
import operator
import plotly.figure_factory as ff

__operation_parser__ = {
    '<': operator.lt, '<=': operator.le, '>': operator.gt, '>=': operator.ge,
    '==': operator.eq, '=': operator.eq, '!=': operator.ne, 'is': operator.is_,
    '!is': operator.is_not, 'is_not': operator.is_not, 'and': operator.and_,
    '&': operator.and_, '&&': operator.and_, 'or': operator.or_, '|': operator.or_, '||': operator.or_
}


def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    columns = [x for x in columns if x in df.columns]
    return df[columns].copy()


def drop_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    columns = [x for x in columns if x in df.columns]
    return df.copy().drop(columns=columns)


def fill_na_values(df: pd.DataFrame, columns='all', value=0) -> pd.DataFrame:
    df_copy = df.copy()
    if columns is 'all':
        df_copy = df_copy.fillna(value)
    else:
        n = len(columns)
        columns = [x for x in columns if x in df.columns]
        if n is not len(columns):
            logger.log_warn('some columns not found in dataFrame')
        df_copy[columns] = df_copy[columns].fillna(value)
    return df_copy


def drop_na(df: pd.DataFrame, columns='all') -> pd.DataFrame:
    df_copy = df.copy()
    if columns is 'all':
        columns = df.columns
    n = len(columns)
    columns = [x for x in columns if x in df.columns]
    if n is not len(columns):
        logger.log_warn('some columns not found in dataFrame')
    df_copy = df_copy.dropna(subset=columns)
    return df_copy


def summarize(df: pd.DataFrame, groupby_columns: List[str], aggregate_functions : List[str]) -> pd.DataFrame:
    for item in groupby_columns:
        if not df.columns.contains(item):
            print('no such column ' + item)
            return
    d = {}
    valid_func = ['min', 'sum', 'count', 'mean', 'max', 'median', 'var', 'std']
    for item in aggregate_functions:
        print(item)
        item = item.split(':')
        if not df.columns.contains(item[0]):
            print('no such column ' + item[0])
            return
        elif not valid_func.__contains__(item[1]):
            print('no such function ' + item[1])
            return
        else:
            d.update({
                item[0]: item[1]
            })
    res = df.groupby(groupby_columns).agg(d).reset_index()
    return res
    

def filter_records(df: pd.DataFrame, criteria: str) -> pd.DataFrame:
    criteria = criteria.strip()
    if len(criteria.split(' ')) != 3:
        logger.log_error("operation must has 3 parts: '" + criteria + "'")
        return df

    first_elm, operation, second_elm = criteria.split(' ')

    try:
        first_elm = __pars_element__(df, first_elm)
        second_elm = __pars_element__(df, second_elm)
    except ValueError:
        logger.log_error("dataframe column not found.")
        return df

    try:
        df = df[__operation_parser__[operation](first_elm, second_elm)]
    except KeyError:
        logger.log_error("Operation not found. Valid operations are:\n"
                         "<\t<=\t>\t>=\n"
                         "=\t==\t!=\tis\n"
                         "!is\tis_not\tand\t&\n"
                         "&&\tor\t||\t|")
    return df


def plot_2d(df: pd.DataFrame, x: str, y: str, color: str = None, trendline: bool = False) -> go.Figure:
    if not x in df.columns:
        logger.log_error('x not found in columns')
        return
    if not y in df.columns:
        logger.log_error('y not found in columns')
        return
    if not color in df.columns and not color is None:
        logger.log_warn('color column not found')
        color = None
    if trendline:
        trendline = 'ols'
    return px.scatter(df, x=x, y=y, color=color, trendline=trendline)


def plot_3d(df: pd.DataFrame, x: str, y: str, z: str, color: str = None) -> go.Figure:
    if color is None and not pd.Series([x, y, z]).isin(df.columns).all() or \
            color is not None and not pd.Series([x, y, z, color]).isin(df.columns).all():
        logger.log_error('columns not found')
        return
    return px.scatter_3d(data_frame=df, x=x, y=y, z=z, color=color)


def histogram(df: pd.DataFrame, x: str, bins: int = 30) -> go.Figure:
    if x not in df.columns:
        logger.log_error('column not found')
        return
    return px.histogram(df, x=x, nbins=bins)


def density(df: pd.DataFrame, *columns: str, bin_size: int = .2) -> go.Figure:
    return ff.create_distplot([df[i] for i in columns if i in df.columns], [i for i in columns if i in df.columns], bin_size=bin_size, curve_type="kde")


def bar_chart(df: pd.DataFrame, x: str, y: str) -> go.Figure:
    if not pd.Series([x, y]).isin(df.columns).all():
        logger.log_error('columns not founded')
        return
    return px.bar(df, x=x, y=y)


def pie_chart(df: pd.DataFrame, r: str, theta: str) -> go.Figure:
    if not pd.Series([theta, r]).isin(df.columns).all():
        logger.log_error('columns not founded')
        return
    return px.bar_polar(df, r=r, theta=theta)


def heatmap(df: pd.DataFrame, x: str, y: str) -> go.Figure:
    if not x in df.columns:
        logger.log_error('x not found in columns')
        return
    if not y in df.columns:
        logger.log_error('y not found in columns')
        return
    return px.density_heatmap(df, x=x, y=y)


def view(df: pd.DataFrame, start: int = None, end: int = None) -> pd.DataFrame:
    #     qgrid.show_grid(df[start:end])
    return df[start:end]


def head(df: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    #     qgrid.show_grid(df[:count])
    return df[:count]


def tail(df: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    #     qgrid.show_grid(df[count:])
    return df[count:]


def max_record(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if not column in df.columns:
        print('no such column ' + column)
        return
    return df[df[column] == max(df[column])]


def min_record(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if not column in df.columns:
        print('no such column ' + column)
        return
    return df[df[column] == min(df[column])]

def sort(df: pd.DataFrame, columns: List[str], ascending: bool) -> pd.DataFrame:
    return df.sort_values(by=columns, ascending=ascending)


def box_plot(df: pd.DataFrame, x: str, y: str) -> go.Figure:
    if not pd.Series([x, y]).isin(df.columns).all():
        logger.log_error('columns not founded')
        return
    return px.box(df, x=x, y=y)



def unique_records(df: pd.DataFrame, columns:List[str]) -> pd.DataFrame:
    for item in columns:
        if not df.columns.contains(item):
            print('no such column ' + item)
            return
    return df.drop_duplicates(columns)


def agg(df: pd.DataFrame, column: str, function:str):
    if not column in df.columns:
        print('no such column ' + column)
        return
    if function == 'mean':
        return df[column].mean()
    elif function == 'max':
        return max(df[column])
    elif function == 'min':
        return min(df[column])
    else:
        print('no such function!')
        return


def __pars_element__(df: pd.DataFrame, value: str):
    string_pattern = re.compile('\\"\\w+\\"')
    if re.fullmatch(string_pattern, value):
        return value[1:-1]
    else:
        try:
            return eval(value)
        except NameError:
            if value not in df.columns:
                raise ValueError
            return df[value]

