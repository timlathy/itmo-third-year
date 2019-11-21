from model import Model, ModelVariations, BufferingStrategy
#from graphviz import Digraph

def write_csv(table, file):
  with open(file, 'w') as f:
    f.write('\n'.join(','.join(l) for l in table))

model = Model(
  queues=[1, 1, 1],
  priorities=[
    [0, 0, 0],
    [2, 0, 0], # class #2 has absolute priority over class #1
    [2, 0, 0]  # class #3 has absolute priority over class #1
  ],
  buf_strategy=BufferingStrategy.OCCUPY_LOWER_IF_FREE
)
g = model.state_graph_builder()
#g = Digraph('G')

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
g.edge('2223', '3220', label='1/3μ2')
g.edge('2323', '3023', label='2/3μ2')
g.edge('2323', '2303', label='1/3μ2')
g.edge('3223', '2023', label='2/3μ3')
g.edge('3223', '3220', label='1/3μ3')
g.edge('3323', '3023', label='2/3μ3')
g.edge('3323', '2303', label='1/3μ3')

# Corrections
g.edge('3303', '3323', label='λ2')
g.edge('2220', '2223', label='λ3')
g.edge('2303', '2323', label='λ2')
g.edge('3220', '3223', label='λ3')

#g.view() # graphviz

g.build_equations(edge_equations={
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
})

lambdas = [0.5, 0.1, 1.0]
bs = [1.0, 2.0, 0.5]

lambda_vars = [
  [0.25, 0.05, 0.5],
  lambdas,
  [1.0, 0.2, 2.0],
  [2.0, 0.4, 4.0]
]
b_vars = [
  [0.5, 1.0, 0.25],
  bs,
  [2.0, 4.0, 1.0],
  [4.0, 8.0, 2.0]
]

write_csv(g.adjacency_table(), 'интенсивности-переходов.csv')
write_csv(model.state_probability_matrix(lambdas, bs), 'стационарные-вероятности-состояний.csv')

measures = model.get_measures(lambdas, bs)
print('Состояния:')
for n in measures.nodes:
  print(n)

measures_table = measures.measures_table()
write_csv(measures_table, 'характеристики.csv')

variations = ModelVariations(model, lambdas, bs, lambda_vars, b_vars)
write_csv(variations.table, 'варьирование-параметров.csv')

print('\nСтрою графики...')

variations.plot('интенсивность-нагрузка.png', 'λ', 'Нагрузка', 'y')
variations.plot('интенсивность-загрузка.png', 'λ', 'Загрузка', '$\\rho$')
variations.plot('интенсивность-длина-очереди.png', 'λ', 'Длина очереди', 'l')
variations.plot('интенсивность-число-заявок.png', 'λ', 'Число заявок', 'm')
variations.plot('интенсивность-время-ожидания.png', 'λ', 'Среднее время ожидания', 'w')
variations.plot('интенсивность-время-пребывания.png', 'λ', 'Среднее время пребывания', 'u')
variations.plot('интенсивность-вероятность-потери.png', 'λ', 'Вероятность потери', '$\\pi$')
variations.plot('интенсивность-пропускная-способность.png', 'λ', 'Пропускная способность', '$\\lambda\'$')

variations.plot('длит-обсл-нагрузка.png', 'b', 'Нагрузка', 'y')
variations.plot('длит-обсл-загрузка.png', 'b', 'Загрузка', '$\\rho$')
variations.plot('длит-обсл-длина-очереди.png', 'b', 'Длина очереди', 'l')
variations.plot('длит-обсл-число-заявок.png', 'b', 'Число заявок', 'm')
variations.plot('длит-обсл-время-ожидания.png', 'b', 'Среднее время ожидания', 'w')
variations.plot('длит-обсл-время-пребывания.png', 'b', 'Среднее время пребывания', 'u')
variations.plot('длит-обсл-вероятность-потери.png', 'b', 'Вероятность потери', '$\\pi$')
variations.plot('длит-обсл-пропускная-способность.png', 'b', 'Пропускная способность', '$\\lambda\'$')
