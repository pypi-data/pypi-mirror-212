# SPDX-FileCopyrightText: 2023-present Casey Schneider-Mizell <caseysm@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause


import pandas as pd
import pytest
import os

# Add the parent directory to the path so we can import from src

os.sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.choosy import StructuredSampler

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

