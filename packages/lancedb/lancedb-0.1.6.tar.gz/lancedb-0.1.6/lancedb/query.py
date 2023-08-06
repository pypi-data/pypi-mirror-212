#  Copyright 2023 LanceDB Developers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from __future__ import annotations

import numpy as np
import pandas as pd
import pyarrow as pa

from .common import VECTOR_COLUMN_NAME


class LanceQueryBuilder:
    """
    A builder for nearest neighbor queries for LanceDB.
    """

    def __init__(self, table: "lancedb.table.LanceTable", query: np.ndarray):
        self._metric = "L2"
        self._nprobes = 20
        self._refine_factor = None
        self._table = table
        self._query = query
        self._limit = 10
        self._columns = None
        self._where = None

    def limit(self, limit: int) -> LanceQueryBuilder:
        """Set the maximum number of results to return.

        Parameters
        ----------
        limit: int
            The maximum number of results to return.

        Returns
        -------
        The LanceQueryBuilder object.
        """
        self._limit = limit
        return self

    def select(self, columns: list) -> LanceQueryBuilder:
        """Set the columns to return.

        Parameters
        ----------
        columns: list
            The columns to return.

        Returns
        -------
        The LanceQueryBuilder object.
        """
        self._columns = columns
        return self

    def where(self, where: str) -> LanceQueryBuilder:
        """Set the where clause.

        Parameters
        ----------
        where: str
            The where clause.

        Returns
        -------
        The LanceQueryBuilder object.
        """
        self._where = where
        return self

    def metric(self, metric: str) -> LanceQueryBuilder:
        """Set the distance metric to use.

        Parameters
        ----------
        metric: str
            The distance metric to use. By default "l2" is used.

        Returns
        -------
        The LanceQueryBuilder object.
        """
        self._metric = metric
        return self

    def nprobes(self, nprobes: int) -> LanceQueryBuilder:
        """Set the number of probes to use.

        Parameters
        ----------
        nprobes: int
            The number of probes to use.

        Returns
        -------
        The LanceQueryBuilder object.
        """
        self._nprobes = nprobes
        return self

    def refine_factor(self, refine_factor: int) -> LanceQueryBuilder:
        """Set the refine factor to use.

        Parameters
        ----------
        refine_factor: int
            The refine factor to use.

        Returns
        -------
        The LanceQueryBuilder object.
        """
        self._refine_factor = refine_factor
        return self

    def to_df(self) -> pd.DataFrame:
        """
        Execute the query and return the results as a pandas DataFrame.
        In addition to the selected columns, LanceDB also returns a vector
        and also the "score" column which is the distance between the query
        vector and the returned vector.
        """
        ds = self._table.to_lance()
        tbl = ds.to_table(
            columns=self._columns,
            filter=self._where,
            nearest={
                "column": VECTOR_COLUMN_NAME,
                "q": self._query,
                "k": self._limit,
                "metric": self._metric,
                "nprobes": self._nprobes,
                "refine_factor": self._refine_factor,
            },
        )
        return tbl.to_pandas()


class LanceFtsQueryBuilder(LanceQueryBuilder):
    def to_df(self) -> pd.DataFrame:
        try:
            import tantivy
        except ImportError:
            raise ImportError(
                "Please install tantivy-py `pip install tantivy@git+https://github.com/quickwit-oss/tantivy-py#164adc87e1a033117001cf70e38c82a53014d985` to use the full text search feature."
            )

        from .fts import search_index

        # get the index path
        index_path = self._table._get_fts_index_path()
        # open the index
        index = tantivy.Index.open(index_path)
        # get the scores and doc ids
        row_ids, scores = search_index(index, self._query, self._limit)
        if len(row_ids) == 0:
            return pd.DataFrame()
        scores = pa.array(scores)
        output_tbl = self._table.to_lance().take(row_ids, columns=self._columns)
        output_tbl = output_tbl.append_column("score", scores)
        return output_tbl.to_pandas()
