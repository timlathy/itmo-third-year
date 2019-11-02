import os
os.environ['MPLBACKEND'] = 'Agg'

import matplotlib.pyplot as plt
import labellines as pltlines

def variation_table(g, model, default_lambdas, default_bs, lambdas_vars, bs_vars):
    var_params = [(l, default_bs) for l in lambdas_vars] + [(default_lambdas, b) for b in bs_vars]

    table = []
    for var_i, (var_l, var_b) in enumerate(var_params):
        print(f'variation #{var_i}: l = {var_l}, b = {var_b}')
        states = g.solve(var_l, mus=[1 / b for b in var_b])
        measures_table = model.get_measures(states).measures_table(var_l, var_b)
        if len(table) == 0:
            for line in measures_table:
                if line[0] != '': # header
                    table.append([*line[:3], *[''] * len(var_params)])
                else: # equation
                    table.append([*line[:2], line[3], *[''] * len(var_params)])
        for i, line in enumerate(measures_table):
            table[i][3 + var_i] = line[3]

    return table

def variation_plot_to_file(table, outfile, param, var_i, var_to_i, var_label, param_label):
    plot_lines = []
    for i, line in enumerate(table):
        if line[0] == param:
            plot_lines = {
                l[1]: [float(v) for v in l[3 + var_i:3 + var_to_i]]
                for l in table[i + 1:i + 5]
            }
            break

    plt.figure(figsize=(10,6))
    plt.xlabel(var_label)
    plt.ylabel(param_label)
    plt.plot(range(var_i, var_to_i), plot_lines['К1'], label='К1')
    plt.plot(range(var_i, var_to_i), plot_lines['К2'], label='К2')
    plt.plot(range(var_i, var_to_i), plot_lines['К3'], label='К3')
    plt.plot(range(var_i, var_to_i), plot_lines['$$\\sum$$'], label='$\\sum$')
    pltlines.labelLines(plt.gca().get_lines(), zorder=2, bbox={'pad': 0.2, 'facecolor': 'white', 'edgecolor': 'none'})
    plt.savefig(outfile)
