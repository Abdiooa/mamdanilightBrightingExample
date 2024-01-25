import numpy as np
from fuzzy.defuzzifier import Defuzzifier
from fuzzy.fuzzifier import gen_output_membership
from utils.plot_util import VERY_SMALL_OUT, SMALL_OUT, BIG_OUT, VERY_BIG_OUT

class FuzzyInferenceSystem:

    '''
    Система нечеткого вывода является ключевым элементом системы нечеткой логики, 
    основной работой которой является принятие решений. Она использует правила 
    “ЕСЛИ... ТО” вместе с соединителями “ИЛИ”, “или”И" для 
    составления основных правил принятия решений.

    Нечеткая система вывода для управления яркостью лампы на основе нечеткой логики.
    Система принимает входные переменные (интенсивность окружающего света и его скорость изменения) и генерирует
    управляющий выход для регулировки яркости лампы.

    Для каждой входной и выходной переменной определены функции принадлежности и правила.
    '''
    def __init__(self) -> None:
        pass


    '''
    ПРАВИЛА
    d* Вывод нечеткой области
    1 - если X1 ТЕМНЫЙ, а X2 - PS, то D равен B
    2 - если X1 ТЕМНЫЙ, а X2 - ZE, то D равен B
    3 - если X1 ТЕМНЫЙ, а X2 - NS, то D равен VB
    4 - если X1 - СРЕДНИЙ, а X2 - PS, то D равен S
    5 - если X1 - СРЕДНИЙ, а X2 - ZE, то D равен B
    6 - если X1 - СРЕДНИЙ, а X2 - NS, то D равен B
    7 - если X1 - СВЕТ, а X2 - PS, то D равен VS
    8 - если X1 - СВЕТ, а X2 - ZE, то D равен S
    9 - если X1 - СВЕТ, а X2 - NS, то D равен B
    '''
#converting a fuzzy set to a crisp set , minimum membership value of each pair of linguistic values from fc_x1, fc_x2
def find_alphacut_from_inputs(fc_x1: dict, fc_x2: dict):
    '''
    Оценка всех правил из нечетких наборов входных переменных для принятия решений.
    :параметр fc_x1: Нечеткий набор для интенсивности окружающего освещения.
    :параметр fc_x2: Нечеткий набор для скорости изменения интенсивности окружающего освещения.
    :return: Альфа-срезы для каждого правила и информация о протоколировании для построения графика.
    '''
    log_rules = {}
    rules_alphacut = {}
    rules_alphacut['1'] = np.fmin(fc_x1['DARK'], fc_x2['PS'])
    rules_alphacut['2'] = np.fmin(fc_x1['DARK'], fc_x2['ZE'])
    rules_alphacut['3'] = np.fmin(fc_x1['DARK'], fc_x2['NS'])
    rules_alphacut['4'] = np.fmin(fc_x1['MEDIUM'], fc_x2['PS'])
    rules_alphacut['5'] = np.fmin(fc_x1['MEDIUM'], fc_x2['ZE'])
    rules_alphacut['6'] = np.fmin(fc_x1['MEDIUM'], fc_x2['NS'])
    rules_alphacut['7'] = np.fmin(fc_x1['LIGHT'], fc_x2['PS'])
    rules_alphacut['8'] = np.fmin(fc_x1['LIGHT'], fc_x2['ZE'])
    rules_alphacut['9'] = np.fmin(fc_x1['LIGHT'], fc_x2['NS'])
    print(rules_alphacut)
    # Logging for graph plotting
    log_rules['1'] = [fc_x1['DARK'], fc_x2['PS']]
    log_rules['2'] = [fc_x1['DARK'], fc_x2['ZE']]
    log_rules['3'] = [fc_x1['DARK'], fc_x2['NS']]
    log_rules['4'] = [fc_x1['MEDIUM'], fc_x2['PS']]
    log_rules['5'] = [fc_x1['MEDIUM'], fc_x2['ZE']]
    log_rules['6'] = [fc_x1['MEDIUM'], fc_x2['NS']]
    log_rules['7'] = [fc_x1['LIGHT'], fc_x2['PS']]
    log_rules['8'] = [fc_x1['LIGHT'], fc_x2['ZE']]
    log_rules['9'] = [fc_x1['LIGHT'], fc_x2['NS']]
    return rules_alphacut, log_rules

def alphacut_for_output(rules):
    '''
    Нахождение альфа-среза из графика объединения в том же нечетком множестве выходных переменных.
    :param rules: Альфа-срезы из входных правил для нечетких множеств выходных переменных.
    :return: Альфа-срезы для каждого нечеткого множества выходных переменных.
    '''
    very_small_alpha = float('-inf')
    small_alpha = float('-inf')
    big_alpha = float('-inf')
    very_big_alpha = float('-inf')
    # union ( max(буквенный вырез из всех правил, по которым вывод D очень МАЛ ) )
    for VS in VERY_SMALL_OUT:
        very_small_alpha = np.fmax(rules[str(VS)], very_small_alpha)
    # union ( max(буквенный вырез из всех правил, по которым вывод D МАЛ ) )
    for S in SMALL_OUT:
        small_alpha = np.fmax(rules[str(S)], small_alpha)
    # union ( max(буквенный вырез из всех правил, по которым вывод D является большим ) )
    for B in BIG_OUT:
        big_alpha = np.fmax(rules[str(B)], big_alpha)
    
    # union ( max(буквенное исключение из всех правил, которые выводят значение D ОЧЕНЬ БОЛЬШИМ ) )
    for VB in VERY_BIG_OUT:
        very_big_alpha = np.fmax(rules[str(VB)], very_big_alpha)
    
    return very_small_alpha, small_alpha, big_alpha, very_big_alpha
        
def union_graph_alphacut(very_small_alpha, small_alpha, big_alpha, very_big_alpha):
    '''
    Объединение графика выхода из всех правил.
    :param very_small_alpha: Альфа-срез для нечеткого множества очень маленького выхода.
    :param small_alpha: Альфа-срез для нечеткого множества маленького выхода.
    :param big_alpha: Альфа-срез для нечеткого множества большого выхода.
    :param very_big_alpha: Альфа-срез для нечеткого множества очень большого выхода.
    :return: Объединенный график выхода.
    '''
    output_graph = {}
    output_vs_g, output_s_g, output_b_g, output_vb_g = gen_output_membership()
    # active alphacut on graph
    act_vs_g = {}
    act_s_g = {}
    act_b_g = {}
    act_vb_g = {}
    for x, mem_val in output_vs_g.items():
        if mem_val <= very_small_alpha:
            act_vs_g[x] = mem_val
        else:
            act_vs_g[x] = very_small_alpha
    for x, mem_val in output_s_g.items():
        if mem_val <= small_alpha:
            act_s_g[x] = mem_val
        else:
            act_s_g[x] = small_alpha
    
    for x, mem_val in output_b_g.items():
        if mem_val <= big_alpha:
            act_b_g[x] = mem_val
        else:
            act_b_g[x] = big_alpha

    for x, mem_val in output_vb_g.items():
        if mem_val <= very_big_alpha:
            act_vb_g[x] = mem_val
        else:
            act_vb_g[x] = very_big_alpha
    
    # union output graph
    for i in range(0, 10, 1):
        output_graph[i] = np.fmax(act_vs_g.get(i), np.fmax(act_s_g.get(i), np.fmax(act_b_g.get(i), act_vb_g.get(i))))
    return output_graph
        
def inference(fc_x1: dict, fc_x2: dict) -> float:
    '''
    Нечеткий вывод.
    :param fc_x1: Нечеткое множество для интенсивности окружающего света.
    :param fc_x2: Нечеткое множество для скорости изменения интенсивности окружающего света.
    :return: Значение выхода, объединенный граф выхода и информация для ведения журнала для построения графиков.
    '''
    alpha_from_inputs, log_rules = find_alphacut_from_inputs(fc_x1, fc_x2)
    output_vs_alphacut, output_s_alphacut, output_b_alphacut, output_vb_alphacut = alphacut_for_output(alpha_from_inputs)
    output_graph = union_graph_alphacut(output_vs_alphacut, output_s_alphacut, output_b_alphacut, output_vb_alphacut)
    output_val = Defuzzifier.centroid(output_graph)
    return output_val, output_graph, log_rules
