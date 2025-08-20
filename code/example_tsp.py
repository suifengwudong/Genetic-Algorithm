import random
from genetic_algorithm import GeneticAlgorithm
from genetic_algorithm_gui import GeneticAlgorithmGUI
from PyQt5.QtWidgets import QApplication
import sys

# TSP参数
CITY_COORDS = [
    (0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 8), (7, 9), (3, 4)
]
CITY_NUM = len(CITY_COORDS)
GENE_LENGTH = CITY_NUM
POP_SIZE = 100         # 增加种群规模
GENERATIONS = 300      # 增加进化代数
ELITE_RATIO = 0.05     # 精英比例
MUTATION_RATE = 0.02   # 降低变异率

# 初始化算子：每个个体为城市排列

def tsp_init(pop_size, gene_length):
    from population import Population
    individuals = [random.sample(range(gene_length), gene_length) for _ in range(pop_size)]
    return Population(pop_size, gene_length, individuals)

def tsp_fitness(individual):
    def distance(a, b):
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5
    total_dist = 0
    for i in range(CITY_NUM):
        city_a = CITY_COORDS[individual[i]]
        city_b = CITY_COORDS[individual[(i+1)%CITY_NUM]]
        total_dist += distance(city_a, city_b)
    return 1 / (total_dist + 1e-6)

def tsp_crossover(parent1, parent2, gene_length=None):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child1 = [None]*size
    child1[a:b] = parent1[a:b]
    for i in range(a, b):
        if parent2[i] not in child1:
            for j in range(size):
                if child1[j] is None and parent2[i] not in child1:
                    child1[j] = parent2[i]
                    break
    for i in range(size):
        if child1[i] is None:
            for city in parent2:
                if city not in child1:
                    child1[i] = city
                    break
    child2 = [None]*size
    child2[a:b] = parent2[a:b]
    for i in range(a, b):
        if parent1[i] not in child2:
            for j in range(size):
                if child2[j] is None and parent1[i] not in child2:
                    child2[j] = parent1[i]
                    break
    for i in range(size):
        if child2[i] is None:
            for city in parent1:
                if city not in child2:
                    child2[i] = city
                    break
    return child1, child2

def tsp_mutate(individual, mutation_rate=MUTATION_RATE):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

class TSPGUI(GeneticAlgorithmGUI):
    def __init__(self):
        ga = GeneticAlgorithm(
            pop_size=POP_SIZE,
            gene_length=GENE_LENGTH,
            init_func=tsp_init,
            fitness_func=tsp_fitness,
            crossover_func=tsp_crossover,
            mutate_func=tsp_mutate,
            elite_ratio=ELITE_RATIO,
            mutation_rate=MUTATION_RATE
        )
        super().__init__(ga=ga)
        self.setWindowTitle('TSP遗传算法结果展示')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TSPGUI()
    window.show()
    sys.exit(app.exec_())
