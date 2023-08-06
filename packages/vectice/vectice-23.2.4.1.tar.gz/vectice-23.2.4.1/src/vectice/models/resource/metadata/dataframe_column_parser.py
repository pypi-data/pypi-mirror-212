from __future__ import annotations

import logging

import pandas as pd
from pandas import DataFrame, Series, api

from vectice.models.resource.metadata.column_metadata import (
    BooleanStat,
    Column,
    ColumnCategoryType,
    DateStat,
    MostCommon,
    NumericalStat,
    Quantiles,
    TextStat,
)

_logger = logging.getLogger(__name__)


def capture_columns(init_columns: list[Column] | None, dataframe: DataFrame | None) -> list:
    init_columns = init_columns if init_columns is not None else []
    if dataframe is None:
        return [column.asdict() for column in init_columns]

    columns: list[Column] = []
    column_names_with_types = dataframe.dtypes.astype(str).to_dict()
    for idx, (name, d_type) in enumerate(column_names_with_types.items()):
        if idx >= 100:
            _logger.warning("Statistics are only captured for the first 100 columns of your dataframe.")
            break
        category_type, stats = capture_column_stats(dataframe[name])
        columns.append(
            Column(
                name=name,
                data_type=d_type if d_type != "object" else "string",
                stats=stats,
                category_type=category_type,
            )
        )

    return [column.asdict() for column in columns]


def capture_column_stats(
    series: Series,
) -> tuple[ColumnCategoryType | None, TextStat | BooleanStat | NumericalStat | DateStat | None]:
    def is_date_series(column: Series) -> bool:
        if api.types.is_datetime64_any_dtype(column):
            return True

        try:
            # Temporary fixing issue -> TypeError: data type 'dbdate' not understood [EN-2534]
            if column.dtypes == "dbdate":
                return True
        except TypeError:
            pass

        return False

    if api.types.is_bool_dtype(series):
        return ColumnCategoryType.BOOLEAN, compute_boolean_column_statistics(series)
    elif api.types.is_numeric_dtype(series):
        return ColumnCategoryType.NUMERICAL, compute_numeric_column_statistics(series)
    elif is_date_series(series):
        return ColumnCategoryType.DATE, compute_date_column_statistics(series)
    if api.types.is_string_dtype(series) | api.types.is_categorical_dtype(series):
        return ColumnCategoryType.TEXT, compute_string_column_statistics(series)
    return None, None


def compute_boolean_column_statistics(series: Series) -> BooleanStat:
    """Parse a dataframe series and return statistics about it.

    The computed statistics are:
    - The percentage of True
    - The percentage of False
    - The count missing value in %
    Parameters:
        series: The pandas series to get information from.

    Returns:
        A BooleanStat object containing the above statistics.
    """
    value_counts = series.value_counts(dropna=False)
    value_counts = value_counts / value_counts.sum()
    missing = series.isnull().sum() / len(series)

    return BooleanStat(true=float(value_counts[True]), false=float(value_counts[False]), missing=float(missing))


def compute_numeric_column_statistics(series: Series) -> NumericalStat:
    """Parse a dataframe series and return statistics about it.

    The computed statistics are:
    - the mean
    - the standard deviation
    - the min value
    - the 25% percentiles
    - the 50% percentiles
    - the 75% percentiles
    - the max value
    - the count missing value in %
    Parameters:
        series: The pandas series to get information from.

    Returns:
        A NumericalStat object containing the above statistics.
    """
    mean = series.mean()
    std = series.std()
    min = series.min()
    q25 = series.quantile(0.25)
    q50 = series.quantile(0.5)
    q75 = series.quantile(0.75)
    max = series.max()
    missing = series.isnull().sum() / len(series)

    return NumericalStat(
        mean=float(mean),
        std_deviation=float(std),
        quantiles=Quantiles(q_min=float(min), q25=float(q25), q50=float(q50), q75=float(q75), q_max=float(max)),
        missing=float(missing),
    )


def compute_string_column_statistics(series: Series) -> TextStat:
    """Parse a dataframe series and return statistics about it.

    The computed statistics are:
    - the unique number of value
    - the top 3 most common values with their percentages
    - the count missing value in %
    Parameters:
        series: The pandas series to get information from.

    Returns:
        A TextStat object containing the above statistics.
    """
    missing = series.isnull().sum() / len(series)
    unique = len(series.unique())
    value_counts: Series[float] = series.value_counts() / series.value_counts(dropna=False).sum()

    size = 3 if unique >= 3 else unique
    value_counts = value_counts.nlargest(size)

    return TextStat(
        unique=float(unique),
        missing=float(missing),
        most_commons=[MostCommon(str(i), float(value_counts[i])) for i in value_counts.index],
    )


def compute_date_column_statistics(series: Series) -> DateStat:
    """Parse a dataframe series and return statistics about it.

    The computed statistics are:
    - the first date
    - the mean
    - the median
    - the last date
    - the count missing value in %
    Parameters:
        series: The pandas series to get information from.

    Returns:
        A DateStat object containing the above statistics.
    """
    # Convert to datetime since mean is not supported for non datetime pandas object such as dbdates
    series = pd.to_datetime(series)
    min = series.min().isoformat()
    mean = series.mean().isoformat()
    median = series.median().isoformat()
    max = series.max().isoformat()
    missing = series.isnull().sum() / len(series)

    return DateStat(missing=float(missing), minimum=str(min), mean=str(mean), median=str(median), maximum=str(max))
