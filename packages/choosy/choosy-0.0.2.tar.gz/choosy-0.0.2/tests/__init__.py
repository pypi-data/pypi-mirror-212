# SPDX-FileCopyrightText: 2023-present Casey Schneider-Mizell <caseysm@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause


import pandas as pd
import pytest

from structured_sampler import StructuredSampler

@pytest.fixture
def data():
    df = pd.DataFrame(
        {
            "column_a": ["a"]*5 + ["b"]*5,
            "sample_column": [1, 2, 3, 4, 5]*2,
        }
    )
    return df

@pytest.fixture
def sampler(data):
    return StructuredSampler(data)

