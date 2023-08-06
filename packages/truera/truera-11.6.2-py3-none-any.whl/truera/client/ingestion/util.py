from typing import Optional, Sequence, Tuple

import pandas as pd

from truera.client.ingestion import ColumnSpec
from truera.client.ingestion.constants import \
    FEATURE_INFLUENCE_SUFFIX_TRUERA_QII


def merge_dataframes_and_create_column_spec(
    id_col_name: str,
    timestamp_col_name: Optional[str] = None,
    pre_data: Optional[pd.DataFrame] = None,
    post_data: Optional[pd.DataFrame] = None,
    predictions: Optional[pd.DataFrame] = None,
    labels: Optional[pd.DataFrame] = None,
    extra_data: Optional[pd.DataFrame] = None,
    feature_influences: Optional[pd.DataFrame] = None,
    feature_influence_suffix: Optional[str
                                      ] = FEATURE_INFLUENCE_SUFFIX_TRUERA_QII
) -> Tuple[pd.DataFrame, ColumnSpec]:

    sys_cols = [id_col_name]
    if timestamp_col_name is not None:
        sys_cols.append(timestamp_col_name)

    pre_data_col_names = _get_columns(pre_data, exclude=sys_cols)

    if pre_data is not None and feature_influences is not None:

        def rename_fi_col(fi_col_name):
            if fi_col_name in pre_data_col_names:
                return fi_col_name + feature_influence_suffix
            return fi_col_name

        feature_influences = feature_influences.rename(columns=rename_fi_col)

    dfs = [
        df for df in [
            pre_data, post_data, predictions, labels, extra_data,
            feature_influences
        ] if df is not None
    ]

    data = None
    for df in dfs:
        if id_col_name not in df.columns:
            raise ValueError(
                f"Id column '{id_col_name}' needs to be in every dataframe."
            )
        if data is None:
            data = df.copy()
        else:
            if len(df) != len(data):
                raise ValueError("DataFrames need to be the same length.")
            columns = df.columns.difference(data.columns
                                           ).to_list() + [id_col_name]
            data = data.merge(df[columns], on=id_col_name)

    column_spec = ColumnSpec(
        id_col_name=id_col_name,
        timestamp_col_name=timestamp_col_name,
        pre_data_col_names=pre_data_col_names,
        post_data_col_names=_get_columns(post_data, exclude=sys_cols),
        prediction_col_names=_get_columns(predictions, exclude=sys_cols),
        label_col_names=_get_columns(labels, exclude=sys_cols),
        extra_data_col_names=_get_columns(extra_data, exclude=sys_cols),
        feature_influence_col_names=_get_columns(
            feature_influences, exclude=sys_cols
        )
    )
    return data, column_spec


def _get_columns(data: pd.DataFrame, exclude: Sequence[str]) -> Sequence[str]:
    if data is None:
        return []
    columns = [c for c in data.columns if c not in exclude]
    return columns
