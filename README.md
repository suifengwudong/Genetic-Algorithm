# 遗传算法多问题框架

本项目实现了一个可复用的遗传算法框架，支持二进制编码、排列编码（如TSP），并集成了PyQt5可视化界面。

## 主要功能
- 算子参数化：支持自定义初始化、适应度、交叉、变异算子
- 支持背包、TSP等多种优化问题
- 结果自动保存为CSV，便于分析和可视化
- GUI界面可动态追加迭代并展示进化曲线

## 目录结构
```
code/
    genetic_algorithm.py      # 算法主类（算子参数化）
    population.py            # 种群数据结构
    config.py                # 全局参数配置
    genetic_algorithm_gui.py # PyQt5可视化界面
    example.py               # TSP问题示例（可继承GUI）
    ...
```

## 快速开始
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行TSP示例并可视化：
   ```bash
   python code/example.py
   ```
3. 运行通用遗传算法：
   ```bash
   python code/example.py  # 可自定义算子
   ```

## 算子自定义示例
详见 `example.py`，只需传入不同算子即可适配任意优化问题。

## 依赖环境
- Python 3.7+
- PyQt5
- matplotlib

## 联系与扩展
如需扩展更多问题或界面功能，请参考算子参数化设计，或联系作者。
