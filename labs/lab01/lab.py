# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False

    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True

    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    mean = sum(nums)/len(nums)
    if (len(nums) % 2 == 1):
        median = nums[len(nums) // 2]
    else:
        median = (nums[len(nums)//2] + nums[len(nums)//2 + 1]) / 2
    return median <= mean

# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    f = ""
    for k in range(n+1):
        f = s[:k] + f
    return f


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    max_num = max(ints) + n
    width = len(str(max_num))
    result = []
    for num in ints:
        exploded_seq = range(num - n, num + n + 1)
        length = [str(x).zfill(width) for x in exploded_seq]
        final = ' '.join(length)
        result.append(final)
    return result


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def last_chars(fh):
    final = ""
    f = fh.read()
    splitted = f.split("\n")
    for k in splitted:
        if k:
            last = k[-1]
            final = final + last
    return final


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    return (A + np.sqrt(np.where(A)))[0]

def where_square(A):
    return np.square(np.floor(np.sqrt(A))) == A


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_loop(matrix, cutoff):
    average = []
    rows = len(matrix)
    col = len(matrix[0])
    for k in range(col):
        sum = 0
        for i in range(rows):
            sum += matrix[i][k]
        if sum//rows > cutoff:
            average.append(k)

    return np.array([[row[j] for j in average] for row in matrix])


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_np(matrix, cutoff):
    rows = len(matrix)
    col = len(matrix[0])
    average = np.mean(matrix, axis = 0) > cutoff
    return matrix[:, average]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    return np.round(np.diff(A) / np.resize(A, len(A) - 1), 2)

def with_leftover(A):
    money = np.zeros(len(A)) + 20
    leftover = np.array([])
    leftover = money % A
    csum = np.cumsum(leftover) 
    day = csum >= A
    return len(day) - np.count_nonzero(day)


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    final = []
    final.append(salary["Player"].nunique())
    final.append(salary["Team"].nunique())
    final.append(salary["Salary"].sum())
    final.append(salary["Salary"].max())
    final.append(salary[salary["Team"] == "Los Angeles Lakers"]["Salary"].mean())
    fifth_lowest = salary[["Salary", "Player", "Team"]].sort_values("Salary", ascending=True).reset_index().take([4])
    final.append(f'{list(fifth_lowest.Player)[0]}, {list(fifth_lowest.Team)[0]}')
    final.append(len([s.split()[1] for s in list(salary.Player)]) == len(salary.Player))

    team = list(salary[salary["Salary"] == salary.Salary.max()]["Team"])[0]

    final.append(salary[salary["Team"] == team]["Salary"].sum())

    index = ['num_players', 'num_teams', 'total_salary', 'highest_salary', 'avg_los', 'fifth_lowest', 'duplicates', 'total_highest']
    return pd.Series(final, index=index)


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    data = []
    with open(fp, 'r') as file:
        headings = file.readline().strip("\n").split(",")
        row_dict = {}
        row_dict = dict.fromkeys(headings)
        print(row_dict)
        

        for line in file:
            cleaned_line = line.strip().replace('"', '')
            parts = cleaned_line.split(',')
            finished_parts = [i for i in parts if i != ""]
            print(finished_parts)
            row_dict = {
                    'first': finished_parts[0],
                    'last': finished_parts[1],
                    'weight': float(finished_parts[2]),
                    'height': float(finished_parts[3]),
                    'geo': f'{finished_parts[4]},{finished_parts[5]}'
            }
            data.append(row_dict)

    return pd.DataFrame(data)

            
    
