import pandas as pd
from typing import List
import plotly.express as px
import plotly.graph_objects as go
import logger
import re
import operator


def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    return df[columns].copy()


def drop_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
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


def summarize(df: pd.DataFrame, groupby_columns: List[str], aggregate_functions: List[str]) -> pd.DataFrame:
    # aggregate_function: sum, count, mean, variance, sd, min, max, mode, mid
    # groupby_columns: list of column names
    pass


__operation_parser__ = {
    '<': operator.lt, '<=': operator.le, '>': operator.gt, '>=': operator.ge,
    '==': operator.eq, '=': operator.eq, '!=': operator.ne, 'is': operator.is_,
    '!is': operator.is_not, 'is_not': operator.is_not, 'and': operator.and_,
    '&': operator.and_, '&&': operator.and_, 'or': operator.or_, '|': operator.or_, '||': operator.or_
}


def filter_records(df: pd.DataFrame, criteria: str) -> pd.DataFrame:
    criteria = criteria.lower().strip()
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
    px.scatter(df, x=x, y=y, color=color, trendline=trendline).show()


def plot_3d(df: pd.DataFrame, x: str, y: str, z: str, color: str = None, trend_pane: bool = False) -> go.Figure:
    pass


def histogram(df: pd.DataFrame, x: str, bins: int = 30) -> go.Figure:
    pass


def density(df: pd.DataFrame, x: str) -> go.Figure:
    pass


def bar_chart(df: pd.DataFrame, x: str, y: str) -> go.Figure:
    if not pd.Series([x, y]).isin(df.columns).all():
        logger.log_error('columns not founded')
        return
    return px.bar(df, x=x, y=y)


def pie_chart(df: pd.DataFrame, r: str, theta: str) -> go.Figure:
    pass


def heatmap(df: pd.DataFrame, x: str, y: str) -> go.Figure:
    if not x in df.columns:
        logger.log_error('x not found in columns')
        return
    if not y in df.columns:
        logger.log_error('y not found in columns')
        return
    px.density_heatmap(df, x=x, y=y).show()


def __pars_element__(df: pd.DataFrame, value: str):
    string_pattern = re.compile('\\"\\w+\\"')
    if re.fullmatch(string_pattern, value):
        return
    else:
        try:
            return eval(value)
        except NameError:
            if value not in df.columns:
                raise ValueError
            return df[value]