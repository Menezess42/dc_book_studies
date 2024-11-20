import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import random
from chapter6_probabilidade.probabilidad import inverse_normal_cdf
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


#
#
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


if __name__ == "__main__":
    plot()

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
