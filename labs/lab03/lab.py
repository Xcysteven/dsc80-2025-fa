# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def read_linkedin_survey(dirname):
    dir_path = Path(dirname)
    if not dir_path.is_dir():
        raise FileNotFoundError()
    
    csv_files = list(dir_path.glob('survey*.csv'))

    if not csv_files:
        return pd.DataFrame(columns=[
            'first name', 'last name', 'current company', 'job title', 'email', 'university'
        ])

    df_list = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(df_list, ignore_index=False)

    final_columns = [
        'first name',
        'last name',
        'current company',
        'job title',
        'email',
        'university'
    ]

    output_df = combined_df[final_columns]
    output_df = output_df.reset_index(drop=True).fillna('')

    return output_df


def com_stats(df):
    ohio = df[df['university'].str.contains('Ohip') & df['job title'].str.contains('Programmer')].shape
    ohio_porp = ohio[0] / df.shape[0]

    eng = df[df['job title'].str.endswith('engineer')].shape
    eng_num = eng[0]

    longest = df[df['job title'].str.len() == df['job title'].str.len().max()]['job title'].to_list()[0]

    manager = df['job title'].apply(lambda x: str.lower(x)).str.contains('manager').sum() / df.shape[0]

    return [ohio_porp, eng_num, longest, manager]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def read_student_surveys(dirname):
    dir_path = Path(dirname)

    base_file = dir_path / 'favorite1.csv'

    if not base_file.exists():
        raise FileNotFoundError()

    combined_df = pd.read_csv(base_file)
    survey_files = dir_path.glob('favorite*.csv')

    for file_path in survey_files:
        if file_path.name == 'favorite1.csv':
            continue

        survey_data = pd.read_csv(file_path)

        combined_df = pd.merge(combined_df, survey_data, on='id', how='left')

    combined_df = combined_df.set_index('id').fillna('')

    return combined_df



def check_credit(df):
    name = df['name']
    temp_df = df.drop(columns= ['name'])
    temp_df = temp_df.map(lambda x: 0 if x == '' else 1)

    ecsum_vert = ((temp_df.sum(axis = 0)) > (df.shape[0] * 0.9)).sum()

    if ecsum_vert > 2:
        ecsum_vert = 2
    
    ecsum_hori = (temp_df.sum(axis = 1) > (temp_df.shape[1] // 2)) * 5 + ecsum_vert

    final_dict = {'name': name.to_list(), 
                  'ec': ecsum_hori.to_list()}
    return pd.DataFrame(final_dict, index=name.index)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):
    temp_df = pd.merge(procedure_history, pets, on='PetID')
    temp_df = temp_df['ProcedureType'].value_counts()

    return temp_df.index[0]
    
def pet_name_by_owner(owners, pets):
    return pd.merge(owners, pets, on='OwnerID').groupby(['OwnerID', 'Name_x'])['Name_y'].agg(list).droplevel(0).map(lambda x: x[0] if len(x) == 1 else x)


def total_cost_per_city(owners, pets, procedure_history, procedure_detail):
    owners_pets = pd.merge(owners, pets, on='OwnerID')
    owners_pets_history = pd.merge(owners_pets, procedure_history, on='PetID')
    full_data = pd.merge(owners_pets_history, procedure_detail, on=['ProcedureType', 'ProcedureSubCode'])
    city_costs = full_data.groupby('City')['Price'].sum()
    all_cities = owners['City'].unique()
    total_costs = city_costs.reindex(all_cities, fill_value=0)
    return total_costs
    


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def average_seller(sales):
    return sales.groupby('Name')['Total'].mean().reset_index().set_index('Name').rename(columns={'Total': 'Average Sales'})

def product_name(sales):
    return sales.groupby(['Name', 'Product'])['Total'].sum().reset_index().pivot(columns='Product',index='Name',values='Total')

def count_product(sales):
    return sales.groupby(['Product', 'Name', 'Date']).count().reset_index().pivot(columns=['Date'], index=['Product', 'Name'], values='Total').fillna(0)

def total_by_month(sales):
    temp_df = sales.copy() 
    temp_df['Month'] = pd.to_datetime(temp_df['Date']).dt.strftime('%B')

    return pd.pivot_table(temp_df,
                          index = ['Name', 'Product'],
                          columns = 'Month',
                          values = 'Total',
                          aggfunc = 'sum',
                          fill_value=0)
