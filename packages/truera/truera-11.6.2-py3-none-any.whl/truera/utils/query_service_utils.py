from typing import Any, Sequence, Union

import pandas as pd


def compute_inner_merge(
    data: Sequence[Union[pd.Series, pd.DataFrame]]
) -> Sequence[Union[pd.Series, pd.DataFrame]]:
    if len(data) <= 1:
        return data
    indexes = compute_index_intersection(data)
    return [curr.loc[indexes] for curr in data]


def compute_index_intersection(
    data: Sequence[Union[pd.Series, pd.DataFrame]]
) -> Sequence[Any]:
    ret = data[0].index
    for i in range(1, len(data)):
        ret = ret.intersection(data[i].index)
    return ret
