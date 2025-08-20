from genetic_algorithm import POP_SIZE, GENE_LENGTH, GeneticAlgorithm
from config import PATH

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import csv
import os
import sys
import matplotlib

class GeneticAlgorithmGUI(QWidget):
    def __init__(self, ga=None):
        super().__init__()
        self.setWindowTitle('遗传算法结果展示')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('遗传算法迭代结果')
        self.layout.addWidget(self.label)

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # 追加迭代控件
        hbox = QHBoxLayout()
        self.add_gen_input = QLineEdit()
        self.add_gen_input.setPlaceholderText('追加代数')
        hbox.addWidget(self.add_gen_input)
        self.add_gen_btn = QPushButton('追加迭代')
        self.add_gen_btn.clicked.connect(self.add_generations)
        hbox.addWidget(self.add_gen_btn)
        self.layout.addLayout(hbox)

        # 初始化算法对象和种群
        matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        matplotlib.rcParams['axes.unicode_minus'] = False
        self.ga = ga if ga is not None else GeneticAlgorithm(POP_SIZE, GENE_LENGTH)

        self.load_and_plot()

    def load_and_plot(self):
        generations = []
        avg_fitness = []
        best_fitness = []
        if os.path.exists(PATH):
            with open(PATH, 'r', encoding='utf-8') as f:
                # 自动判断是否有表头
                first_line = f.readline()
                if 'generation' in first_line:
                    f.seek(0)
                    reader = csv.DictReader(f)
                    for row in reader:
                        generations.append(int(row['generation']))
                        avg_fitness.append(float(row['avg_fitness']))
                        best_fitness.append(float(row['best_fitness']))
                else:
                    # 无表头，按列索引读取
                    f.seek(0)
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 3:
                            generations.append(int(row[0]))
                            avg_fitness.append(float(row[1]))
                            best_fitness.append(float(row[2]))
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('遗传算法迭代曲线')
        ax.set_xlabel('代数')
        ax.set_ylabel('适应度')
        ax.plot(generations, avg_fitness, label='平均适应度')
        ax.plot(generations, best_fitness, label='最优适应度')
        ax.legend()
        self.canvas.draw()

    def add_generations(self):
        try:
            add_num = int(self.add_gen_input.text())
        except ValueError:
            self.label.setText('请输入有效的代数！')
            return
        self.ga.evolve(generations=add_num)
        
        self.load_and_plot()
        self.label.setText(f'已追加{add_num}代，当前代数: {self.ga.generation}')
        print(f'已追加{add_num}代，当前代数: {self.ga.generation}')

    def update(self):
        self.load_and_plot()
    

def main():
    app = QApplication(sys.argv)
    window = GeneticAlgorithmGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
