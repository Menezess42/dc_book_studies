import matplotlib.pyplot as plt
from collections import Counter


class BgHistogramDistribuiton:
    """um gráfico de barras também pode ser uma boa opção para plotar
    histogramas de valores numéricos agrupados e representar visualmente
    a 'distribuição' dos valores"""

    def __init__(self):
        self.grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]

    def grades_get(self):
        return self.grades

    def grades_set(self, list):
        self.grades = list

    def make_histogram(self):
        """Agrupa as notas por decil, mas coloque o 100 com o 90"""
        return Counter(min(grade // 10 * 10, 90) for grade in self.grades)

    def make_graph(self):
        # Agrupa as notas por decil, mas coloque o 100 com o 90
        histogram = self.make_histogram()
        plt.bar(
            [x + 5 for x in histogram.keys()],  # Move as barras para a direita em 5
            histogram.values(),  # Atribui a altura correta a cada barra
            10,  # Atribui a largura 10 a cada barra
            edgecolor=(0, 0, 0),  # Escureça as bordas das barras
        )
        plt.axis([-5, 105, 0, 5])  # eixo x de -5 a 105, eixo y de 0 a 5

        plt.xticks([10 * i for i in range(11)])  # Rótulos do eixo x em 0, 10, ..., 100
        plt.xlabel("decile")
        plt.ylabel("# of Students")
        plt.title("Distribution of Exam 1 Grades")
        plt.savefig("BarGraph_Histogram_Distribution.png")
        plt.show()


if __name__ == "__main__":
    bg_histogram_distribution = BgHistogramDistribuiton()
    bg_histogram_distribution.make_graph()
