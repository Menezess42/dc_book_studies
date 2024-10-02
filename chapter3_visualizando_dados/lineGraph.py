import matplotlib.pyplot as plt


class LineGraph:
    """como vimos antes, podemos criar gráficos de linh usando o plt.plot
    Essa é uma boa opção para mostrar 'tendências'"""

    def __init__(self):
        self.variance = [1,2,4,8,16,32,64,128,256]
        self.bias_squared = [256,128,64,32,16,8,4,2,1]

    def get_variance(self):
        return self.variance

    def set_variance(self, variance):
        self.variance = variance

    def get_bias_squared(self):
        return self.bias_squared

    def set_bias_squared(self, bias_squared):
        self.bias_squared = bias_squared

    def make_total_error(self):
        self.total_error = [x+y for x, y in zip(self.variance,self.bias_squared)]

    def make_xs(self):
        self.xs = [i for i, _ in enumerate(self.variance)]


    def make_graph(self):
        """Podemos fazer múltiplas chamadas para o plt.plot
        para mostrar múltiplas séries no mesmo gráfico"""
        plt.plot(self.xs, self.variance, 'g-', label='variance') # linha verde sólida
        plt.plot(self.xs, self.bias_squared, 'r-.', label='bias^2') # linha vermelha de pontos tracejados
        plt.plot(self.xs, self.total_error, 'b:', label='total error') # linha pontilhada azul

        # Como atribuimos rótulos a cada série
        # podemos criar uma legenda de graça (loc=9 means "top center")
        plt.legend(loc=9)
        plt.xlabel("model complexity")
        plt.xticks([])
        plt.title('The Bias-variance tradeoff')
        plt.savefig('lineGraph.png')
        plt.show()

if __name__ == "__main__":
    linegraph = LineGraph()
    linegraph.make_total_error()
    linegraph.make_xs()
    linegraph.make_graph()
