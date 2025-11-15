# lab.py


import pandas as pd
import numpy as np
import io
from pathlib import Path
import os


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def prime_time_logins(login):
    temp_df = login.copy()
    temp_series = pd.to_datetime(login['Time']).dt.hour

    temp_df['is_prime_time'] = (temp_series >= 16) & (temp_series < 20)

    final_series = temp_df.groupby('Login Id')['is_prime_time'].sum()

    return final_series.to_frame(name='Time')


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def count_frequency(login):
    def helper(series):
        total_logins = series.size
        tod = pd.to_datetime('2024-01-31 23:59:00')
        first_login = series.min()
        diff = tod - first_login
        days = diff.days
        days_adjusted = max(1, days)
        return total_logins / days_adjusted
    
    temp_df = login.copy()
    temp_df['Time'] = pd.to_datetime(temp_df['Time'])
    freq = temp_df.groupby('Login Id')['Time'].agg(helper)
    return freq


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def cookies_null_hypothesis():
    return [1,2]
                         
def cookies_p_value(N):
    p_null = 0.04
    n = 250
    observed = 15
    
    simulated_stats = np.random.binomial(n=n, p=p_null, size=N)
    p_value = np.mean(simulated_stats >= observed)

    return p_value


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def car_null_hypothesis():
    return [1,4]

def car_alt_hypothesis():
    return [2,6]

def car_test_statistic():
    return [1,4]

def car_p_value():
    return 4


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def superheroes_test_statistic():
    return [1]
    
def bhbe_col(heroes):
    blond = heroes['Hair color'].str.contains('blond', case=False, na=False)
    blue = heroes['Eye color'].str.contains('blue', case=False, na=False)
    return blond & blue

def superheroes_observed_statistic(heroes):
    bhbe = bhbe_col(heroes)
    bhbe_alignments = heroes.loc[bhbe, 'Alignment']
    observed_stat = (bhbe_alignments == 'good').mean()
    return observed_stat

def simulate_bhbe_null(heroes, N):
    p_null = (heroes['Alignment'] == 'good').mean()
    n_bhbe = bhbe_col(heroes).sum()
    simulated_counts = np.random.binomial(n=n_bhbe, p=p_null, size=N)
    simulated_stats = simulated_counts / n_bhbe
    return simulated_stats
    

def superheroes_p_value(heroes):
    n = 100000
    obs_stat = superheroes_observed_statistic(heroes)
    null_stats = simulate_bhbe_null(heroes, n)
    p = np.mean(null_stats >= obs_stat)
    if (p < 0.01):
        return [p, 'Reject']
    return [p, 'Fail to reject']


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def diff_of_means(data, col='orange'):
    york = data[data['Factory'] == 'Yorkville'][col].mean()
    waco = data[data['Factory'] == 'Waco'][col].mean()

    return np.abs(york - waco)


def simulate_null(data, col='orange'):
    shuffled_df = data.copy()
    shuffled_df['Factory'] = np.random.permutation(shuffled_df['Factory'])
    return diff_of_means(shuffled_df, col)


def color_p_value(data, col='orange'):
    n = 1000
    observed_stat = diff_of_means(data, col)
    simulated_stats = np.array([simulate_null(data, col) for i in range(n)])
    p_value = np.mean(simulated_stats >= observed_stat)
    return p_value


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def ordered_colors():
    return [('yellow', np.float64(0.0)), ('orange', np.float64(0.04)), ('red', np.float64(0.246)), ('green', np.float64(0.464)), ('purple', np.float64(0.981))]


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


    
def same_color_distribution():
    return (0.007, 'Reject')


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def perm_vs_hyp():
    return ['P', 'P', 'H', 'H', 'P']
