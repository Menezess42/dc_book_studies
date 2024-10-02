import matplotlib.pyplot as plt


class DispersionGraph:
    """O gráfico de dispersão é a opção certa para representar
    as relações entre pares de conjuntos de dados.
    Este gráfico porexemplo, ilustra as relações entre o número de amigos
    dos usuários e o número de minutos que eles passam no site por dia
    """

    def __init__(self):
        self.friends = [70, 65, 72, 63, 71, 64, 60, 64, 67]
        self.minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
        self.labels = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

    def get_friends(self):
        return self.friends

    def set_friends(self, friends):
        self.friends = friends

    def get_minutes(self):
        return self.minutes

    def set_minutes(self, minutes):
        self.minutes = minutes

    def get_labels(self):
        return self.labels

    def set_labels(self, labels):
        self.labels = labels

    def make_graph(self):
        plt.scatter(self.friends, self.minutes)

        for label, friend_count, minute_count in zip(
            self.labels, self.friends, self.minutes
        ):
            plt.annotate(
                label,
                xy=(friend_count, minute_count),  # Coloque o rótulo no respectivo ponto
                xytext=(5, -5),  # mas levemetne deslocado
                textcoords="offset points",
            )

        plt.title("Daily Minutes vs. number of Friends")
        plt.xlabel("# of friends")
        plt.ylabel("daily minuts spent on the size")
        plt.savefig("dispersionGraph.png")
        plt.show()


if __name__ == "__main__":
    dispersiongraph = DispersionGraph()
    dispersiongraph.make_graph()
