import ciw
import simplejson as json
from tqdm import tqdm
from collections import namedtuple
from random import uniform
from multiprocessing import Pool

Distribution = namedtuple('Distribution', 'kind mean')
Model = namedtuple('Model', 'num_servers queue_capacity arrival_dist service_dist')
SimResult = namedtuple('SimResult', 'utilization task_count loss_probability mean_wait_time mean_residence_time')

# === Distributions

class DExp(Distribution):
    def __new__(cls, rate):
        dist = Distribution.__new__(cls, kind='Экспоненциальное', mean=(1 / rate))
        dist.d = ciw.dists.Exponential(rate)
        return dist

class DUniform(Distribution):
    def __new__(cls, a, b):
        dist = Distribution.__new__(cls, kind='Равномерное', mean=((a + b) / 2))
        dist.d = ciw.dists.Uniform(a, b)
        return dist

class DHypoexp2(Distribution):
    def __new__(cls, rate1, rate2):
        dist = Distribution.__new__(cls, kind='Гипоэкспоненциальное', mean=(1 / rate1 + 1 / rate2))
        dist.d = ciw.dists.Exponential(rate1) + ciw.dists.Exponential(rate2)
        return dist

class DErlang2(Distribution):
    def __new__(cls, rate):
        dist = Distribution.__new__(cls, kind='Эрланга 2-й степени', mean=(2 / rate))
        dist.d = ciw.dists.Exponential(rate) + ciw.dists.Exponential(rate)
        return dist

class DHyperexp(Distribution):
    def __new__(cls, qq, tt_1, tt_2):
        dist = Distribution.__new__(cls, kind='Гиперэкспоненциальное', mean=(qq / tt_1 + (1 - qq) / tt_2))
        dist.d = ciw.dists.CombinedDistribution(
            ciw.dists.Exponential(tt_1),
            ciw.dists.Exponential(tt_2),
            lambda s1, s2: s1 if uniform(0, 1) < qq else s2
        )
        return dist

class DTrace(Distribution):
    def __new__(cls):
        with open('trace.txt', 'r') as f:
            trace = [float(v) for v in f.read().splitlines()]

        dist = Distribution.__new__(cls, kind='Трасса', mean=(sum(trace) / len(trace)))
        dist.d = ciw.dists.Sequential(trace)
        return dist

# === Simulation

def compute_result(sim):
    tasks = sim.get_all_records()

    return SimResult(
        utilization = sim.transitive_nodes[0].server_utilisation,
        task_count = len(tasks),
        loss_probability = len(sim.rejection_dict[1][0]) / len(tasks),
        mean_wait_time = sum(t.waiting_time for t in tasks) / len(tasks),
        mean_residence_time = sum(t.waiting_time + t.service_time for t in tasks) / len(tasks)
    )

def simulate(model, task_counts):
    sim = ciw.Simulation(ciw.create_network(
        arrival_distributions=[model.arrival_dist.d],
        service_distributions=[model.service_dist.d],
        number_of_servers=[model.num_servers],
        queue_capacities=[model.queue_capacity]
    ))
    results = []
    for task_count in tqdm(task_counts):
        sim.simulate_until_max_customers(task_count, method='Finish')
        results.append(compute_result(sim))
    return results

# === Runner

models = [
    # === 3.2.1
    # utilization = 0.1
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 50), service_dist=DExp(1 / 10)),
    # utilization = 0.5
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    # utilization = 0.9
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 10), service_dist=DExp(1 / 18)),

    # === 3.2.2
    # increase lambda
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 15), service_dist=DExp(1 / 30)),
    # decrease lambda
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 60), service_dist=DExp(1 / 30)),
    # default
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    # increase mu
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 15)),
    # decrease mu
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 60)),

    # exponential arrival distributions
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 9.85), service_dist=DExp(1 / 30)),
    # traced arrival distribution
    Model(num_servers=2, queue_capacity=10, arrival_dist=DTrace(), service_dist=DExp(1 / 30)),
    # approximated (hyperexponential) arrival distribution
    Model(num_servers=2, queue_capacity=10, arrival_dist=DHypoexp2(1 / 8.55, 1 / 1.3), service_dist=DExp(1 / 30)),

    # exponential service distribution
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    # uniform service distribution
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DUniform(0, 60)),
    # erlang service distribution
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DErlang2(1 / 15)),
    # hyperexponential service distribution
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DHyperexp(1 / 2, 1 / 40, 1 / 20)),

    # === 3.2.3
    # vary queue capacity to determine at which point can we treat the model as a model with infinite queue
    # utilization = 0.5
    # loss probability is 0 at 14 (but the results can vary actually...) if running 100k tasks
    Model(num_servers=2, queue_capacity=8, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    Model(num_servers=2, queue_capacity=12, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    Model(num_servers=2, queue_capacity=14, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    Model(num_servers=2, queue_capacity=16, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    Model(num_servers=2, queue_capacity=18, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),

    # utilization = 0.9
    # loss probability is 0 at 70 (results can vary greatly) if running 100k tasks
    Model(num_servers=2, queue_capacity=55, arrival_dist=DExp(1 / 10), service_dist=DExp(1 / 18)),
    Model(num_servers=2, queue_capacity=60, arrival_dist=DExp(1 / 10), service_dist=DExp(1 / 18)),
    Model(num_servers=2, queue_capacity=65, arrival_dist=DExp(1 / 10), service_dist=DExp(1 / 18)),
    Model(num_servers=2, queue_capacity=70, arrival_dist=DExp(1 / 10), service_dist=DExp(1 / 18)),
    Model(num_servers=2, queue_capacity=75, arrival_dist=DExp(1 / 10), service_dist=DExp(1 / 18)),
    Model(num_servers=2, queue_capacity=80, arrival_dist=DExp(1 / 10), service_dist=DExp(1 / 18)),

    # === 3.2.4
    # Vary server count (1, 2, 3) and utilization (0.1, 0.5, 0.9)
    # (changing lambda & mu to keep utilization and load constant)
    # utilization = 0.1
    Model(num_servers=1, queue_capacity=10, arrival_dist=DExp(1 / 200), service_dist=DExp(1 / 20)),
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 50), service_dist=DExp(1 / 10)),
    Model(num_servers=3, queue_capacity=10, arrival_dist=DExp(1 / 20), service_dist=DExp(1 / 6)),

    # utilization = 0.5
    Model(num_servers=1, queue_capacity=10, arrival_dist=DExp(1 / 40), service_dist=DExp(1 / 20)),
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 30), service_dist=DExp(1 / 30)),
    Model(num_servers=3, queue_capacity=10, arrival_dist=DExp(1 / 24), service_dist=DExp(1 / 36)),

    # utilization = 0.9
    Model(num_servers=1, queue_capacity=10, arrival_dist=DExp(1 / 60), service_dist=DExp(1 / 54)),
    Model(num_servers=2, queue_capacity=10, arrival_dist=DExp(1 / 20), service_dist=DExp(1 / 36)),
    Model(num_servers=3, queue_capacity=10, arrival_dist=DExp(1 / 10), service_dist=DExp(1 / 27))
]

def simulate_model(m_idx):
    task_counts = [300] + list(range(10_000, 100_000, 5_000)) + list(range(100_000, 1_100_000, 100_000))

    print(f'Running model #{m_idx}')
    results = simulate(models[m_idx], task_counts)
    with open(f'model{m_idx}.json', 'w') as f:
        json.dump(results, f)
    print(f'Saved {len(results)} results for model #{m_idx}')

if __name__ == '__main__':
    with open('models.json', 'w') as f:
        json.dump(models, f)

    with Pool(8) as pool:
        pool.map(simulate_model, range(len(models)))
    pool.join()

