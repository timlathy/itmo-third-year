import numpy as np
import sympy as sp

class GraphSolver:
    nodes = set()
    adjacency = {}
    symbols = {
        'l': sp.Symbol('λ'),
        'mu': sp.Symbol('μ')
    }
    adjacency_eqs = []

    def edge(self, a, b, **kwargs):
        if a not in self.adjacency:
            self.adjacency[a] = {}
        self.adjacency[a][b] = kwargs['headlabel'] if 'headlabel' in kwargs else kwargs['label']
        self.nodes.add(a)
        self.nodes.add(b)

    def make_equations(self, edge_equations):
        self.nodes = list(self.nodes)
        self.nodes.sort()

        self.symbols['p'] = {sp.Symbol(f'p{i}'): node for i, node in enumerate(self.nodes)}
        ps = list(self.symbols['p'].keys())

        def cell(i_row, n_row, i_col, n_col):
            if n_row in self.adjacency and n_col in self.adjacency[n_row]:
                v = self.adjacency[n_row][n_col]
                return edge_equations[v](ps[i_row])
            return 0

        def row(i_row, n_row):
            cells = [cell(i_row, n_row, i_col, n_col) for i_col, n_col in enumerate(self.nodes)]
            cells[i_row] = -1 * sum(cells)
            return cells

        self.adjacency_eqs = [row(i_row, n_row) for i_row, n_row in enumerate(self.nodes)]

        cols = np.transpose(self.adjacency_eqs)
        return [sp.Eq(sum(col), 0) for col in cols] + [sp.Eq(sum(ps), 1)]

    def solve(self, equations, l, mu):
        solution = sp.solve(equations, list(self.symbols['p'].keys()))
        return {self.symbols['p'][p]: v.subs([(self.symbols['l'], l), (self.symbols['mu'], mu)]) for p, v in solution.items()}

    def adjacency_table_csv(self):
        return '\n'.join(','.join(map(str, row)) for row in self.adjacency_eqs)

