import enum, random

# um Enum é um conjuto tipado de valores enumerados que deixa
# o código mais descritivo e legível.
class kid(enum.Enum):
    BOY = 0
    GIRL = 1

def random_kid() -> kid:
    return random.choice([kid.BOY, kid.GIRL])

both_girls=0
older_girls=0
either_girl=0

random.seed(0)

for _ in range(10000):
    younger = random_kid()

    older = random_kid()
    if older == kid.GIRL:
        older_girls+=1
    if older == kid.GIRL and younger == kid.GIRL:
        both_girls+=1
    if older == kid.GIRL or younger == kid.GIRL:
        either_girl+=1


# Função de densidade de probabilidade (PDF)
def uniform_pdf(x: float) -> float:
    return 1 if 0 <= x < 1 else 0

# Função de distribuição cumulativa (CDF)
def uniform_cdf(x: float) -> float:
    """Retorna a probabilidade de uma varivável aleatória uniforme ser <= x"""
    if x < 0:
        return 0
    elif x < 1:
        return x
    else:
        return 1


# Distribuição Normal. A distribuição normal se expressa na clássica curva em forma
# de sino e é totalmente determinada por dois parâmetros: u(mi)=>média, o(sigma)=>desvio padrão,
# A média indica onde é o ponto central do sino e o desvio-padrão indica a sua largura.
import math
SQRT_TWO_PI = math.sqrt(2*math.pi)

def normal_pdf(x: float, mu: float=0, sigma: float=1) -> float:
    return (math.exp(-(x-mu)**2 / 2 / sigma ** 2) / (SQRT_TWO_PI*sigma))

import matplotlib.pyplot as plt
# Vamos plotar algumas figuras para conferir seu visual
def normal_pdf_plot():
    xs = [x/10 for x in range(-50,50)]
    plt.plot(xs, [normal_pdf(x,sigma=1) for x in xs], '-', label='mu=0,sigma=1')
    plt.plot(xs, [normal_pdf(x,sigma=2) for x in xs], '--', label='mu=0,sigma=1')
    plt.plot(xs, [normal_pdf(x,sigma=0.5) for x in xs], ':', label='mu=0,sigma=0.5')
    plt.plot(xs, [normal_pdf(x,mu=-1) for x in xs], ':', label='mu=-1,sigma=1')
    plt.legend()
    plt.title("Various Normal pdfs")
    plt.savefig('various_normal_pdfs.png')
    plt.show()



# A CDF para distribuição normal não pode ser calculada de forma simples
# mas podemos usar a função do erro que vem embutida na lib math
def normal_cdf(x: float, mu: float=0, sigma: float=1) -> float:
    return (1+math.erf((x-mu)/math.sqrt(2)/sigma)) / 2

# Agora vamos plotar alguns normal_cdf
def normal_cdf_plot():
    xs = [x / 10.0 for x in range(-50,50)]
    plt.plot(xs, [normal_cdf(x,sigma=1) for x in xs], '-', label="mu=0,sigma=1")
    plt.plot(xs, [normal_cdf(x,sigma=2) for x in xs], '--', label="mu=0,sigma=2")
    plt.plot(xs, [normal_cdf(x,sigma=0.5) for x in xs], ':', label="mu=0,sigma=0.5")
    plt.plot(xs, [normal_cdf(x,mu=-1) for x in xs], '-', label="mu=-1,sigma=1")
    plt.legend(loc=4) # no canto direito
    plt.title("Various Normal CDFs")
    plt.savefig("./various_normal_cdfs.png")
    plt.show()


# Ocasionalmente, vamos inverter a normal_cdf para obter o valor correspondente
# à probabilidade especificada. Não existe uma forma simples de computar essa inversão,
# no entanto como a normal_cdf é contínua e está crescendo estritamente, podemos usar
# busca binária.
def inverse_normal_cdf(p: float, mu: float=0, sigma: float=1, tolerance: float=0.00001) -> float:
    """Encontre o inverso aproximado usando a busca binária"""
    # se não for padrão, computa o padrão e redimensiona
    if mu!=0 or sigma!=1:
        return mu+sigma*inverse_normal_cdf(p, tolerance=tolerance)
    low_z = -10.0 # normal_cdf(-10) é (muito próximo de) 0
    hi_z = 10.0 # normal_cdf(10) é (muito próximo de) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z)/2 # considere o ponto médio
        mid_p = normal_cdf(mid_z) # e o valor de CDF
        if mid_p < p:
            low_z = mid_z # O ponto médio é muito baixo, procure um maior
        else:
            hi_z = mid_z # o ponto médio é muito alto, procure um menor

    return mid_z

# Teorema do Limite Central
def bernoulli_trial(p: float) -> int:
    """Retorna 1 com probabilidade p e 0 com probabilidade 1-p"""
    return 1 if random.random() < p else 0

def binomial(n: int, p: float) -> int:
    """Retorna a soma de n trial bernoulli(p)"""
    return sum(bernoulli_trial(p) for _ in range(n))

# A média de uma variável bernoulli(p) é p e seu desvio-padrão,
# raiz(p(1-p)). Segundo o teorema do limite central, à medida
# que n aumenta, a variável Binominal(n.p) se torna, aproximadamente,
# uma variável aleatória normal ccom a média u=np e o desvio-padrão
# o=raiz(np(1-p)).
# Plotamos os dois para observar claramente a semelhança.
from collections import Counter
def binomial_histogram(p: float, n: int, num_points: int) -> None:
    """Seleciona pontos de um Binomial(n,p) e plota seu histograma"""
    data = [binomial(n,p) for _ in range(num_points)]

    # Use um gráfico de barras para indicar as amostras de binomiais
    histogram = Counter(data)
    plt.bar([x - 0.4 for x in histogram.keys()],
            [v / num_points for v in histogram.values()],
            0.8,
            color='0.75')

    mu = p*n
    sigma = math.sqrt(n*p*(1-p))

    # Use um gŕafico de linhas para indicar a aproximação normal
    xs = range(min(data), max(data)+1)
    ys = [normal_cdf(i+0.5,mu,sigma) - normal_cdf(i-0.5, mu, sigma) for i in xs]
    plt.plot(xs, ys)
    plt.title("Binomial Distribution vs. Normal Aproximation")
    plt.show()


if __name__ == "__main__":
    normal_cdf_plot()
    print(f"(Both | older): {both_girls / older_girls}") # 0.514 - 1/2
    print(f"(Both | either): {both_girls / either_girl}") # 0.342 - 1/3
    normal_pdf_plot()
    print(inverse_normal_cdf(0.9))
    binomial_histogram(0.75, 100, 10000)















