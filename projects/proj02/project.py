# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pd.options.plotting.backend = 'plotly'

from IPython.display import display

# DSC 80 preferred styles
pio.templates["dsc80"] = go.layout.Template(
    layout=dict(
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=True,
        width=600,
        height=400,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        title=dict(x=0.5, xanchor="center"),
    )
)
pio.templates.default = "simple_white+dsc80"
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def clean_loans(loans):
    temp_df = loans.copy()
    temp_df['term'] = temp_df.term.str.split(' ').map(lambda x: int(x[1]))

    temp_df['issue_d'] = pd.to_datetime(temp_df['issue_d'])

    temp_df['emp_title'] = temp_df['emp_title'].str.lower().str.strip().replace('rn', 'registered nurse')

    temp_df['term_end'] = temp_df.apply(
        lambda row: row['issue_d'] + pd.DateOffset(months=row['term']),
        axis=1)
    
    return temp_df


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def correlations(df, pairs):
    corr_values = []
    index_labels = []

    for col1, col2 in pairs:
        corr = df[col1].corr(df[col2])
        corr_values.append(corr)
        index_labels.append(f'r_{col1}_{col2}')

    return pd.Series(corr_values, index=index_labels)



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def create_boxplot(loans):
    df_plot = loans.copy()
    bins = [580, 670, 740, 800, 850]

    df_plot['fico_bin'] = pd.cut(df_plot['fico_range_low'],
                                 bins=bins,
                                 right=False)
    df_plot['fico_bin_str'] = df_plot['fico_bin'].astype(str)

    df_plot['term_in_months'] = df_plot['term'].astype(str)

    fig = px.box(
        df_plot,
        x='fico_bin_str',
        y='int_rate',
        color='term_in_months',
        title="Interest Rate vs. Credit Score",
        labels={
            'fico_bin_str': 'Credit Score Range',
            'int_rate': 'Interest Rate (%)',
            'term_in_months': 'Loan Length (Months)'
        },
        color_discrete_map={
            '36': 'purple',
            '60': 'gold'
        }
    )

    return fig


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def ps_test(loans, N):
    df_test = loans[['desc', 'int_rate']].copy()
    df_test['has_ps'] = df_test['desc'].notna()
    rates_with_ps = df_test[df_test['has_ps']]['int_rate']
    rates_without_ps = df_test[~df_test['has_ps']]['int_rate']
    observed_stat = rates_with_ps.mean() - rates_without_ps.mean()

    all_rates = df_test['int_rate'].values
    n_with_ps = len(rates_with_ps)
    simulated_stats = []
    
    for i in range(N):
        shuffled_rates = np.random.permutation(all_rates)
        sim_rates_with_ps = shuffled_rates[:n_with_ps]
        sim_rates_without_ps = shuffled_rates[n_with_ps:]
        sim_stat = sim_rates_with_ps.mean() - sim_rates_without_ps.mean()
        simulated_stats.append(sim_stat)
    
    simulated_stats = np.array(simulated_stats)
    p_value = (simulated_stats >= observed_stat).mean()
    
    return p_value

def missingness_mechanism():
    return 2
    
def argument_for_nmar():
    '''
    Put your justification here in this multi-line string.
    Make sure to return your string!
    '''

    return "The behavior of writing a personal statement, might reflect the use of the loan and their personal backgrounds, which is not reflected through this dataset. Those points are the hiddle metrics of dicision making of who is getting the loans"


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def tax_owed(income, brackets):
    total = 0.0
    for i in range(len(brackets)):
        current_rate, current_lower = brackets[i]

        if income <= current_lower:
            break

        if i + 1 < len(brackets):
            next_lower = brackets[i+1][1]
        else:
            next_lower = income

        tax = (min(next_lower, income) - current_lower) * current_rate

        total += tax 
    return total


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def clean_state_taxes(state_taxes_raw): 
    temp_df = state_taxes_raw.dropna(how='all')
    temp_df['State'] = temp_df['State'].where(~temp_df['State'].str.startswith('(', na=False), np.nan).ffill()
    temp_df['Rate'] = temp_df['Rate'].replace('none', '0.0').apply(lambda x: np.round((float(x[:-1]) / 100), decimals=2))
    temp_df['Lower Limit'] = temp_df['Lower Limit'].fillna(0).apply(lambda x: int(x[1:].replace(',', '')) if type(x) == str else x)

    return temp_df
    


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def state_brackets(state_taxes):
    temp_df = state_taxes.groupby('State').agg(list)
    temp_df['bracket_list'] = temp_df.apply((lambda x: list(zip(x['Rate'], x['Lower Limit']))), axis=1)
    return temp_df.get(['bracket_list'])
    
def combine_loans_and_state_taxes(loans, state_taxes):
    # Start by loading in the JSON file.
    # state_mapping is a dictionary; use it!
    import json
    state_mapping_path = Path('data') / 'state_mapping.json'
    with open(state_mapping_path, 'r') as f:
        state_mapping = json.load(f)
        temp_state = state_brackets(state_taxes).copy().reset_index()
        temp_state['State'] = temp_state['State'].apply(lambda x: state_mapping[x])
        temp_loan = loans.copy()
        temp_final_df = pd.merge(temp_state, temp_loan, left_on='State', right_on='addr_state').drop(columns='addr_state')
    return temp_final_df
        


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def find_disposable_income(loans_with_state_taxes):
    FEDERAL_BRACKETS = [
     (0.1, 0), 
     (0.12, 11000), 
     (0.22, 44725), 
     (0.24, 95375), 
     (0.32, 182100),
     (0.35, 231251),
     (0.37, 578125)
    ]
    temp_df = loans_with_state_taxes.copy()
    temp_df['federal_tax_owed'] = temp_df.apply(lambda x: tax_owed(x['annual_inc'], FEDERAL_BRACKETS), axis = 1)
    temp_df['state_tax_owed'] = temp_df.apply(lambda x: tax_owed(x['annual_inc'], x['bracket_list']), axis = 1)
    temp_df['disposable_income'] = temp_df['annual_inc'] - temp_df['federal_tax_owed'] - temp_df['state_tax_owed']
    
    return temp_df


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def aggregate_and_combine(loans, keywords, quantitative_column, categorical_column):
    dfs_to_merge = []
    for keyword in keywords:
        df_filtered = loans[loans['emp_title'].str.contains(keyword, na=False)]
        per_category_means = df_filtered.groupby(categorical_column)[quantitative_column].mean()
        col_name = f'{keyword}_mean_{quantitative_column}'
        keyword_df = per_category_means.to_frame(col_name)
        overall_mean = df_filtered[quantitative_column].mean()
        keyword_df.loc['Overall'] = overall_mean
        dfs_to_merge.append(keyword_df)

    # print(dfs_to_merge)
    final_df = dfs_to_merge[0].merge(dfs_to_merge[1], left_index=True, right_index=True)
    # print(final_df)
    final_df.index.name = categorical_column
    
    return final_df

# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def exists_paradox(loans, keywords, quantitative_column, categorical_column):
    results_df = aggregate_and_combine(loans, keywords, quantitative_column, categorical_column)
    case1 = (results_df.iloc[:-1, 0] > results_df.iloc[:-1, 1]).all() and \
            (results_df.iloc[-1, 0] < results_df.iloc[-1, 1])
    
    case2 = (results_df.iloc[:-1, 0] < results_df.iloc[:-1, 1]).all() and \
            (results_df.iloc[-1, 0] > results_df.iloc[-1, 1])
    
    return bool(case1 or case2)

def paradox_example(loans):
    return {
        'loans': loans,
        'keywords': ['manager', 'teacher'],
        'quantitative_column': 'loan_amnt',
        'categorical_column': 'verification_status'
    } 
