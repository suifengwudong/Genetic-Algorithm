import random

class Population:
	"""
	种群类：只负责个体数据的存储和访问，不包含遗传算法逻辑。
	- pop_size: 种群规模
	- gene_length: 个体基因长度
	- individuals: 个体列表，每个个体为一个基因序列（list[int]）
	"""
	def __init__(self, pop_size, gene_length, individuals=None):
		self.pop_size = pop_size
		self.gene_length = gene_length
		if individuals is not None:
			self.individuals = individuals
		else:
			self.individuals = self._init_population()

	def _init_population(self):
		"""初始化种群个体"""
		return [[random.randint(0, 1) for _ in range(self.gene_length)] for _ in range(self.pop_size)]

	def get_individuals(self):
		"""获取所有个体"""
		return self.individuals

	def set_individuals(self, individuals):
		"""设置种群个体（用于算法更新）"""
		self.individuals = individuals

	def __len__(self):
		return len(self.individuals)

	def __getitem__(self, idx):
		return self.individuals[idx]

	def __setitem__(self, idx, value):
		self.individuals[idx] = value

	def copy(self):
		"""深拷贝当前种群"""
		new_pop = Population(self.pop_size, self.gene_length)
		new_pop.individuals = [ind[:] for ind in self.individuals]
		return new_pop
