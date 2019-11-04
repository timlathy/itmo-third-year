import os
os.environ['MPLBACKEND'] = 'Agg'

import matplotlib.pyplot as plt
import matplotlib.ticker as pltticker
import labellines as pltlines

class ModelVariations:
    def __init__(self, model, default_lambdas, default_bs, lambdas_vars, bs_vars):
        self.lambdas_vars = lambdas_vars
        self.bs_vars = bs_vars

        var_params = [(l, default_bs) for l in lambdas_vars] + [(default_lambdas, b) for b in bs_vars]

        self.table = []
        for var_i, (var_l, var_b) in enumerate(var_params):
            print(f'Вариация #{var_i}: l = {var_l}, b = {var_b}')
            measures_table = model.get_measures(var_l, var_b).measures_table()
            if len(self.table) == 0:
                for line in measures_table:
                    if line[0] != '': # header
                        self.table.append([*line[:3], *[''] * len(var_params)])
                    else: # equation
                        self.table.append([*line[:2], line[3], *[''] * len(var_params)])
            for i, line in enumerate(measures_table):
                self.table[i][3 + var_i] = line[3]

    def plot(self, outfile, var, param, param_label):
        if var == 'λ':
            var_i = 0
            var_to_i = len(self.lambdas_vars)
        elif var == 'b':
            var_i = len(self.lambdas_vars)
            var_to_i = var_i + len(self.bs_vars)
        else:
            raise f'Unknown variable {var}, possible values: "λ" or "b".'

        plot_lines = []
        for i, line in enumerate(self.table):
            if line[0] == param:
                plot_lines = {
                    l[1]: [float(v) for v in l[3 + var_i:3 + var_to_i]]
                    for l in self.table[i + 1:i + 5]
                }
                break

        plt.figure(figsize=(10,6))
        plt.xlabel('Номер опыта')
        plt.ylabel(param_label)
        plt.plot(range(var_i, var_to_i), plot_lines['К1'], label='К1')
        plt.plot(range(var_i, var_to_i), plot_lines['К2'], label='К2')
        plt.plot(range(var_i, var_to_i), plot_lines['К3'], label='К3')
        plt.plot(range(var_i, var_to_i), plot_lines['$$\\sum$$'], label='$\\sum$')

        plot_line_bbox = {'pad': 0.2, 'facecolor': 'white', 'edgecolor': 'none'}
        plt.gca().xaxis.set_major_locator(pltticker.MultipleLocator(1))
        pltlines.labelLines(plt.gca().get_lines(), zorder=2, bbox=plot_line_bbox)

        plt.tight_layout()
        plt.savefig(outfile)
