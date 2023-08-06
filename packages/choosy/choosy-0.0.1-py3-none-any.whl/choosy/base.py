# SPDX-FileCopyrightText: 2023-present Casey Schneider-Mizell <caseysm@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd


class StructuredSampler:
    def __init__(
        self,
        data: pd.DataFrame,
        bin_column: Optional[Union[str, List[str]]] = None,
        weight_column: Optional[str] = None,
    ):
        """
        Set up a dataframe for sampling.

        Parameters
        ~~~~~~~~~
        data: pd.DataFrame
            Dataframe to sample from.
        bin_column: str or list of str, optional.
            Column or columns to use for binning. If None, no binning is used.
        weight_column: str, optional.
            Column to use for weighting. If None, no weighting is used.
        seed: int, optional.
            Seed for the random number generator. Default is None.
        """
        self._data = data
        self._weight_column = weight_column
        self._bin_column = bin_column

    def sample_data(
        self,
        n_sample: Union[int, Dict, pd.Series],
        count_column: Optional[str] = None,
        bin_column: Optional[Union[str, List[str]]] = None,
        weight_column: Optional[str] = None,
        replace: Optional[bool] = True,
        seed: Optional[int] = None,
        column_name: Optional[str] = "sample_count",
    ):
        """
        Sample data from a dataframe, selecting specified numbers of samples based on values in a column or columns.

        Parameters
        ~~~~~~~~~
        n_sample: int, pd.Series, or dict.
            Number of samples to pull from the initial dataframe.
            If an int, bin_column is not used.
            If a dict, maps bins to number of samples per bin. Must have a bin_column.
            If a Series, maps bins to number of samples via n_sample.loc[*index_value] where
            bin_column must be the same length and order as the indices, for example as in a
            groupby+count operation.
        count_column : str or None.
            Column to accumulate values for.
            If None, returns the sampled dataframe rather than accumulated values.
        bin_column : str or list.
            Column to use for binning. Values in this column must match values in the n_sample dict or series.
            Bin column can be a list of strings if n_sample is a series with a multi-level index.
        replace: bool, optional.
            Chooses whether to sample data with replacement or not. Default is True.
        seed: int, optional.
            Seed for the random number generator. Default is None.
        column_name: str, optional.
            Name of the column to use for the aggregated count column. Default is "sample_count".

        Returns
        ~~~~~~~
        pd.DataFrame
            A dataframe sampled from the original. If count_column is not None, the dataframe is aggregated by values
            from that column, otherwise the dataframe rows are returned directly.
        """
        if bin_column is None:
            bin_column = self._bin_column
        if weight_column is None:
            weight_column = self._weight_column
        dfs = []
        if isinstance(n_sample, int):
            if bin_column is None:
                dfs.append(
                    self._simple_sample(
                        n_sample,
                        None,
                        replace=replace,
                        seed=seed,
                        weight=weight_column,
                    )
                )
            else:
                bin_values = np.unique(self._data[bin_column])
                for bin_value in bin_values:
                    dfs.append(
                        self._simple_sample(
                            n_sample,
                            self._format_filter(bin_column, bin_value),
                            replace=replace,
                            seed=seed,
                            weight=weight_column,
                        )
                    )
        elif isinstance(n_sample, dict):
            if bin_column is None:
                msg = "No bin column is set!"
                raise ValueError(msg)
            for bin_value, n in n_sample.items():
                dfs.append(
                    self._simple_sample(
                        n,
                        self._format_filter(bin_column, bin_value),
                        replace=replace,
                        seed=seed,
                        weight=weight_column,
                    )
                )
        elif isinstance(n_sample, pd.Series):
            if bin_column is None:
                msg = "No bin column is set!"
                raise ValueError(msg)
            for index_val in n_sample.index:
                dfs.append(
                    self._simple_sample(
                        n_sample.loc[index_val],
                        self._format_filter(bin_column, index_val),
                        replace=replace,
                        seed=seed,
                        weight=weight_column,
                    )
                )
        else:
            msg = f"n_sample must be an int, dict, or pd.Series, not {type(n_sample)}"
            raise ValueError(msg)
        return self._aggregate_results(dfs, count_column, column_name)

    def sample_repeat(
        self,
        n_repeat: int,
        n_sample: Union[int, Dict, pd.Series],
        count_column: str,
        bin_column: Optional[Union[str, List[str]]] = None,
        weight_column: Optional[str] = None,
        replace: Optional[bool] = True,
        seed: Optional[int] = None,
    ):
        """Repeated sampling of counts from a dataframe with the same parameters.

        Parameters
        ----------
        n_repeat : int
            Number of repeated samplings.
        n_sample : int, pd.Series, or dict.
            Number of samples to pull from the initial dataframe.
            Same behavior as in sample_data.
            If an int, bin_column is not used.
            If a dict, maps bins to number of samples per bin. Must have a bin_column.
            If a Series, maps bins to number of samples via n_sample.loc[*index_value] where
            bin_column must be the same length and order as the indices, for example as in a
            groupby+count operation.
        count_column : str
            Column to accumulate values for.
        bin_column : str or list, optional
            Column to use for binning. Values in this column must match values in the n_sample dict or series.
            Bin column can be a list of strings if n_sample is a series with a multi-level index.
            Optional, default is None.
        weight_column : str, optional
            Column to use for sample weighting. Optional, default is None.
        replace : bool, optional
            Chooses whether to sample with replacement, by default True
        seed : int, optional
            Random seed value, by default None

        Returns
        -------
        pd.DataFrame
            A dataframe with columns that are sampled values and rows that are repeated samples.
        """
        dfs = []
        for ii in np.arange(n_repeat):
            dfs.append(
                self.sample_data(
                    n_sample=n_sample,
                    count_column=count_column,
                    bin_column=bin_column,
                    weight_column=weight_column,
                    replace=replace,
                    seed=seed,
                    column_name=f"{ii}",
                ).T
            )
        out = pd.concat(dfs, axis=0)
        out.index = out.index.astype(int)
        return out

    def _aggregate_results(self, dfs, count_column, name):
        "Format the results into a single dataframe."
        df = pd.concat(dfs, ignore_index=True)
        if count_column is None:
            return df
        else:
            return df.groupby(count_column).agg(**{name: pd.NamedAgg(column=count_column, aggfunc="count")}).fillna(0)

    def _format_filter(self, columns, values):
        "Format the filter for the query method."
        filters = []
        for col, val in zip(np.atleast_1d(columns), np.atleast_1d(values)):
            if isinstance(val, str):
                filters.append(f'{col}=="{val}"')
            else:
                filters.append(f"{col}=={val}")
        return " and ".join(filters)

    def _simple_sample(self, n_sample, data_filter, replace, seed, weight):
        "Sample an individual filtered dataframe."
        if data_filter:
            dat = self._data.query(data_filter)
        else:
            dat = self._data
        return dat.sample(
            n_sample,
            replace=replace,
            random_state=seed,
            weights=weight,
        )
