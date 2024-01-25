import numpy as np
from fuzzy.membership import fuzzify_output_very_small, fuzzify_output_small, fuzzify_output_big, fuzzify_output_verry_big

rules_str = {'1': 'if X1 is DARK and X2 is PS then DM is B',
             '2': 'if X1 is DARK and X2 is ZE then DM is B',
             '3': 'if X1 is DARK and X2 is NS then DM is VB',
             '4': 'if X1 is MEDIUM and X2 is PS then DM is S',
             '5': 'if X1 is MEDIUM and X2 is ZE then DM is B',
             '6': 'if X1 is MEDIUM and X2 is NS then DM is B',
             '7': 'if X1 is LIGHT and X2 is PS then DM is VS',
             '8': 'if X1 is LIGHT and X2 is ZE then DM is S',
             '9': 'if X1 is LIGHT and X2 is NS then DM is B',
            }

VERY_SMALL_OUT = [7]  # Numbers of rule that output FAN is LOW
SMALL_OUT = [4, 8]    # Numbers of rule that output FAN is MEDIUM
BIG_OUT = [1,2, 5, 6, 9]  # Numbers of rule that output FAN is HIGH
VERY_BIG_OUT = [3]

def get_label(var: str, r_num: int, pos: int):
    if var == 'X1':
        if 1 <= r_num <= 3 and pos == 1:
            return 'DARK'
        elif 4 <= r_num <= 6 and pos == 2:
            return 'MEDIUM'
        elif 7 <= r_num <= 9 and pos == 3:
            return 'LIGHT'
    elif var == 'X2':
        if r_num % 3 == 1 and pos == 1:
            return 'PS'
        elif r_num % 3 == 2 and pos == 2:
            return 'ZE'
        elif r_num % 3 == 0 and pos == 3:
            return 'NS'
    elif var == 'DM':
        if r_num in VERY_SMALL_OUT and pos == 1:
            return 'VS'
        elif r_num in SMALL_OUT and pos == 2:
            return 'S'
        elif r_num in BIG_OUT and pos == 3:
            return 'B'
        elif r_num in VERY_BIG_OUT and pos == 4:
            return 'VB'
    return ''

def get_color(var: str, r_num: int, pos: int):
    if var == 'X1':
        if 1 <= r_num <= 3 and pos == 1:
            return 'r'
        elif 4 <= r_num <= 6 and pos == 2:
            return 'r'
        elif 7 <= r_num <= 9 and pos == 3:
            return 'r'
        else:
            return '0.85'
    elif var == 'X2':
        if r_num % 3 == 1 and pos == 1:
            return 'r'
        elif r_num % 3 == 2 and pos == 2:
            return 'r'
        elif r_num % 3 == 0 and pos == 3:
            return 'r'
        else:
            return '0.85'
    elif var == 'DM':
        if r_num in VERY_SMALL_OUT and pos == 1:
            return 'r'
        elif r_num in SMALL_OUT and pos == 2:
            return 'r'
        elif r_num in BIG_OUT and pos == 3:
            return 'r'
        elif r_num in VERY_BIG_OUT and pos == 4:
            return 'r'
        else:
            return '0.85'
    return '0.85'

def get_z(var: str, r_num: int, pos: int):
    if var == 'X1':
        if 1 <= r_num <= 3 and pos == 1:
            return 10
        elif 4 <= r_num <= 6 and pos == 2:
            return 10
        elif 7 <= r_num <= 9 and pos == 3:
            return 10
    elif var == 'X2':
        if r_num % 3 == 1 and pos == 1:
            return 10
        elif r_num % 3 == 2 and pos == 2:
            return 10
        elif r_num % 3 == 0 and pos == 3:
            return 10
    elif var == 'DM':
        if r_num in VERY_SMALL_OUT and pos == 1:
            return 10
        elif r_num in SMALL_OUT and pos == 2:
            return 10
        elif r_num in BIG_OUT and pos == 3:
            return 10
        elif r_num in VERY_BIG_OUT and pos == 4:
            return 10
    return 0

def fill_DM(r_num: int, alpha: float):
    x = np.array([int(i) for i in range(10)])
    y = []
    if r_num in VERY_SMALL_OUT:
        for _x in x:
            temp = fuzzify_output_very_small(_x)
            if temp >= alpha:
                temp = alpha
            y.append(temp)
    elif r_num in SMALL_OUT:
        for _x in x:
            temp = fuzzify_output_small(_x)
            if temp >= alpha:
                temp = alpha
            y.append(temp)
    elif r_num in BIG_OUT:
        for _x in x:
            temp = fuzzify_output_big(_x)
            if temp >= alpha:
                temp = alpha
            y.append(temp)
    elif r_num in VERY_BIG_OUT:
        for _x in x:
            temp = fuzzify_output_verry_big(_x)
            if temp >= alpha:
                temp = alpha
            y.append(temp)
    y = np.array(y)
    return x, y
