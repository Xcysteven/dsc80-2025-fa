# lab.py


from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def after_purchase():
    return ['NMAR', 'MD', 'MAR', 'NMAR', 'MAR']


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def multiple_choice():
    return ['MAR', 'NMAR', 'MAR', 'NMAR', 'MCAR']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------



def first_round():
    return [0.1558, 'NR']


def second_round():
    return [0.0163, 'R', 'D']


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def verify_child(heights):
    p_values = {} 
    for col_name in heights.columns:
        if col_name.startswith('child_'):
            is_missing_mask = heights[col_name].isna()
            fathers_missing = heights.loc[is_missing_mask, 'father']

            fathers_not_missing = heights.loc[~is_missing_mask, 'father']
            
            test_result = stats.ks_2samp(fathers_missing.dropna(), 
                                           fathers_not_missing.dropna())
            
            p_values[col_name] = test_result.pvalue

    return pd.Series(p_values)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def cond_single_imputation(new_heights):
    father_quartiles = pd.qcut(new_heights['father'], q=4)
    grouped_by_quartile = new_heights['child'].groupby(father_quartiles).transform('mean')
    imputed_series = new_heights['child'].fillna(grouped_by_quartile)
    return imputed_series


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def quantitative_distribution(child, N):
    observed_heights = child.dropna()
    counts, bin_edges = np.histogram(observed_heights, bins=10)
    
    proportions = counts / counts.sum()
    
    bin_indices = np.arange(10)
    chosen_bin_indices = np.random.choice(
        a=bin_indices,
        size=N,
        p=proportions,
        replace=True 
    )
    left_edges = bin_edges[chosen_bin_indices]
    right_edges = bin_edges[chosen_bin_indices + 1]
    imputed_values = np.random.uniform(low=left_edges, high=right_edges, size=N)
    return imputed_values


def impute_height_quant(child):
    num_missing = child.isna().sum()
    nan_indices = child[child.isna()].index
    new_values = quantitative_distribution(child, num_missing)
    replacement_series = pd.Series(new_values, index=nan_indices)
    imputed_series = child.fillna(replacement_series)
    return imputed_series


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def answers():
    multiple_choice_answers = [1, 2, 2, 1]
    sites = ['https://www.w3.org/', 'https://www.facebook.com/']
    return [multiple_choice_answers, sites]
