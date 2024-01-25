import matplotlib.pyplot as plt
from fuzzy.membership import *
from utils.plot_util import get_label, get_color, get_z, rules_str, fill_DM

def x1_fuzzy():
    dark = []
    medium = []
    light = []
    for x in x_ambientLight:
        dark.append(fuzzify_x1_dark(x))
        medium.append(fuzzify_x1_medium(x))
        light.append(fuzzify_x1_light(x))
    return dark, medium, light

def x2_fuzzy():
    NS_fr = []
    PS_fr = []
    Ze_fr = []
    for x in x_ratechange:
        PS_fr.append(fuzzify_x2_PS(x))
        NS_fr.append(fuzzify_x2_NS(x))
        Ze_fr.append(fuzzify_x2_ZE(x))
    return PS_fr, Ze_fr, NS_fr

def DM_fuzzy():
    VS_DM = []
    S_DM = []
    B_DM = []
    VB_DM = []
    for x in x_controlvalue:
        VS_DM.append(fuzzify_output_very_small(x))
        S_DM.append(fuzzify_output_small(x))
        B_DM.append(fuzzify_output_big(x))
        VB_DM.append(fuzzify_output_verry_big(x))
    return VS_DM, S_DM, B_DM, VB_DM


#  Построение функций принадлежности  
def plot_membershipfn():
    # data preparing
    dark_fr, medium_fr, light_fr = x1_fuzzy()
    PS_fr, ZE_fr, NS_fr = x2_fuzzy()
    VS_DM, S_DM, B_DM, VB_DM = DM_fuzzy()
    # setup
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
    # ax0 is aqi plot
    ax0.plot(x_ambientLight, dark_fr, linewidth=2.5, label='Темный')
    ax0.plot(x_ambientLight, medium_fr, linewidth=2.5, label='Средний')
    ax0.plot(x_ambientLight, light_fr, linewidth=2.5, label='Свет')
    ax0.set_title('X1')
    ax0.legend()
    # ax1 is flowrate plot
    ax1.plot(x_ratechange, PS_fr, linewidth=2.5, label='PS')
    ax1.plot(x_ratechange, ZE_fr, linewidth=2.5, label='ZE')
    ax1.plot(x_ratechange, NS_fr, linewidth=2.5, label='NS')
    ax1.set_title('X2')
    ax1.legend()
    # ax2 is fanspeed plot
    ax2.plot(x_controlvalue, VS_DM, linewidth=2.5, label='VS')
    ax2.plot(x_controlvalue, S_DM, linewidth=2.5, label='S')
    ax2.plot(x_controlvalue, B_DM, linewidth=2.5, label='B')
    ax2.plot(x_controlvalue, VB_DM, linewidth=2.5, label='VB')
    ax2.set_title('D')
    ax2.legend()
    # adjust graph position
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.5)
    # add global title
    plt.suptitle('Функции принадлежности', fontsize=16)
    plt.show()



def plot_output_graph(output_graph: dict, centroid: float, aqi:float, flow:float):
    VS_DM, S_DM, B_DM, VB_DM  = DM_fuzzy()
    centroid_label = 'Centroid = ' + str(round(centroid,4)) + '\nD = ' + str(int(centroid)) + '%'
    print("D = "+ str(int(centroid)))
    text_offset = len(centroid_label) / 3.5
    x = []
    y = []
    for _x, mem_val in output_graph.items():
        x.append(float(_x))
        y.append(float(mem_val))
    x = np.array(x)
    y = np.array(y)
    plt.plot(x_controlvalue, VS_DM, linewidth=3, label='VS_DM', zorder=10)
    plt.plot(x_controlvalue, S_DM, linewidth=3, label='S_DM', zorder=10)
    plt.plot(x_controlvalue, B_DM, linewidth=3, label='B_DM', zorder=10)
    plt.plot(x_controlvalue, VB_DM, linewidth=3, label='VB_DM', zorder=10)
    plt.fill_between(x, 0, y, where=y>0, interpolate=True, color='0.35', zorder=5)
    plt.plot([centroid, centroid], [-0.05,1.05], 'r--', lw=3, zorder=15, label='Centroid', clip_on=False)
    props = dict(boxstyle='round', facecolor='white', alpha=1)
    plt.text((centroid - text_offset),-0.1, centroid_label, bbox=props ,zorder=20)
    title = 'D Percentage\n' + 'X1: ' + str(int(aqi)) +  ' X2: ' +str(int(flow)) 
    plt.suptitle(title)
    plt.legend()
    plt.show()
        
def plot_rules(log_rules: dict, x1: float, x2: float):
    dark_fr, medium_fr, light_fr = x1_fuzzy()
    PS_fr, ZE_fr, NS_fr = x2_fuzzy()
    VS_DM, S_DM, B_DM, VB_DM = DM_fuzzy()

    # create subplots
    col = 0
    r_num = 1
    isFirst = True

    # loop
    for loop in range(2):  # Run two loops
        num_rules_to_print = 5 if loop == 0 else 4

        fig, axs = plt.subplots(nrows=num_rules_to_print, ncols=3, figsize=(12, 5 * num_rules_to_print))
        plt.subplots_adjust(hspace=0.65, left=0.125, bottom=0.055, right=0.9, top=0.971, wspace=0.2)

        for ax in axs.reshape(-1):
            if str(r_num) in log_rules and len(log_rules[str(r_num)]) > 0:
                
                if col == 0:
                    ax.plot(x_ambientLight, dark_fr, color=get_color('X1', r_num, 1), linewidth=2.5, label=get_label('X1', r_num, 1),
                            zorder=get_z('X1', r_num, 1))
                    ax.plot(x_ambientLight, medium_fr, color=get_color('X1', r_num, 2), linewidth=2.5, label=get_label('X1', r_num, 2),
                            zorder=get_z('X1', r_num, 2))
                    ax.plot(x_ambientLight, light_fr, color=get_color('X1', r_num, 3), linewidth=2.5, label=get_label('X1', r_num, 3),
                            zorder=get_z('X1', r_num, 3))
                    #print(log_rules[str(r_num)][0])
                    ax.axvline(x=x1, ymax=log_rules[str(r_num)][0], color='b', linewidth=2.5, zorder=50)
                    ax.axhline(y=log_rules[str(r_num)][0], color='b', linewidth=2.5, xmin=120, xmax=x1 / 230.0, zorder=50)
                    ax.axhline(y=log_rules[str(r_num)][0], color='b', linewidth=2.5, xmin=x1 / 230.0, linestyle='--',
                                zorder=70)
                    if isFirst:
                        ax.set_title('X1')

                    rule = 'Rule ' + str(r_num) + ': ' + rules_str[str(r_num)]
                    ax.text(100, -0.55, rule, color='red', fontsize=10)
                    ax.legend(loc='upper right')
                    col += 1

                elif col == 1:
                    ax.plot(x_ratechange, PS_fr, color=get_color('X2', r_num, 1), linewidth=2.5, label=get_label('X2', r_num, 1),
                            zorder=get_z('X2', r_num, 1))
                    ax.plot(x_ratechange, ZE_fr, color=get_color('X2', r_num, 2), linewidth=2.5, label=get_label('X2', r_num, 2),
                            zorder=get_z('X2', r_num, 2))
                    ax.plot(x_ratechange, NS_fr, color=get_color('X2', r_num, 3), linewidth=2.5, label=get_label('X2', r_num, 3),
                            zorder=get_z('X2', r_num, 3))
                    #print(log_rules[str(r_num)][1])
                    ax.axvline(x=x2, ymax=log_rules[str(r_num)][1], color='b', linewidth=2.5, zorder=50)
                    ax.axhline(y=log_rules[str(r_num)][1], color='b', xmin=-10, xmax=x2 / 10.0, linewidth=2.5, zorder=50)
                    ax.axhline(y=log_rules[str(r_num)][1], color='b', xmin=x2 / 10.0, linewidth=2.5, linestyle='--',
                               zorder=70)
                    if isFirst:
                        ax.set_title('X2')
                    ax.legend(loc='upper right')
                    col += 1

                elif col == 2:
                    ax.plot(x_controlvalue, VS_DM, color=get_color('DM', r_num, 1), linewidth=2.5, label=get_label('DM', r_num, 1),
                            zorder=get_z('DM', r_num, 1))
                    ax.plot(x_controlvalue, S_DM, color=get_color('DM', r_num, 2), linewidth=2.5, label=get_label('DM', r_num, 2),
                            zorder=get_z('DM', r_num, 2))
                    ax.plot(x_controlvalue, B_DM, color=get_color('DM', r_num, 3), linewidth=2.5, label=get_label('DM', r_num, 3),
                            zorder=get_z('DM', r_num, 3))
                    ax.plot(x_controlvalue, VB_DM, color=get_color('DM', r_num, 4), linewidth=2.5, label=get_label('DM', r_num, 4),
                            zorder=get_z('DM', r_num, 4))
                    min_r = min(log_rules[str(r_num)][0], log_rules[str(r_num)][1])
                    #ax.axhline(y=min_r, color='b', linewidth=2.5, linestyle='--', zorder=50)
                    x, y = fill_DM(r_num, min_r)
                    ax.fill_between(x, 0, y, where=y > 0, interpolate=True, color='0.35', zorder=5)
                    if isFirst:
                        ax.set_title('DM Percentage')
                    ax.legend(loc='upper right')
                    r_num += 1
                    col = 0
                    isFirst = False
            else:
                pass

        plt.show()
    
if __name__ == '__main__':
    plot_membershipfn()