from typing import List
from num_friends import num_friends
from collections import Counter


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
