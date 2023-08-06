# choosy

[![PyPI - Version](https://img.shields.io/pypi/v/choosy.svg)](https://pypi.org/project/choosy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/choosy.svg)](https://pypi.org/project/choosy)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install choosy
```

## Usage

### Sampling
`choosy` is designed to make it easy to do selective sampling from a Pandas dataframe.
The main work is handled by the `StructuredSampler` class, which holds a dataframe and
optional information about informative columns.

```python
import pandas as pd
import choosy

df = pd.DataFrame(
        {
            "category_col": ["a"]*5 + ["b"]*5,
            "value_col": [1, 2, 3, 4, 5]*2,
        }
)

sampler = choosy.StructuredSampler(
    df,
)
```

The most simple case is that you want to sample `n` rows from a dataframe.
Frankly, in that simple case you should just use the native `df.sample()`
method, but `choosy` can do that too:

```python
sampler.sample_data(n_sample=3)
```

will return 3 random rows.

The real use of `choosy` comes from the ability to sample rows based on values in a column.
Let's say we want to sample 2 rows with value `a` in `category_col` and 1 row with value `b`.
Instead of an integer for `n_sample`, we use a dictionary mapping values to the number of samples from rows with that value.
In addition, we define a `bin_column` that will be the column in which to find those values.

```python
sampler.sample_data(n_sample={'a': 2, 'b': 1}, bin_column="category_col")
```

Now you will get three rows, one with value `b` and two with value `a`. 
Note that it will only sample from those values specified, which may mean that some rows with values other than keys in the dictionary are never potentially sampled.
If you specify a `bin_column` but `n_sample` is an integer, it will sample that many values from each unique value in the `bin_column`.

If you want to sample based on the unique combination of values in multiple columns, you can specify a list of `bin_columns` and keys can be a tuple of sample selection values in the same order.
Alternatively, you can use a pandas Series whose index is the sample selection values and whose elements are the number of samples to take from that value.
The second case is useful if you have, for example, a dataframe with observations and second baseline dataframe that you want to sample from with the same frequencies based on some value.
Here, you can use the `groupby` method to get the number of samples to take from each value.

```python
n_sample = df_obs.groupby(['selection_column_1', 'selection_column_2'])['selection_column_2'].count()]
sampler = choosy.StructuredSampler(df_baseline)
df_sample = sampler.sample_data(
    n_sample=n_sample,
    bin_column=['selection_column_1', 'selection_column_2'],
)
```

### Counting and Repeat Sampling

In all cases above, the `sample_data` method returns a dataframe with the sampled rows.
In many applications, the main thing you want to know is the number of observations of some other value in the dataframe.
By adding a `count_column` argument, to any of the situations described above, you get a dataframe with the sampled counts of the values in that column.
This is fully equivalent to doing a `groupby().count()` on the results of the `sample_data` method.

```python

```python
df = pd.DataFrame(
        {
            "category_col": ["a"]*5 + ["b"]*5,
            "value_col": [1, 2, 3, 4, 5]*2,
        }
)

sampler = choosy.StructuredSampler(
    df,
    count_column='value_col',
)

# Sample and get the list of observations of each value from category_col.
sampler.sample_data(
    n_sample={'a': 2, 'b': 1},
    count_column='value_col',
    bin_column='category_col',
)
```

To get `n_repeat` sample distributions of a given count variable, you can use the `sample_repeat` method.
You are required to specify a `count_column` for this method, and you can specify a `bin_column` and `n_sample` as described above.
For example, to do 1000 repeats of the sampling above:

```python

sampler.sample_repeat(
    n_repeat=1000,
    n_sample={'a': 2, 'b': 1},
    count_column='value_col',
    bin_column='category_col',
)

```

### Notes

* If you plan to always sample using the same `bin_column`, you can also specify this value in the `StructuredSampler` constructor.
This will save you from having to specify it in every call to `sample_data`.

* You can also specify a `weight_column` in either the constructor or the `sample_data`/`sample_repeat` methods to weight the sampling by the values in that column, which is passed through the `pd.sample`.

* By default, `choosy` uses sampling with replacement unless `replace=False` is specified in methods.

* A `seed` can be specified in the methods to make the sampling reproducible.

* The code is primarily for convenience for flexible sampling from the same dataframe, and has not been optimized for speed at this time.

## License

`choosy` is distributed under the terms of the [BSD 3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
