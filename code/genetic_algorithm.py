import random
from population import Population
import csv
from config import POP_SIZE, GENE_LENGTH, GENERATIONS
from config import PATH

# 默认算子定义

def default_init(pop_size, gene_length):
    return Population(pop_size, gene_length)

def default_fitness(individual):
    return int(''.join(str(bit) for bit in individual), 2)

def default_crossover(parent1, parent2, gene_length=None):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def default_mutate(individual, mutation_rate=0.1):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

class GeneticAlgorithm:
    """
    算子参数化遗传算法主类，支持自定义和默认算子。
    """
    def __init__(self, pop_size=POP_SIZE, gene_length=GENE_LENGTH,
                 init_func=default_init,
                 fitness_func=default_fitness,
                 crossover_func=default_crossover,
                 mutate_func=default_mutate,
                 mutation_rate=0.1):
        self.mutation_rate = mutation_rate
        self.population = init_func(pop_size, gene_length)
        self.fitness_func = fitness_func
        self.crossover_func = crossover_func
        self.mutate_func = mutate_func
        self.generation = 0
        self.init_csv(PATH)

    def selection(self, elite_ratio=0.05):
        fits = [self.fitness_func(ind) for ind in self.population.get_individuals()]
        total_fit = sum(fits)
        probs = [f / total_fit for f in fits]
        selected_inds = []
        for _ in range(self.population.pop_size):
            r = random.random()
            acc = 0
            for i, p in enumerate(probs):
                acc += p
                if r <= acc:
                    selected_inds.append(self.population[i][:])
                    break
        elite_num = max(1, int(self.population.pop_size * elite_ratio))
        sorted_inds = sorted(self.population.get_individuals(), key=self.fitness_func, reverse=True)
        elites = [ind[:] for ind in sorted_inds[:elite_num]]
        self.population.set_individuals(elites + selected_inds[:self.population.pop_size-elite_num])

    def crossover_population(self):
        individuals = self.population.get_individuals()
        new_inds = []
        i = 0
        while i < self.population.pop_size:
            p1 = individuals[i % self.population.pop_size]
            p2 = individuals[(i+1) % self.population.pop_size]
            c1, c2 = self.crossover_func(p1, p2, self.population.gene_length)
            new_inds.append(c1)
            if len(new_inds) < self.population.pop_size:
                new_inds.append(c2)
            i += 2
        self.population.set_individuals(new_inds)

    def mutate_population(self):
        individuals = self.population.get_individuals()
        mutated = [self.mutate_func(ind[:], self.mutation_rate) for ind in individuals]
        self.population.set_individuals(mutated)

    def evolve_1time(self, elite_ratio=0.05):
        self.selection(elite_ratio)
        self.crossover_population()
        self.mutate_population()
        self.generation += 1

    def evolve(self, generations=1, elite_ratio=0.05):
        if generations <= 0:
            raise ValueError("进化代数必须大于0")
        if generations >= GENERATIONS:
            generations = GENERATIONS
        for _ in range(generations):
            self.record_generation(PATH)
            self.evolve_1time(elite_ratio)

    def init_csv(self, path=PATH):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['generation', 'avg_fitness', 'best_fitness', 'best_individual'])

    def record_generation(self, path=PATH):
        individuals = self.population.get_individuals()
        fitness_values = [self.fitness_func(ind) for ind in individuals]
        avg_fitness = sum(fitness_values) / len(fitness_values)
        best_fitness = max(fitness_values)
        best_individual = individuals[fitness_values.index(best_fitness)]
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.generation,
                avg_fitness,
                best_fitness,
                best_individual
            ])
    def get_population(self):
        return self.population
