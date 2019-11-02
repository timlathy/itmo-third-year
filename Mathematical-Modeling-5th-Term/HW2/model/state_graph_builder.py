import numpy as np
import sympy as sp

class StateGraphBuilder:
    nodes = set()
    adjacency = {}
    adjacency_eqs = []
    equations = None

    def __init__(self, num_priorities):
        self.symbols = {
            'l': [sp.Symbol('λ' + str(i)) for i in range(num_priorities)],
            'mu': [sp.Symbol('μ' + str(i)) for i in range(num_priorities)]
        }

    def edge(self, a, b, **kwargs):
        if a not in self.adjacency:
            self.adjacency[a] = {}
        self.adjacency[a][b] = kwargs['headlabel'] if 'headlabel' in kwargs else kwargs['label']
        self.nodes.add(a)
        self.nodes.add(b)

    def build_equations(self, edge_equations):
        self.nodes = list(self.nodes)
        self.nodes.sort()

        self.symbols['p'] = {sp.Symbol(f'p{i}'): node for i, node in enumerate(self.nodes)}
        self.p_list = list(self.symbols['p'].keys())

        def cell(i_row, n_row, i_col, n_col):
            if n_row in self.adjacency and n_col in self.adjacency[n_row]:
                v = self.adjacency[n_row][n_col]
                return edge_equations[v](self.p_list[i_row])
            return 0

        def row(i_row, n_row):
            cells = [cell(i_row, n_row, i_col, n_col) for i_col, n_col in enumerate(self.nodes)]
            cells[i_row] = -1 * sum(cells)
            return cells

        self.adjacency_eqs = [row(i_row, n_row) for i_row, n_row in enumerate(self.nodes)]
        cols = np.transpose(self.adjacency_eqs)

        self.equations = [sp.Eq(sum(col), 0) for col in cols] + [sp.Eq(sum(self.p_list), 1)]

    def solve(self, lambdas, mus):
        assert self.equations is not None, \
            "call #build_equations first"
        assert len(lambdas) == len(self.symbols['l']), \
            "len(lambdas) must be equal to num_priorities passed to GraphSolver(...)"
        assert len(mus) == len(self.symbols['mu']), \
            "len(mus) must be equal to num_priorities passed to GraphSolver(...)"

        substitutions = [*zip(self.symbols['l'], lambdas), *zip(self.symbols['mu'], mus)]
        substituted = [e.subs(substitutions) for e in self.equations]

        solution = sp.solve(substituted, list(self.symbols['p'].keys()))
        return {self.symbols['p'][p]: (self.p_list.index(p), v) for p, v in solution.items()}

    def adjacency_table(self):
        return [[str(c) for c in row] for row in self.adjacency_eqs]

    def probability_table(self, states):
        return [
            [str(i + 1), node, str(round(states[node][1], 4))]
            for i, node in enumerate(self.symbols['p'].values())
        ]
