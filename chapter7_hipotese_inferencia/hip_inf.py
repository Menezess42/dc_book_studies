# Teste estatístico de Hipótese
# Muitas vezes DCientits fazem teste para confirmar
# se uma hipótese é verdadeira. Tipo afirmações como
# "é mais provável que as pessoas saim da página sem ler
# o conteúdo quando surge um anúncio em uma janela pop-up
# com um botão de fechar pequeno e inacaessível".

# O esquema clássico contém a hipótese nula h0, que representa
# uam posição padrão, e uma hipótese h1 para comparação.
# Aplicamos estatística para decidir se h0 é falsa ou não.

# EXEMPLO LANÇAMENTO DA MOEDA
# Queremos testar a honestidade de uma moeda. Partimos da premissa
# de que a moeda tem a probabilidade p de dar cara; então, a hipótese
# nula é de que a moeda seja honesta -- ou seja, de que p=0.5. Testaremos
# essa premissa em comparação com hipótese alternativa p!=0.5.

# Especificamente, o teste consistirá em n lançamentos da moeda e na contagem do
# número de X de caras. Cada lançamento da moeda é um ensaio de Bernouli, ou seja,
# X é variável aleatória Binomial(n,p), que podemos aproximar usando a distribuição
# normal
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Tuple
import math


def normal_approximation_to_binomial(n: int, p: float) -> Tuple[float, float]:
    """Retorna mu e sigma correspondentes Binomial(n, p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma


# Sempre que uma variável aleatória segue uma distribuição normal, é possível
# aplicar o normal_cdf para descobrir a probabilidade de o seu valor realizado estar
# contido (ou não) em um determinado intervalo
from chapter6_probabilidade.probabilidad import normal_cdf

# o normal cdf é a probabilidade de a variável estar abaixo de um limite
normal_probability_below = normal_cdf


# Está acima do limite se não está abaixo do limite
def normal_probability_above(lo: float, mu: float = 0, sigma: float = 1) -> float:
    """A probabilidade de que N(mu, sigma) seja maior do que lo."""
    return 1 - normal_cdf(lo, mu, sigma)


# Está entre se é menor que hi, mas não menor do que lo
def normal_probability_between(
    lo: float, hi: float, mu: float = 0, sigma: float = 1
) -> float:
    """A probabilidade de que um N(mu, sigma) esteja entre lo e hi"""
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)


# Está fora se não está dentro
def normal_probability_outside(
    lo: float, hi: float, mu: float = 0, sigma: float = 1
) -> float:
    """A probabilidade de que um N(mu, sigma) não esteja entre lo e hi"""
    return 1 - normal_probability_between(lo, hi, mu, sigma)


# Também podemos fazer o contrário e encontrar a região fora do limiar ou
# o intervalo (simétrico) em torno da média que está associado a um determinado
# nível de probabilidade. Por exemplo, para encontrar o intervalo centrado
# na média que contém 60% da probabilidade, é preciso determinar os limiares
# inferirores e superiores que contêm, individualmente 20% da probabilidade (deixando 60%)

from chapter6_probabilidade.probabilidad import inverse_normal_cdf


def normal_upper_bound(probability: float, mu: float = 0, sigma: float = 1) -> float:
    """Retorna o z para o qual P(z <= Z) = probabilidade"""
    return inverse_normal_cdf(probability, mu, sigma)


def normal_lower_bound(probability: float, mu: float = 0, sigma: float = 1) -> float:
    """Retorna o z pra o qual P(z>=1) = probabilidade"""
    return inverse_normal_cdf(1 - probability, mu, sigma)


def normal_two_sided_bounds(
    probability: float, mu: float = 0, sigma: float = 1
) -> Tuple[float, float]:
    """retorna os limites simétricos (relativos à média) que contêm a probabilidade especificada"""
    tail_probability = (1 - probability) / 2

    # o limite superior deve estar abaixo de tail_probability
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)

    # O limite inferior deve estar acima de tail_probability
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)

    return lower_bound, upper_bound


#### P-Values
# No teste anterior, também podemos aplicar os p-values. Em vez de escolher
# limites com base eum um limiar de probabilidade, é possível
# computar a probabilidade -- com base na premissa de que h0 é verdadeiro --
# de observar um valor pelo menos tão extremo quanto o que já observamos
# Computamos o teste bilateral da honestidade da moeda da seguinte forma:
def two_sided_p_value(x: float, mu: float = 0, sigma: float = 1) -> float:
    """
    Qual é a probabilidade de observar um valor pelo menos tão extremo
    quanto x (em qualquer direção) se os valores vêm de um N(mu, sigma)?
    """
    if x >= mu:
        # x é maior que a média, então a coroa é qualquer valor maior que x
        return 2 * normal_probability_above(x, mu, sigma)

    # x é menor que a média, então a coroa é qualquer valor menor que x
    return 2 * normal_probability_below(x, mu, sigma)


# Para que a sensibilidade dessa estimativa fique clara, vamos a uma simulação:
def p_value_simulation():
    import random

    extreme_value_count = 0
    for _ in range(1000):
        num_heads = sum(
            1 if random.random() < 0.5 else 0  # Conte o n⁰ de caras
            for _ in range(1000)
        )  # em mil lançamentos,
        # e conte as vezes em que
        # o n⁰ é 'extremo'

        if num_heads >= 530 or num_heads <= 470:
            extreme_value_count += 1

    # O p-value era 0.062 => ~62 valores extremos em 1000
    assert 59 < extreme_value_count < 65, f"{extreme_value_count}"


if __name__ == "__main__":
    # Digamos que a moeda será lançada n=mil vezes.
    # Se a hipótese de honestidade estiver correta,
    # X estará distribuido, aproximadamente, de modo
    # normal com média de 500 e desvio-padrão de 15.8
    mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
    print(f"mu_0:{mu_0}\nsigma_0:{sigma_0}")

    # Precisamos definir a significancia -- Determinar nosso nível
    # de disposição para obter um erro tipo 1 ("falso positivo")
    # e recusar a H0 mesmo se ela for verdadeira.
    # essa disposição costuma ser definida em 5% ou 1%. Aqui, escolhemos
    # 5%
    # O teste recusará H0 se X estiver fora dos limites obtidos da seguinte
    # forma:
    lower_bound, upper_bound = normal_two_sided_bounds(0.95, mu_0, sigma_0)
    print(f"Lower Bound:{lower_bound}\nUpper Bound:{upper_bound}")
    # Partindo da premissa de que p é igual a 0.5(h0 verdadeiro), há uma
    # probabilidade de apenas 5% de observarmos um X fora desse intervalo,
    # exatamente a significancia determinada. Em outras palavras, se h0 é verdadeira,
    # então o teste indica o resultado correto em, aproximadamente, 19 de 20 vezes.

    # Também queremos determinar a potência do teste, a probabilidade de não
    # ocorrer um erro tipo 2, que acontece quando falhamos na recusa de uma h0 falsa.
    # Para medir isso, temos que especificar o significado de uma h0 falsa.
    # (saber que p não é 0.5 não fornce muita informação sobre a distribuição de X).
    # Especificamente, queremos verificar o que acontece se p realmente for 0.55;
    # nesse caso, a moeda estará levemente viciada em cara.
    # Aqui podemos calcular a potência do teste da seguinte forma:

    # limites de 95% baseados na premissa de que p=0.5
    lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
    print(f"limites de 95% baseados na premissa de que p=0.5\n\tlo:{lo}\n\thi:{hi}")

    # mu e sigma reais baseados em p=0.55
    mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
    print(f"mu e sigma reais baseados em p=0.55\n\tmu_1:{mu_1}\n\tsigma_1:{sigma_1}")

    # Um erro tipo 2 ocorre quando falhamos em rejeitar a hipótese nula, o que ocorre
    # quando X ainda está no intervalo original
    type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
    print(
        f" Um erro tipo 2 ocorre quando falhamos em rejeitar a hipótese nula, o que ocorre quando X ainda está no intervalo original\n\tType_2_probability:{type_2_probability} "
    )
    power = 1 - type_2_probability  # 0.887
    print(f"Power of type_2 in %:\n\tPower:{power}")

    # Agora imagine que a hipótese nula indica que a moeda não está viciada em cara,
    # ou seja, que p<=0.5. Nesse caso, queremos um teste unilateral pra rejeitar a
    # hipótese nula quando X é muito maior que 50, mas não quando X é menor. Portanto,
    # o teste de significancia de 5% deve aplicar o normal_probability_below para
    # encontrar o limiar que fica sobre probabilidade de 95%:

    hi = normal_upper_bound(0.95, mu_0, sigma_0)
    # é 526 (<531, já que precisamos de mais probabilidade no ponto superior)
    type_2_probability = normal_probability_below(hi, mu_1, sigma_1)
    power = 1 - type_2_probability  # 0.936
    print(f"Power of type_2 in %:\n\tPower:{power}")

    # Esse teste tem uma potência maior, pois não recusa mais a h0 quando X é
    # menor do que 469 (algo muito improvável de acontecer se h1 for verdadeiro);
    # em vez disso, ele recusa a h0 quando X está entre 526 e 531 (algo provável
    # de acontecer se h1 for verdadeiro).

    # Computamos a observação de 530 caras da seguinte forma:
    tw_sided_p_value = two_sided_p_value(529.5, mu_0, sigma_0)  # 0.062
    print(tw_sided_p_value)
    p_value_simulation()
    # Como o p-value é maior que a significância de 5% não recusamos a hípotese
    # nula. Se observamos 532 caras, então o p-value é:
    print(two_sided_p_value(531.5, mu_0, sigma_0))

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
#
#
#
#
#
#
#
