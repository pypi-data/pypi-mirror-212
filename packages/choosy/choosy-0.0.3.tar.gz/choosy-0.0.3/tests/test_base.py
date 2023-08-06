import pytest
from . import data, sampler

def test_simple_sample(sampler):
    n = 3
    df_test = sampler.sample_data(n)
    assert len(df_test) == n

def test_simple_per_value(sampler):
    n=3
    df_test = sampler.sample_data(
        n_sample=n,
        bin_column="column_a",
    )
    assert len(df_test) == n*2

def test_varied_sample(sampler):
    a = 2
    b = 4
    df_test = sampler.sample_data(
        n_sample={"a": a, "b": b},
        bin_column="column_a",
        count_column="sample_column",
    )
    assert df_test["sample_count"].sum() == a+b

def test_repeat_sample(sampler):
    n_rep = 100
    df = sampler.sample_repeat(
        n_repeat = n_rep,
        n_sample = {"a": 2, "b": 3},
        count_column = "sample_column",
        bin_column = "column_a",
    )
    assert len(df) == n_rep