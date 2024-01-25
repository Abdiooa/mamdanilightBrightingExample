from fuzzy.mamdani import LightingController_Mamdani
from plot import plot_output_graph, plot_rules,plot_membershipfn

if __name__ == "__main__":

    x1_test = [125]
    x2_test = [-6]
    fis = LightingController_Mamdani(0,0)
    for i in range(len(x1_test)):
        print('X1:', x1_test[i], ' X2:', x2_test[i])
        fis.set_input(x1_test[i], x2_test[i])
        plot_membershipfn()
        result = fis.run()
        plot_rules(result.log_rules, result.x1, result.x2)
        plot_output_graph(result.output_graph, result.crisp_value_output, x1_test[i], x2_test[i])