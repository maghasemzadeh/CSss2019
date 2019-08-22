import logger
import pandas as pd
from typing import List
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


def show_columns(df: pd.DataFrame):
    '''
    :param df:
    :return dataframe:
    '''
    out = [i for i in df.columns]
    return out


def select_columns(df: pd.DataFrame, columns: List[str], criteria: str = None) -> pd.DataFrame:
    '''
    :param df:
    :param columns:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    columns = [x for x in columns if x in df.columns]
    return df[columns].copy()


def drop_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    '''
    :param df:
    :param columns:
    :return:
    '''
    columns = [x for x in columns if x in df.columns]
    return df.copy().drop(columns=columns)


def fill_na_values(df: pd.DataFrame, columns='all', value=0) -> pd.DataFrame:
    '''
    :param df:
    :param columns:
    :param value:
    :return:
    '''
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
    '''
    :param df:
    :param columns:
    :return:
    '''
    df_copy = df.copy()
    if columns is 'all':
        columns = df.columns
    n = len(columns)
    columns = [x for x in columns if x in df.columns]
    if n is not len(columns):
        logger.log_warn('some columns not found in dataFrame')
    df_copy = df_copy.dropna(subset=columns)
    return df_copy


def summarize(df: pd.DataFrame, groupby_columns: List[str], aggregate_functions: List[str]) -> pd.DataFrame:
    '''
    :param df:
    :param groupby_columns:
    :param aggregate_functions:
    :return:
    '''
    for item in groupby_columns:
        if item not in df.columns:
            print('no such column ' + item)
            return
    d = {}
    valid_func = ['min', 'sum', 'count', 'mean', 'max', 'median', 'var', 'std']
    for item in aggregate_functions:
        print(item)
        item = item.split(':')
        if item[0] not in df.columns:
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
    '''
    :param df:
    :param criteria:
    :return:
    '''
    try:
        result = df[df.eval(criteria)]
        return result
    except Exception as e:
        logger.log_error(e)
        return df


def plot_2d(df: pd.DataFrame, x: str, y: str, color: str = None, trendline: bool = False, criteria: str = None) -> go.Figure:
    '''
    :param df:
    :param x:
    :param y:
    :param color:
    :param trendline:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
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


def plot_3d(df: pd.DataFrame, x: str, y: str, z: str, color: str = None, criteria: str = None) -> go.Figure:
    '''
    :param df:
    :param x:
    :param y:
    :param z:
    :param color:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    if color is None and not pd.Series([x, y, z]).isin(df.columns).all() or \
            color is not None and not pd.Series([x, y, z, color]).isin(df.columns).all():
        logger.log_error('columns not found')
        return
    return px.scatter_3d(data_frame=df, x=x, y=y, z=z, color=color)


def histogram(df: pd.DataFrame, x: str, bins: int = 30, criteria: str = None) -> go.Figure:
    '''
    :param df:
    :param x:
    :param bins:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    if x not in df.columns:
        logger.log_error('column not found')
        return
    return px.histogram(df, x=x, nbins=bins)


def density(df: pd.DataFrame, columns: List[str], bin_size: int = .2, criteria: str = None) -> go.Figure:
    '''
    :param df:
    :param columns:
    :param bin_size:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    return ff.create_distplot([df[i] for i in columns if i in df.columns], [i for i in columns if i in df.columns], bin_size=bin_size, curve_type="kde")


def bar_chart(df: pd.DataFrame, x: str, y: str, color: str = None, criteria: str = None) -> go.Figure:
    '''
    :param df:
    :param x:
    :param y:
    :param color:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    if not pd.Series([x, y]).isin(df.columns).all():
        logger.log_error('columns not founded')
        return
    return px.bar(df, x=x, y=y, color=color)


def pie_chart(df: pd.DataFrame, r: str, theta: str, criteria: str = None) -> go.Figure:
    '''
    :param df:
    :param r:
    :param theta:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    if not pd.Series([theta, r]).isin(df.columns).all():
        logger.log_error('columns not founded')
        return
    return px.bar_polar(df, r=r, theta=theta)


def heatmap(df: pd.DataFrame, x: str, y: str, criteria: str = None) -> go.Figure:
    '''
    :param df:
    :param x:
    :param y:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    if not x in df.columns:
        logger.log_error('x not found in columns')
        return
    if not y in df.columns:
        logger.log_error('y not found in columns')
        return
    return px.density_heatmap(df, x=x, y=y)


def view(df: pd.DataFrame, start: int = None, end: int = None, criteria: str = None) -> pd.DataFrame:
    '''
    :param df:
    :param start:
    :param end:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    #     qgrid.show_grid(df[start:end])
    return df[start:end]


def head(df: pd.DataFrame, count: int = 5, criteria: str = None) -> pd.DataFrame:
    '''
    :param df:
    :param count:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    #     qgrid.show_grid(df[:count])
    return df[:count]


def tail(df: pd.DataFrame, count: int = 5, criteria: str = None) -> pd.DataFrame:
    '''
    :param df:
    :param count:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    #     qgrid.show_grid(df[count:])
    return df[count:]


def max_record(df: pd.DataFrame, column: str, criteria: str = None) -> pd.DataFrame:
    '''
    :param df:
    :param column:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    if not column in df.columns:
        print('no such column ' + column)
        return
    return df[df[column] == max(df[column])]


def min_record(df: pd.DataFrame, column: str, criteria: str = None) -> pd.DataFrame:
    '''
    :param df:
    :param column:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    if not column in df.columns:
        print('no such column ' + column)
        return
    return df[df[column] == min(df[column])]


def sort(df: pd.DataFrame, columns: List[str], ascending: bool, criteria: str = None) -> pd.DataFrame:
    '''
    :param df:
    :param columns:
    :param ascending:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    return df.sort_values(by=columns, ascending=ascending)


def box_plot(df: pd.DataFrame, x: str, y: str, criteria: str = None) -> go.Figure:
    '''
    :param df:
    :param x:
    :param y:
    :param criteria:
    :return:
    '''
    if criteria is not None:
        df = filter_records(df, criteria)
    if not pd.Series([x, y]).isin(df.columns).all():
        logger.log_error('columns not founded')
        return
    return px.box(df, x=x, y=y)


def unique_records(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    '''
    :param df:
    :param columns:
    :return:
    '''
    for item in columns:
        if item not in df.columns:
            print('no such column ' + item)
            return
    return df.drop_duplicates(columns)


def agg(df: pd.DataFrame, column: str, function:str):
    '''
    :param df:
    :param column:
    :param function:
    :return:
    '''
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


def tokenize(f):
    '''
    :param f:
    :return:
    '''
    symbols = ['(', ')', '=', '+', '-', '*', '/', '%', '^', '==', '<=', '>=', '>', '<', '<>', '!=']
    f = f.replace(' ', '')
    tokens = []
    token = ''
    i = 0
    while i < len(f):
        if f[i] in symbols:
            if token != '':
                tokens.append((token, 'operand'))
                token = ''
            if f[i:i + 2] in symbols:
                tokens.append((f[i:i + 2], 'symbol'))
                i += 1
            else:
                tokens.append((f[i], 'symbol'))
        else:
            token += f[i]
        i += 1
    if token != '':
        tokens.append((token, 'operand'))

    return tokens


def apply(df: pd.DataFrame, new_col: str,  formula: str) -> pd.DataFrame:
    '''
    :param df:
    :param new_col:
    :param formula:
    :return:
    '''
    new_df = df.copy()
    tokens = tokenize(formula)
    for t in tokens:
        if t[1] is 'operand':
            if not t[0].isdigit() and '.' not in t[0]:
                formula = formula.replace(t[0], 'df[\'' + t[0] + '\']')
    new_df[new_col] = eval(formula)
    return new_df
