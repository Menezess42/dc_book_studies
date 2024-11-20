import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import random
from chapter6_probabilidade.probabilidad import inverse_normal_cdf
from chapter4_Algebra_Linear.matrizes import Matrizes
from chapter4_Algebra_Linear.vetores import Vetores
from chapter5_estatistica.estatistica import Correlacao
from typing import List, Dict
from collections import Counter
import math

import matplotlib.pyplot as plt


## Dados unidmensionais
# O primeiro passo (e o mais óbivio) é computar algumas estatísticas sumárias,
# como o número de pontos de dados, o menor, o maior, a média e o desvio-padrão

# No entanto, isso não fornece, necessariamente, uma boa compreensão. Uma boa ideia
# é criar um histograma para agrupar os dados em buckets discretos e contar quantos
# pontos entram em cada um deles:


def bucketsize(point: float, bucket_size: float) -> float:
    """Coloque o ponto perto do próximo minimo múltiplo de bucket_size"""
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points: List[float], bucket_size: float) -> Dict[float, int]:
    """Coloca os pontos em buckets e conta o número de pontos em ccada bucket"""
    return Counter(bucketsize(point, bucket_size) for point in points)


# Por exemplo, veja os seguintes conjuntos de dados:
def plot_histogram(points: List[float], bucket_size: float, title: str = ""):
    """Plot the histogram"""
    histogram = make_histogram(points=points, bucket_size=bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.savefig(f"./{title}.png")
    plt.show()


random.seed(0)

# uniforme entre -100 e 100
uniform = [200 * random.random() - 100 for _ in range(10000)]

# distribuição normal com média 0, desvio-padrão 57
normal = [57 * inverse_normal_cdf(random.random()) for _ in range(10000)]

# Ambos têm média próximas de 0 e desvio-padrão próximos de 58,k
# porém sua distribuição são bem diferentes. A figura 10-1 mostra
# a distribuição de uniform:
plot_histogram(uniform, 10, "Uniform Histogram")

plot_histogram(normal, 10, "Normal Histogram")
# Neste caso as duas distribuições tem pontso max e min muito diferentes, mas determminar
# não é o suficiente para explicar a diferença

## Dados Bidimencionais
# Imagine que agora além dos minutos diários,
# você também tem os anos de experiência em data science. Certamente, é preciso
# entender cada dimensão individualmente, mas vocÊ tmame quer dispersar os dados
# por exemplo, veja esse outro conjunto de dados falsos
def random_normal() -> float:
    """Retorna um ponto aleatório de uma distribuição normal padrão"""
    return inverse_normal_cdf(random.random())


xs = [random_normal() for _ in range(1000)]
ys1 = [x + random_normal() / 2 for x in xs]
ys2 = [-x + random_normal() / 2 for x in xs]


# Se você executar plot_histogram em ys1 e ys2, criará gŕafico
def plot():
    plt.scatter(xs, ys1, marker=".", color="black", label="ys1")
    plt.scatter(xs, ys2, marker=".", color="gray", label="ys2")
    plt.xlabel("xs")
    plt.ylabel("ys")
    plt.legend(loc=9)
    plt.title("Very different Joint Distributions")
    plt.show()
    plt.savefig("Very_different_Joint_Distributions.png")


## Multidimentional data
Vector = Vetores.Vector
Matrix = Matrizes.Matrix
correlation = Correlacao.correlation
make_matrix = Matrizes.make_matrix

# Ao lidar com muitas dimensões, você deve determinar as relações entre elas.
# uma boa abordagem simples é analisar a matriz de correlação (correlation matrix)
# na qual a entrada na linha i e na coluna j é a correlação entre a dimensão
# i e a dimensão j dos dados:
def correlation_matrix(data: List[Vector]) -> Matrix:
    """
    retorna a matriz len(data) x len(data), na qual a entrada
    (i,j) é a correlação entre data[i] e data[j]
    """
    def correlation_ij(i: int, j: int) -> float:
        return correlation(data[i], data[j])

    return make_matrix(len(data), len(data), correlation_ij)

# Uma abordagem mais visual (quando não há muitas dimensões)
# é criar uma matriz de gráfico de dispersão (Figura 10-4)
# para indicar todos os pares de pontos nos gráficos de dispersão
# Aqui, usaremos o plt.subplot para criar subgráficos a partir
# do gráfico de referência. Quando indicamos o número de linhas
# e colunas, ele retorna um objeto figure(que não usaremos) e um array
# bidmensional de objetos axes (com os quais criaremos os gráficos):

num_points = 100
def random_row() -> List[float]:
    row = [0.0, 0, 0, 0]
    row[0] = random_normal()
    row[1] = -5 * row[0] + random_normal()
    row[2] = row[0] + row[1] + 5 * random_normal()
    row[3] = 6 if row[2] > -2 else 0
    return row

random.seed(0)
# each row has 4 points, but really we want the columns
corr_rows = [random_row() for _ in range(num_points)]

corr_data = [list(col) for col in zip(*corr_rows)]

# corr_data is a list of four 100-d vectors
num_vectors = len(corr_data)
fig, ax = plt.subplots(num_vectors, num_vectors)

for i in range(num_vectors):
    for j in range(num_vectors):

        # Scatter column_j on the x-axis vs column_i on the y-axis,
        if i != j: ax[i][j].scatter(corr_data[j], corr_data[i])

        # unless i == j, in which case show the series name.
        else: ax[i][j].annotate("series " + str(i), (0.5, 0.5),
                                xycoords='axes fraction',
                                ha="center", va="center")

        # Then hide axis labels except left and bottom charts
        if i < num_vectors - 1: ax[i][j].xaxis.set_visible(False)
        if j > 0: ax[i][j].yaxis.set_visible(False)

# Fix the bottom right and top left axis labels, which are wrong because
# their charts only have text in them
ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
ax[0][0].set_ylim(ax[0][1].get_ylim())
# plt.show() corr_data é uma lista com quatro vetores de 100-d
plt.savefig("multiD.png")
plt.show()

# Ao analisar os gráficos de dispersão, observe que a série 1 é muito negativamente
# correlacionada com a série 0, a śerie 2 é positivamente correlacionada com a série 1
# e a série 3 somente acieta os valores 0 e 6, sendo que 0 corresponde aos valores pequenos
# da série 2; e 6, aos valores grandes.
# Essa é uma forma rápida de sacar como as variáveis estão correlacionadas (você também
# pode passar horas mexendo no matplotlib para exibir as coisas do jeito especifico,
# mas isso não é muito rápido)



if __name__ == "__main__":
    # plot()
    print(":)")

#
#
#
#
#
#
#
#
#
#
#
