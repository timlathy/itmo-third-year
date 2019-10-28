from graph_solver import GraphSolver
from system_equations import priority_queue_eqs

g = GraphSolver(num_priorities=3)

g.edge('0000', '1000', label='λ1')
g.edge('0000', '2000', label='λ2')
g.edge('0000', '3000', label='λ3')

g.edge('1000', '1100', label='λ1')
g.edge('1000', '2100', label='λ2')
g.edge('1000', '3100', label='λ3')
g.edge('2000', '2100', label='λ1')
g.edge('2000', '2020', label='λ2')
g.edge('2000', '2003', label='λ3')
g.edge('3000', '3100', label='λ1')
g.edge('3000', '3020', label='λ2')
g.edge('3000', '3003', label='λ3')

g.edge('1100', '2100', label='λ2')
g.edge('1100', '3100', label='λ3')

g.edge('2100', '2120', label='λ2')
g.edge('2100', '2103', label='λ3')
g.edge('2020', '2120', label='λ1')
g.edge('2020', '2023', label='λ3')
g.edge('2003', '2103', label='λ1')
g.edge('2003', '2023', label='λ2')
g.edge('2120', '2123', label='λ3')
g.edge('2023', '2123', label='λ1')
g.edge('2103', '2123', label='λ2')

g.edge('3100', '3120', label='λ2')
g.edge('3100', '3103', label='λ3')
g.edge('3020', '3120', label='λ1')
g.edge('3020', '3023', label='λ3')
g.edge('3003', '3103', label='λ1')
g.edge('3003', '3023', label='λ2')
g.edge('3120', '3123', label='λ3')
g.edge('3023', '3123', label='λ1')
g.edge('3103', '3123', label='λ2')

g.edge('2020', '2220', label='λ2')
g.edge('2023', '2223', label='λ2')
g.edge('3020', '3220', label='λ2')
g.edge('3023', '3223', label='λ2')
g.edge('2003', '2303', label='λ3')
g.edge('2023', '2323', label='λ3')
g.edge('3003', '3303', label='λ3')
g.edge('3023', '3323', label='λ3')


g.edge('1000', '0000', label='μ1')
g.edge('2000', '0000', label='μ2')
g.edge('3000', '0000', label='μ3')

g.edge('1100', '1000', label='μ1')
g.edge('2100', '1000', label='μ2')
g.edge('2020', '2000', label='μ2')
g.edge('2003', '3000', label='μ2')
g.edge('3100', '1000', label='μ3')
g.edge('3020', '2000', label='μ3')
g.edge('3003', '3000', label='μ3')

g.edge('2120', '2100', label='μ2')
g.edge('2103', '3100', label='μ2')
g.edge('2023', '2003', label='0.5μ2')
g.edge('2023', '3020', label='0.5μ2')
g.edge('3120', '2100', label='μ3')
g.edge('3103', '3100', label='μ3')
g.edge('3023', '2003', label='0.5μ3')
g.edge('3023', '3020', label='0.5μ3')

g.edge('2123', '2103', label='0.5μ2')
g.edge('2123', '3120', label='0.5μ2')
g.edge('3123', '2103', label='0.5μ3')
g.edge('3123', '3120', label='0.5μ3')

g.edge('2303', '3003', label='μ2')
g.edge('3303', '3003', label='μ3')
g.edge('2220', '2020', label='μ2')
g.edge('3220', '2020', label='μ3')
g.edge('2223', '2023', label='2/3μ2')
g.edge('2223', '2220', label='1/3μ2')
g.edge('2323', '3023', label='2/3μ2')
g.edge('2323', '2303', label='1/3μ2')
g.edge('3223', '2023', label='2/3μ3')
g.edge('3223', '3220', label='1/3μ3')
g.edge('3323', '3023', label='2/3μ3')
g.edge('3323', '2303', label='1/3μ3')

edge_equations = {
  'λ1': lambda p: p * g.symbols['l'][0],
  'λ2': lambda p: p * g.symbols['l'][1],
  'λ3': lambda p: p * g.symbols['l'][2],
  'μ1': lambda p: p * g.symbols['mu'][0],
  'μ2': lambda p: p * g.symbols['mu'][1],
  '0.5μ2': lambda p: p * g.symbols['mu'][1] * 0.5,
  '1/3μ2': lambda p: p * g.symbols['mu'][1] / 3,
  '2/3μ2': lambda p: p * g.symbols['mu'][1] * 2 / 3,
  'μ3': lambda p: p * g.symbols['mu'][2],
  '0.5μ3': lambda p: p * g.symbols['mu'][2] * 0.5,
  '1/3μ3': lambda p: p * g.symbols['mu'][2] / 3,
  '2/3μ3': lambda p: p * g.symbols['mu'][2] * 2 / 3
}

lambdas = [0.5, 0.1, 1.0]
bs = [1.0, 2.0, 0.5]
priorities = [
  [0, 0, 0],
  [2, 0, 0], # class #2 has absolute priority over class #1
  [2, 0, 0]  # class #3 has absolute priority over class #1
]

eqs = g.make_equations(edge_equations)
ps = g.solve(eqs, lambdas, mus=[1 / b for b in bs])
e = priority_queue_eqs(ps, queues=[1, 1, 1], priorities=priorities)

equation_table = e.equation_table(lambdas, bs)
param_variation_table = e.param_variation_table(lambdas, bs,
  lambdas_alt=[
    [l * 0.5 for l in lambdas],
    [l * 2 for l in lambdas]
  ],
  bs_alt=[
    [b * 0.5 for b in bs],
    [b * 2 for b in bs]
  ])

#print(f'Матрица интенсивностей переходов:\n{",".join(g.nodes)}\n')
#print(g.adjacency_table_csv())
#print('\nСтационарные вероятности состояний:\n')
#print(g.probability_table_csv(ps))
print('\nХарактеристики системы:\n')
print(table_to_csv(equation_table))
print('\nВарьирование параметров:\n')
print(table_to_csv(param_variation_table))
