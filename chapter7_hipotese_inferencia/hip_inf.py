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
# nula é de que a moeda seja honesta -- ou seja, de que p=0.5. Testaremos # essa premissa em comparação com hipótese alternativa p!=0.5.

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


### Intervalo de confiança
def trust_inverval():
    """
    Podemos estimar a probabilidade de uma moeda viciada ao analisar
    o valor médio das variáveis de Bernouli correspondentes a cada lançamento
    -- 1 para cara, 0 para coroa. Se observarmos 525 caras em 1000 lançamentos,
    então estimamos p=0.525.
    Qual o é o nosso nível de confiança nessa estimativa ? Bem, quando sabemos o valor
    exato de p, segundo o teorema do limite central, a média das variáveis Bernouli
    deve ser aproximadamente normal, com média p eo seguinte desvio-padrão:
    math.sqrt(p*(1-p) / 1000)
    """
    # Aqui, como não sabemso o valor de p, usamos nossa estimativa
    p_hat = 525/1000
    mu=p_hat
    sigma = math.sqrt(p_hat*(1-p_hat)/1000) # 0.0158
    print(f"p_hat: {p_hat}\nmu: {mu}\nsigma: {sigma}")
    # Embora esse método não seja totalmente seguro, as pessoas costumam fazer isso.
    # Aplicando a aproximação normal concluimos que temos um "nível de confiança de 95%"
    # na afirmação de que o seguinte intervalo contém o parâmetro verdadeiro p
    a = normal_two_sided_bounds(0.95, mu, sigma) # [0.4940, 0.5560]
    print(f"{a}")

    # Logo, não determinamos que a moeda é viciada, já que 0.5 está dentro do intervalo de confiança.
    # Se tivéssemos observado 540 caras, a situação seria:
    p_hat = 540/1000
    mu = p_hat
    sigma =math.sqrt(p_hat * (1-p_hat)/1000) # 0.0158
    normal_two_sided_bounds(0.95, mu, sigma) # [0.5091, 0.5709]

    # Aqui, a "moeda honesta" não está no intervalo de confiança. (A hipótese da "meoda honesta"
    #                                                              não é verdadeira por que não
    #                                                              pasa no teste aplicado em 95% das vezes)

## P-hacking
# O procedimento que rejeita erroneamente a hipótese nula em apenas 5% das vezes - por extensão -
# rejeitrá erronemanete a hipótese nula em 5% das vezes:
from typing import List
import random
def run_experiment() -> List[bool]:
    """Lança uma moeda honesta mil vezes, True = heads, False = tails"""
    return [random.random() < 0.5 for _ in range(1000)]

def reject_fairness(experiment: List[bool]) -> bool:
    """Usando os níveis de significância de 5%"""
    num_heads = len([flip for flip in experiment if flip])
    return num_heads <469 or num_heads>531

def test_p_hacking():
    random.seed(0)
    experiments = [run_experiment() for _ in range(1000)]
    num_rejections = len([experiment
                          for experiment in experiments
                          if reject_fairness(experiment)])
    print(num_rejections)
    assert num_rejections == 46


### Test A/B
# Decidir sobre o anúncio A e o anúncio B.
# Por ser um ciêntista de dados vocÊ decide executar um experimento que consiste em exibir
# aleatoriamente um dos anúncios e contar quantos visitantes do ssitema clicam neles.
# Se 990 de mil visualizadores clicarem no anúncio A e só 10 de mil visualizadores clicarem no B,
# você pode afirmar com confiança que A é melhor do que B.
# Mas se as diferenças não forem tão acentuadas, nesse caso, aplique a inferência estatistica.

# Digamos que Na são as pessoas que visualizam o anúncio A e que na são as que clicam nele.
# Podemos pensar em cada visualização como um ensaio de Bernouli em que PA é a probabilidade
# de alguém clicar no anúnico A. Então (se Na for grande, o que é o caso aqui), sabemos que
# na/Na é, aproximadamente, uma variável aleatória normal com média PA e dsevio padrão sigma=sqrt(Pa(1-Pa)/Na)
# Da mesma forma isso ocorre para B.

# No código, expressamos isso da seguinte forma:
def estimated_parameters(N: int, n: int) -> Tuple[float, float]:
    p = n/N
    sigma = math.sqrt(p*(1-p)/N)
    return p, sigma
# Se partirmos da premissa de que as duas normais são independentes, então sua diferença também deve
# ser normal com a média PB-PA e o desvio-padrão sqrt(sigmaa² + sigmab²)

# Logo podemos testar a hipótese nula de que PA e PB são iguais aplicando a estatística:
def a_b_test_statisc(N_A: int, n_A: int, N_B: int, n_B: int) -> float:
    P_A, sigma_A = estimated_parameters(N_A, n_A)
    P_B, sigma_B = estimated_parameters(N_B, n_B)
    return (P_B - P_A) / math.sqrt(sigma_A**2 + sigma_B**2)
# Esse valor será aproximadamente uma normal padrão.

# Por exemplo se A recebe 200 cliques em mil visualizações e B recebe 180 cliques em mil visualizações,
# então a estatística é:
def z_for_A200_B180():
    z = a_b_test_statisc(1000, 200, 1000, 180)
    print(f"z:{z} para A 200 em mil e B 180 em mil")
    # A probabilidade de observar essa grande diferença se a média for igual será
    var = two_sided_p_value(z)
    print(f"Prob. d observar essa grande diferenaca se a média for igual será {var}")

# Esse valor é tão grande que não podemos definir se há alguma diferença. Por outro lado, se B
# receber somente 150 cliques, temos que:
def z_for_A200_B150():
    z = a_b_test_statisc(1000, 200, 1000, 150)
    print(f"z:{z} para A 200 em mil e B 150 em mil")
    # A probabilidade de observar essa grande diferença se a média for igual será
    var = two_sided_p_value(z)
    print(f"Prob. d observar essa grande diferenaca se a média for igual será {var}")
    # isso indica que há somente uma probabilidade de 0.003 de observar essa grande diferença
    # se os anúncios forem igualmente eficazes.

### Inferencia Bayesiana
# Os procedimentos que vimos até aqui consistem em fazer declarações de probabilidade
# sobre os testes. Exemplo "Há apenas uma probabilidade de 3% de observar uma estatística tão
# extrma se a hipótese nula for verdadeira"
# Uma abordagem alternativa à iferência é tratar os parâmetros desconhecidos como variáveis
# aleatŕoias. O analista parte de uma distribuição anterior para definir os parâmetros
# e usa os dados observados e o teorema de Bayes para atualizar a distribuição posterior desses
# parâmetros. Em vez de mitir declarações de probabilidade sobre os testes, avaliamos a probabilidade
# dos parâmetros.

# Exemplo, quando o parâmetro desconhecido é uma probabilidade (como no exemplo da moeda), costumamos
# usar uma anterior baseada na distribuição Beta, que coloca todas as probabilidades entre 0 e 1:
def B(alpha: float, beta: float) -> float:
    """Uma constante normalizadora para a qual a probabilidade total é 1"""
    return math.gamma(alpha)*math.gamma(beta) / math.gamma(alpha+beta)

def beta_pdf(x: float, alpha: float, beta: float) -> float:
    if x<=0 or x>=1: # nenhum peso foda de [0,1]
        return 0
    return x**(alpha-1)*(1-x)**(beta-1)/B(alpha, beta)
# em geral, essa distribuição centraliza seu peso em:
# alpha / (alpha + beta)
# E, quando maiores forem alpha e beta, mais "estreita" será a distribuição.
# Por exemplo, se alpha e beta são iguais a 1, a dstribução é uniforme (centrada em 0.5,
# ela será muito dispersa). Se alpha é muito maior do que beta, a maoir parte do peso fica perto de 1.
# E, se se alpha for muito menor do que beta, a maior parte do peso fica perto de 0.
# Imagine que partimos de uma distribuição anterior em p. Talvez não seja o caso de afirmar que a moeda
# é honesta; então, definimos alpha e beta como iguais a 1. Ou talvez haja uma forte convicção de que a moeda
# dá cara em 55% das vezes; nesse caso, definimos alpha como 55 e beta como 45.
# Em seguida, lançamos a moeda várias vezes e observamos h caras e t coroas. Segundo o teorema de Bayes, a
# distribuição posterior de p é, novamente, uma distribuição Beta, mas com os parâmetors alpha + h e bet + t.
# Imagine que a moeda é lançada 10 vezes, dando 3 caras. Se você partiu de uma anterior uniforme (o que
# equivale a não afirmar nada sobre a honestidade da moeda), a distribuição posterior é uma Beta(4, 8), centrada
# perto de 0.33. Como todas as probabilidades foram igualadas, seu palpite está bem perto da probabilidade observada.
# Se você partir de um Beta(20,20)(por acreditar que a moeda era razoavelmente honesta), a distribuição posterior
# é um Beta(23,27). Centrada perto de 0.46.
# À medida que lançamos a moeda mais vezes, a anterior vai perdendo a importância até que, eventualmente, temos (quase)
# a mesma distribuição posterior, seja qual tenha sido a anterior inicial.
# O mais interesante nisso tudo é a possibilidade de fazer declarações de probabilidade sobre hipóteses: "Como base
# na anterior e nos dados observados, há uma chance de apenas 5% de a probabilidade da moeda dar cara estar entre 49%
# e 51%". Filosoficamente, isso é muito diferente de uma declaração do tipo "Se a moeda for honesta, devmos observar
# dados muito extremos em apenas 5% das vezes".
# Há uma certa controvérsia em torno da aplicação da inferência Bayesiana no teste de hipóteses - em parte, porque os
# cálculos às vezes são complexos, mas também devido à escolha subjetiva da anterior.


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
    trust_inverval()
    test_p_hacking()
    z_for_A200_B180()
    z_for_A200_B150()
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
