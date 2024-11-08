### Gradiente: O vetor das derivadas parciais
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chapter4_Algebra_Linear.vetores import Vetores


# Imagine uma funçção f cuja entrada é um veotr de números reais
# cuja saída gera um número real. É uma função simplse:
def sum_of_squares(v: Vetores.Vector) -> float:
    """Computa a soma de elementos quadrados em v"""
    return Vetores.dot(v,v)

# Muitas vezes teremos que maximizar ou minimizar essas funções,
# ou seja, determinar a entrada v que produz o maior (ou menor)
# valor possível.

# Em funções como essa, o gradiente aponta a direção da entrada
# na qual a função cresce mais rapidamente.

## Estimando o Gradiente
# Se f é uma função com uma variável, sua derivada em um ponto X indicada como
# f(X) muda quando alternamos X bem pouco.
# A derivada é definida como o limite do quociente das diferenças:
from typing import Callable

def difference_quotient(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x+h)-f(x))/h

# Isso ocorre a medida que H se aproxíma de 0.

# A derivada é a inclinação da reta tangente em (x,f(x)),
# e o quociente das diferenças é a inclinação da reta secante que
# passa por (x+h,f(x+h)). À mediad que h diminui, a reta secante
# se aproxíma da reta tangente.

# Em muitas funções, é fácil calcular as derivadas com exatidão.
# Por exemplo, na função square:
def square(x: float) -> float:
    return x*x
# A derivada é
def derivative(x: float) -> float:
    return 2*x

# Isso é fácil de vericar: basta computar o quociente das diferenças
# e conferir o limite.

# E se você não conseguir determinar o gradiente? Embora naõ seja
# possíivel definir o limites em python, podemos estimar derivadas
#analisando o quociente das diferenças para um pequeno valor e.
def estimar_derivadas():
    xs = range(-10,11)
    actuals = [derivative(x) for x in xs]
    estimates = [difference_quotient(square, x, h=0.001) for x in xs]

    # plote para indicar que eles são essencialmente os mesmos
    import matplotlib.pyplot as plt
    plt.title("Actual derivates vs. Estimates")
    plt.plot(xs, actuals, 'rx', label='Actual') # vermelho x
    plt.plot(xs, estimates, 'b+', label='Estimate') # azul +
    plt.legend(loc=9)
    plt.savefig("./actual_derivates_vs_estimates.png")
    plt.show()

# Se f é uma função com muitas variáveis, ela tem múltiplas derivadas parciais
# e cada uma delas indica como f muda quando fazemos pequenas alterações em uma das
# variáveis de entrada.
# Para calcular a derivada de i, devemos tratá-la como uma função da variável i e
# considerar as outras variáveis como fixas:
def partial_difference_quotient(f: Callable[[Vetores.Vector], float],
                                v: Vetores.Vector,
                                i: int,
                                h: float) -> float:
    """Retorna o quociente parcial das diferenças de i f em v"""
    w = [v_j + (h if j == i else 0)
         for j, v_j in enumerate(v)]
    return (f(w)-f(v))/h

# Depois disso estimamos o gradiente da mesma forma
def estimate_gradient(f: Callable[[Vetores.Vector], float], v: Vetores.Vector, h: float = 0.0001) -> float:
    return [partial_difference_quotient(f,v,i,h) for i in range(len(v))]

# A maior desvantagem dessa abordagem de "fazer estimativas com o quociente das diferenças"
# é seu alto custo computacional. Se v tem um comprimento n, o estimate_gradient dve
# avaliar f em 2n entradas. Nesse esquema, estimar uma série de gradientes dá muito trabalho.
# Por isso, sempre realizaremos operações matemáticas para calcular as funções de gradiente.

### Usando o Gradiente
# Usaremos os gradientes para encontrar o mínimo entre os vetores tridimencionais.
# Selecionaremos um ponto de partida aleatório e daremos pequenos passos na direção oposta
# a do gradiente até atingir um ponto em que ele seja muito pequeno
import random
from chap

if __name__=="__main__":
    estimar_derivadas()




















