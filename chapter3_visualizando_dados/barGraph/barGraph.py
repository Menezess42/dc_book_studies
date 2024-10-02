import matplotlib.pyplot as plt


class BarGraph:
        """Um gráfico de barras é uma boa opção para mostrar como algumas quantidades variam em um conjunto
        de dados 'discretos' de itens.
        """
    def __init__(self):
        self.movies = [
            "Annie Hall",
            "Ben-Hur",
            "Casablanca",
            "Gandhi",
            "West Side Story",
        ]
        self.number_of_oscars = [5, 11, 3, 8, 10]

    def movies_get(self):
        return self.movies

    def number_of_oscars_get(self):
        return self.number_of_oscars

    def movies_set(self, list):
        self.movies = list

    def number_of_oscars_set(self, list):
        self.number_of_oscars = list

    def make_graph(self):
        """Função que faz o gráfico de barras"""
        # Plota as barras com coordenadas X à esquerda [0, 1, 2, 3, 4], alturas [num_oscars]
        plt.bar(range(len(self.movies)), self.number_of_oscars)
        plt.title("My Favorite Movies")  # Adiciona um título
        plt.ylabel("# Of Academy Awards")  # rotule o exio Y
        # Rotule o eixo X com os nomes dos filmes nos centros das barras
        plt.xticks(range(len(self.movies)), self.movies)
        plt.savefig("BarGraph.png")
        plt.show()


if __name__ == "__main__":
    bargraph = BarGraph()
    bargraph.make_graph()
