import matplotlib.pyplot as plt


class SimpleGraph():
    def __init__(self):
        self.years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
        self.gpd = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

    def gpd_get(self):
        return self.gpd

    def years_get(self):
        return self.years

    def gpd_set(self, list):
        self.gpd = list

    def years_set(self, list):
        self.years = list

    def make_graph(self):
        """Cria um gráfico de linhas, anos no eixo x, gpd no eixo y"""
        plt.plot(self.years, self.gpd,
                 color='green',
                 marker='o',
                 linestyle='solid')

        # Adiciona um título
        plt.title("Normal GDP")

        # Adiciona um rótulo ao eixo Y
        plt.ylabel("Billions of $")
        plt.savefig("simpleGraph.png")
        plt.show()


if __name__ == "__main__":
    simplegraph = SimpleGraph()
    simplegraph.make_graph()
