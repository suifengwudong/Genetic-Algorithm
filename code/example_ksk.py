import random
from genetic_algorithm import GeneticAlgorithm
from genetic_algorithm_gui import GeneticAlgorithmGUI
from PyQt5.QtWidgets import QApplication
import sys

# 背包问题参数
weights = [2, 3, 4, 5, 9]
values = [3, 4, 8, 8, 10]
max_weight = 10
GENE_LENGTH = len(weights)

# 初始化算子：二进制编码
def ksk_init(pop_size, gene_length):
    from population import Population
    individuals = [[random.randint(0, 1) for _ in range(gene_length)] for _ in range(pop_size)]
    return Population(pop_size, gene_length, individuals)

# 适应度算子：超重为0，否则为总价值
def ksk_fitness(individual):
    total_weight = sum(w for w, bit in zip(weights, individual) if bit)
    total_value = sum(v for v, bit in zip(values, individual) if bit)
    return total_value if total_weight <= max_weight else 0

# 其余均采用默认算子

class KSKGUI(GeneticAlgorithmGUI):
    def __init__(self):
        ga = GeneticAlgorithm(
            pop_size=10,
            gene_length=GENE_LENGTH,
            init_func=ksk_init,
            fitness_func=ksk_fitness,
            mutation_rate=0.05
        )
        super().__init__(ga=ga)
        self.setWindowTitle('背包问题遗传算法结果展示')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KSKGUI()
    window.show()
    sys.exit(app.exec_())
