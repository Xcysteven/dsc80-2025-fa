# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):
    final = {'lab':[],
             'project':[],
             'midterm':[],
             'final':[],
             'disc':[],
             'checkpoint':[]
             }
    for i in list(grades.columns.drop(['PID', 'College', 'Level', 'Section'])):
        if 'Max' not in i and 'Lateness' not in i:
            # print(i)
            if ('lab' in i):
                final['lab'].append(i)
            elif ('Midterm' in i):
                final['midterm'].append(i)
            elif ('Final' in i):
                final['final'].append(i)
            elif ('disc' in i):
                final['disc'].append(i)
            elif ('checkpoint' in i):
                final['checkpoint'].append(i)
            elif ('project' in i):
                final['project'].append(i)
    return final


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):
    person_score = grades.loc[:, grades.columns.str.contains('project')]
    person_score = person_score.filter(regex='^((?! - Lateness|checkpoint).)*$')
    final = list(np.zeros(grades.shape[0]))
    for i in range(int(int(person_score.columns.to_list()[-1][7:9]))):
        scores = person_score.get(f'project0{i+1}').fillna(0)
        max_single_score = person_score[f'project0{i+1} - Max Points'].take([0]).to_list()[0]
        if (f'project0{i+1}_free_response' in person_score):
            free_scores = person_score.get(f'project0{i+1}_free_response').fillna(0)
            max_free_response = person_score[f'project0{i+1}_free_response - Max Points'].take([0]).to_list()[0]
            scores = scores + free_scores
            max_single_score = max_single_score + max_free_response
        grade = scores / max_single_score
        final += grade * 0.2
    
    return pd.Series(final)
    
        
    


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(col):
    lst = col.to_list()
    final = []
    for i in lst:
        split = i.split(':')
        hours = int(split[0])
        mi = int(split[1])
        sec = int(split[2])
        if (hours < 2) or (hours == 2 and mi == 0 and sec == 0):
            final.append(1.0)
        elif (hours < 7*24) or (hours == 7*24 and mi == 0 and sec ==0):
            final.append(0.9)
        elif (hours < 14*24) or (hours == 14*24 and mi == 0 and sec == 0):
            final.append(0.7)
        else:
            final.append(0.4)
    return pd.Series(final, index=col.index)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    lst = ['lab01','lab02','lab03','lab04','lab05','lab06','lab07','lab08','lab09']
    lateness = ' - Lateness (H:M:S)'
    max_points = ' - Max Points'
    final = {}
    for i in lst:
        late = i + lateness
        penalty = lateness_penalty(grades[late])
        original_score = grades[i].fillna(0)
        max_score = grades[i+max_points]
        after_penalty = original_score * penalty / max_score
        final[i] = after_penalty

    return pd.DataFrame(final, index=grades.index)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):
    size = processed.shape
    final = []
    for i in range(size[0]):
        adjusted_sum = processed.take([i]).sum(axis=1) - processed.take([i]).min(axis=1)
        final_weight = (adjusted_sum / (size[1]-1)).iloc[0]
        final.append(final_weight)
    return pd.Series(final, index=processed.index)

# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    assignments = get_assignment_names(grades)
    project_subgrade = projects_total(grades)
    lab_subgrade = lab_total(process_labs(grades))
    midterm_subgrade = grades['Midterm'].fillna(0) / grades['Midterm - Max Points']
    final_subgrade = grades['Final'].fillna(0) / grades['Final - Max Points']
    
    disc_subgrade = pd.Series(np.zeros(len(midterm_subgrade)), index=midterm_subgrade.index)
    max_points = ' - Max Points'

    for i in assignments['disc']:
        scores = grades[i].fillna(0) / grades[i+max_points]
        disc_subgrade += scores.to_list()
    disc_subgrade = disc_subgrade / len(assignments['disc'])
    
    check_subgrade = pd.Series(np.zeros(len(midterm_subgrade)), index=midterm_subgrade.index)
    for i in assignments['checkpoint']:
        scores = grades[i].fillna(0) / grades[i+max_points]
        check_subgrade += scores.to_list()
    check_subgrade = check_subgrade / len(assignments['checkpoint'])

    final_score = project_subgrade * 0.3 + lab_subgrade * 0.2 + midterm_subgrade * 0.15 + final_subgrade * 0.3 + check_subgrade * 0.025 + disc_subgrade * 0.025
    return final_score
    
    
    
    


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    def helper(indiv):
        if indiv >= 0.9:
            return 'A'
        elif indiv >= 0.8:
            return 'B'
        elif indiv >= 0.7:
            return 'C'
        elif indiv >= 0.6:
            return 'D'
        else:
            return 'F'
    
    return total.apply(helper)

def letter_proportions(total):
    final_series = final_grades(total).value_counts() / len(total)
    ideal = ['A', 'B', 'C', 'D', 'F']
    if len(final_series != 5):
        diff = [i for i in ideal if i not in final_series.index.to_list()]
        final_series = pd.concat([final_series, pd.Series(np.zeros(len(diff)), index=diff)])
    return final_series.sort_values(ascending=False)
    

# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    final_breakdown = final_breakdown.fillna(0)
    PIDs = final_breakdown.iloc[:, [0]].copy()
    redemption_questions = final_breakdown.iloc[:, question_numbers].copy()
    
    max_points = redemption_questions.columns.str.split(' ')
    max_points = [float(i[2][1:]) for i in max_points]
    total_redeption_points = sum(max_points)
    raw_redemtpion_points = redemption_questions.sum(axis = 1) / total_redeption_points
    PIDs['Raw Redemption Score'] = raw_redemtpion_points
    return PIDs
    
    
def combine_grades(grades, raw_redemption_scores):
    return pd.merge(grades, raw_redemption_scores, on='PID')


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    return (ser - np.mean(ser)) / np.std(ser)
    
def add_post_redemption(grades_combined):
    z_scores = z_score(grades_combined['Raw Redemption Score'].fillna(0))
    midterm_pre = grades_combined['Midterm'].fillna(0) / grades_combined['Midterm - Max Points']
    new_df = grades_combined.copy()
    new_df['Midterm Score Pre-Redemption'] = midterm_pre
    mean = np.mean(midterm_pre)
    sd = np.std(midterm_pre)
    midterm_post = z_scores * sd + mean
    midterm_post_real = np.maximum(midterm_pre, midterm_post)
    midterm_post_real_real = [i if i <= 1 else 1 for i in midterm_post_real]
    new_df['Midterm Score Post-Redemption'] = midterm_post_real_real
    return new_df




# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    temp_df = add_post_redemption(grades_combined)
    return total_points(grades_combined) + (temp_df['Midterm Score Post-Redemption'] - temp_df['Midterm Score Pre-Redemption']) * 0.15
        
def proportion_improved(grades_combined):
    grade_after = total_points_post_redemption(grades_combined) // 0.1
    
    grade_before = total_points(grades_combined) // 0.1
    diff = grade_after - grade_before
    # print(grade_after)
    # print(grade_before)
    return np.count_nonzero(diff) / diff.count()


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    sections = grades_analysis['Section'].unique()
    sections_improved = []
    for sec in sections:
        temp_df = grades_analysis[grades_analysis['Section'] == sec]
        sections_improved.append(proportion_improved(temp_df))
    return sections[np.argmax(sections_improved)]
        
    
def top_sections(grades_analysis, t, n):
    sections = grades_analysis['Section'].unique()
    sect_final = []
    final_max = grades_analysis['Final - Max Points'].to_list()[0]
    for sec in sections:
        temp_list = grades_analysis[grades_analysis['Section'] == sec]
        greater_threshold = (temp_list.Final / final_max) >= t
        if sum(greater_threshold) >= n:
            sect_final.append(sec)
    return np.array(sect_final)


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    sections = grades_analysis['Section'].unique()
    temp_dict = {}
    for sect in sorted(sections):
        temp_dict[sect] = grades_analysis[grades_analysis['Section'] == sect].sort_values('Total Points Post-Redemption', ascending=False).reset_index().PID
    final_df = pd.DataFrame(temp_dict).fillna('')
    final_df = final_df.melt(var_name='Section', value_name='PID')
    final_df['Section Rank'] = final_df.groupby('Section').cumcount() + 1
    return final_df.pivot(index='Section Rank', columns='Section', values='PID')   
    


# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    row_name = ['A', 'B', 'C', 'D', 'E']
    col_name = sorted(grades_analysis['Section'].unique())
    final_dict = {}
    for sec in col_name:
        final_letter_grade_prop = letter_proportions(grades_analysis[grades_analysis['Section'] == sec]['Total Points Post-Redemption'])
        final_dict[sec] = final_letter_grade_prop
    final_df = pd.DataFrame(final_dict)
    fig = px.imshow(final_df, 
                    labels = dict(x="Section", y="Letter Grade Post-Redemption", color="color"),
                    title = 'Distribution of Letter Grades by Section',
                    color_continuous_scale='Blues'
                    )
    return fig
