import numpy as np
from pymoo.core.individual import Individual
from pymoo.core.problem import Problem
from pymoo.core.sampling import Sampling
from pymoo.core.variable import Choice


def individual_to_arch(population, n_blocks):
    archs = []
    for individual in population:
        archs.append(
            {
                "ks": individual[0:n_blocks],
                "e": individual[n_blocks : 2 * n_blocks],
                "d": individual[2 * n_blocks : -1],
                "r": individual[-1:],
            }
        )
    return archs


class OfaIndividual(Individual):
    def __init__(self, individual, accuracy_predictor, config=None, **kwargs):
        super().__init__(config=None, **kwargs)
        self.X = np.concatenate(
            (
                individual[0]["ks"],
                individual[0]["e"],
                individual[0]["d"],
                individual[0]["r"],
            )
        )
        self.latency = individual[1]
        self.accuracy = 100 - accuracy_predictor.predict_accuracy([individual[0]])
        self.F = np.concatenate((self.latency, [self.accuracy.squeeze().numpy()]))


class OfaProblem(Problem):
    def __init__(self, efficiency_predictor, accuracy_predictor, num_blocks, num_stages, search_vars):
        self.ks = Choice(options=search_vars.get('ks'))
        self.e = Choice(options=search_vars.get('e'))
        self.d = Choice(options=search_vars.get('d'))
        self.r = Choice(options=search_vars.get('r'))
        super().__init__(
            vars=num_blocks * [self.ks] + num_blocks * [self.e] + num_stages * [self.d] + [self.r],
            n_obj=2,
            n_constr=0,
        )
        self.efficiency_predictor = efficiency_predictor
        self.accuracy_predictor = accuracy_predictor
        self.blocks = num_blocks
        self.stages = num_stages
        self.search_vars = search_vars

    def _evaluate(self, x, out, *args, **kwargs):
        # x.shape = (population_size, n_var) = (100, 4)
        arch = individual_to_arch(x, self.blocks)
        f1 = self.efficiency_predictor.predict_efficiency(arch)
        f2 = 100 - self.accuracy_predictor.predict_accuracy(arch)
        out["F"] = np.column_stack([f1, f2])


class OfaSampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        return [
            [np.random.choice(var.options) for var in problem.vars]
            for _ in range(n_samples)
        ]


class OfaRandomSampler:
    def __init__(self, arch_manager, efficiency_predictor):
        self.arch_manager = arch_manager
        self.efficiency_predictor = efficiency_predictor

    def random_sample(self):
        sample = self.arch_manager.random_sample()
        efficiency = self.efficiency_predictor.predict_efficiency([sample])
        return sample, efficiency
