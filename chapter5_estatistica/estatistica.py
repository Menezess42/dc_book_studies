import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from data import num_friends, daily_minutes, daily_hours
from collections import Counter
from chapter4_Algebra_Linear.vetores import Vetores



class TendenciasCentrais:

    # A média se move sempre dependendo do valor de cada ponto.
    # Por exemplo, quando temos 10 pontos de dados e aumentamos o valor
    # de um deles em 1, a média aumenta em 0.1
    def mean(self, xs: List[float]) -> float:
        """Geralmente queremso ter alguma noção sobre o ponto central.
        Para isso usamos a média(mean) que é a soma dos dados dividio
        por sua contagem
        """
        return sum(xs) / len(xs)

    # As vezes também calculamos a mediana, que corresponde ao valor:
    # do meio quando o número de pontos de dados é ímpar.
    # ou à media dos dois valores do meio quando o numero de pontos de dados é par.
    # Ao contrario da média a mediana não se move mesmo que alteremos os valores,
    # podemos aumentar o maior valor ou diminuir o menor e a mediana continuara a mesma

    # Os sublinhados indicam que essas são funções "privadas",pois elas
    # devem ser chamadas pela função de mediana, mas não por outros usuários
    def _median_odd(self, xs: List[float]) -> float:
        """se len(xs) for impar, a mediana será o elemento do meio"""
        return sorted(xs)[len(xs) // 2]

    def _median_even(self, xs: List[float]) -> float:
        """se len(xs) for par, a mediana será a média dos dois
        elementos do meio"""
        sorted_xs = sorted(xs)
        hi_midpoint = len(xs) // 2  # p. ex., comprimento 4 => hi_midpoint 2
        return (sorted_xs[hi_midpoint - 1] + sorted_xs[hi_midpoint]) / 2

    def median(self, v: List[float]) -> float:
        """Encontra o valor do meio em v"""
        return self._median_even(v) if len(v) % 2 == 0 else self._median_odd(v)

    # Uma generalização da mediana é o quantil, um valor que separa uma
    # determianda porcentagem dos dados( a mediana separa 50% dos dados)
    def quantile(self, xs: List[float], p: float) -> float:
        """Retorna o valor pth-percentil em x"""
        p_index = int(p * len(xs))
        return sorted(xs)[p_index]

    # É pouco comum mas talvez você queira calcular a moda
    # (os valores mais frequentes)
    def moda(self, x: List[float]) -> List[float]:
        """Retorna uma lista, pois pode haver mais de uma moda"""
        counts = Counter(x)
        max_count = max(counts.values())
        return [x_i for x_i, count in counts.items() if count == max_count]

class Dispersao:
    """
    A dispersão expressa a medidad da distribuição dos dados. Aqui, em geral,
    os valores próximos de 0 indicam que os dados não estão espalhados e os
    valores maiores (ou algo assim) indicam dados muito espalhados.
    """
    # como o termpo "range" já tem um significado no python, usaremos outro nome
    def data_range(self, xs: List[float]) -> float:
        return max(xs)-min(xs)

    # A amplitude é igual a zero se os valores max e min são iguais == dados não dispersos.
    # Por outro lado se a amplitude é maior, significa que os dados estão bem dispersos.
    # Como a mediana a AMPLITUDE não depende do conjunto de dados como um todo, e sim só
    # mente dos dados Max e Min, o que significa que se um conjunto vai de 0 a 100 mas todos
    # os valores no meio são 5 ou se o conjunto vai de 0 a 100 mas os valores no meio são todos
    # 50, ambos os conjuntos terão a mesma amplitude.

    # Uma medidad de dispersão maix complexa é a VARIANCIA
    def de_mean(self, xs: List[float]) -> List[float]:
        """Traduza xs subtraindo sua média (self,para que o resultado tenha meia 0)"""
        tc = TendenciasCentrais()
        x_bar = tc.mean(xs)
        return [x - x_bar for x in xs]

    def variance(self, xs: List[float]) -> float:
        """Quase o desvio quadrado médio da média"""
        n = len(xs)
        assert n >= 2, "variance requires at least two elements"
        deviations = self.de_mean(xs)
        vetores = Vetores()
        return vetores.sum_of_squares(deviations)/(n-1)

    # Desvio padrão
    def standard_deviation(self, xs: List[float]) -> float:
        import math
        """O desvio-padrão é a raiz quadrada da variância, ou seja,
        ela é a variancia mas retirando o quadrado da medida. Tipo se
        os dados estão em metros(m) o resultado da variancia seria m²
        e o resultado do desvio-padrão é m. Mas ambos mostram a mesma coisa,
        a dispersão dos dados em relação ao ponto médio.
        """
        return math.sqrt(self.variance(xs))

    # O problema da média com os outliers também atinge a amplitude e
    # o desvio-padrão, Os outliers ditam os dados.
    # Uma alternativa mais eficiente computa a diferença entre vaolr do 75⁰ percentil
    # e o valor do 25⁰ percentil.
    def interquartile_range(self, xs: List[float]) -> float:
        """Retorna a diferença entre o percentil 75% e o percentil 25%"""
        tc = TendenciasCentrais()
        return tc.quantile(xs, 0.75) - tc.quantile(xs, 0.25)


class Correlacao:
    """Segundo o vice-presidente de Crescimento da DS ele acredita que existe
    uma corelação enter o tempo que os usuários ficam online com a quantidade de
    amigos, vamos analisar isso"""

    # Primeiro, analisaremos a covariância, um tipo de variância aplicada
    # a pares. Se a variancia mede o desvio de uma variável de média, a
    # covariância mede a varaiação simultânea de duas variáveis em relação
    # às suas médias.
    def covariance(self, xs: List[float], ys: List[float]) -> float:
        assert len(xs) == len(ys), "xs and ys must have the same size"
        dispersao = Dispersao()
        v = Vetores()
        return v.dot(v=dispersao.de_mean(xs), w=dispersao.de_mean(ys))/(len(xs)-1)
    # > Lembrete: O dot soma os produtos dos pares de elementos correspondentes.
    # > Quando os elementos correspondentes de X e Y estão acima ou abaixo das
    # > suas médias, um número positivo entra na soma. Quando um valor está acima
    # > de sua média e o outro está abaixo, um número negativo entra na soma. Logo,
    # > uma covariância positiva 'alta' indica que x tende a ser alto quando y é alto,
    # > e baixo quando y baixo.
    # > Uma covariância negativa 'alta' indica o oposto -- que x tende a ser baixo quando
    # > y é alto e vice-versa. Uma covariância próxima de zero indica que essa relação
    # > não existe.
    # Mesmo assim, pode ser difícil interpretar essse número por dois motivos:
    # 1⁰ -> Suas unidades são o produto das unidades das entradas (exemplo,
    # amigos*daily_minutes -> amigos-minuts-por-dia), o que talvez seja difícil
    # de entender.
    # 2⁰ -> Se cada usuário tivesse o dobro de amigos (mas o mesmo número de minutos),
    # a covariância seria duas vezes maior. porém, na prática, as variáveis estariam
    # tão inter-relacionadas quanto antes. Em outras palavras, é difícil definir uma
    # covariância 'alta'.

    # Por isso, é mais comum calcular a correlação, que divide os desvios-padrão das duas
    # variáveis.
    def correlation(self, xs: List[float], ys: List[float]) -> float:
        """Mede a variação simultânea de xs e ys a partir da suas médias"""
        disp = Dispersao()
        stdev_x = disp.standard_deviation(xs)
        stdev_y = disp.standard_deviation(ys)
        if stdev_x > 0 and stdev_y > 0:
            return self.covariance(xs, ys)/stdev_x / stdev_y
        else:
            return 0

    # A correlation nã tem unidade e sempre fica entre -1 (anticorrelação perfeita)
    # e 1 (correlação perfeita).



        

if __name__ == "__main__":
    tend_central = TendenciasCentrais()
    median_odd = tend_central.median([1, 10, 2, 9, 5])
    assert median_odd == 5
    median_even = tend_central.median([1, 9, 2, 10])
    assert median_even == (2 + 9) / 2
    # print(tend_central.median(num_friends))
    quantil = tend_central.quantile
    assert quantil(num_friends, 0.10) == 1
    assert quantil(num_friends, 0.25) == 3
    assert quantil(num_friends, 0.75) == 9
    assert quantil(num_friends, 0.90) == 13
    moda = tend_central.moda
    assert set(moda(num_friends)) == {1, 6}
    dispersao = Dispersao()
    data_range = dispersao.data_range(num_friends)
    assert data_range == 99
    variance = dispersao.variance(num_friends)
    assert 81.54 < variance < 81.55
    standard_deviaiton = dispersao.standard_deviation(num_friends)
    assert 9.02 < standard_deviaiton < 9.04
    interquartile = dispersao.interquartile_range(num_friends)
    assert interquartile == 6
    cr = Correlacao()
    assert 22.42 < cr.covariance(num_friends, daily_minutes) < 22.43
    assert 22.42/60 < cr.covariance(num_friends, daily_hours) < 22.43/60
    assert 0.24 < cr.correlation(num_friends, daily_minutes) < 0.25
    assert 0.24 < cr.correlation(num_friends, daily_hours) < 0.25


