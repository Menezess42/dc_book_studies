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
from chapter4_Algebra_Linear.vetores import Vetores

def gradient_step(v: Vetores.Vector, gradient: Vetores.Vector, step_size: float) -> Vetores.Vector:
    vetores = Vetores()
    """Move 'step_size' na direção 'gradient' a partir de 'v' """
    assert len(v) == len(gradient)
    step = vetores.scalar_multply(step_size, gradient)
    return vetores.add(v, step)

def sum_of_squares_gradient(v: Vetores.Vector) -> Vetores.Vector:
    return [2*v_i for v_i in v]

def using_gradient():
    v = [random.uniform(-10,10) for i in range(3)]
    vetores = Vetores()
    for epoch in range(1000):
        grad = sum_of_squares_gradient(v) # compute o gradiente em v
        v = gradient_step(v,grad,-0.01)   # de um passo negativo para o gradiente
        print(f"Epoch:{epoch} V:{v}")
        
    assert vetores.distance(v, [0,0,0]) < 0.001 # v deve ser próximo de 0

# Escolhendo o tamanho do passo
# As opções mais populares para escolher os step é:
# - Usar um passo de tamanho fixo;
# - Diminuir gradualmente o tamanho do passo;
# - A cada passo, escolher um tamanho que minimize o valor da função objetiva.
# Essa última abordagem parece ótima, mas tem um alto custo computacional na prática.
# O "Melhor" tamanho depende do problema.
# Step pequeno d+ == gradiente infinito
# Step grande d+ == Função cresce d+ ou fica indefinida

### Usando o gradiente descendente para ajustar modelos
# Geralmente, os dados estão em conjuntos e modelos(hipotéticos) que
# dependem (de maneira diferenciável) deu um ou mais parâmetros. Além disso,
# teremos uma função de 'perda' para medir a adequação do modelo aos dados.
# Se estabelecermos que os dados são fixos, nossa função de perda indicará
# a eficácia dos parâmetros de um determinado modelo. Assim, podemos usar o
# gradiente descendente para definir os parâmetros do modelo e reduzir ao máximo
# a perda.
# Vamos a um exemplo simples:

# x vai de -50 a 49, y é sempre 20*x+5
inputs = [(x,20*x+5) for x in range(-50,50)]
# Neste caso, conhecemos os parâmetros de relação linear entre x e y,
# mas imagine que queremos obtê-los a partir dos dados. Usaremos o gradiente
# descendente para encontrar a inclinação e o intercepto que minimizam o erro
# quadrático médio.

# Começaremos com uma função que determina o gradiente com base no erro
# de apenas um ponto de dados:
def linear_gradient(x: float, y: float, theta: Vetores.Vector) -> Vetores.Vector:
    slope, intercept = theta
    predicted = slope * x+intercept # a previsão do modelo
    erro = (predicted - y) # o erro é (previsto - real)
    squared_error = erro**2 # vamos minimizar o erro quadrático
    grad = [2*erro*x, 2*erro] # usando seu gradiente
    return grad

# VAMOS ANALISAR o significado desse gradiente. Imagine que, para x, a previsão é
# alta demais. Nesse caso, o erro é positivo. O seegundo termo do gradiente, 2*erro,
# é positivo, indicando que pequenos aumentos no intercepto aumentarão ainda mais a
# previsão (que já é muito grande), o que, por sua vez, aumentará bastatne o erro
# quadrático (para esse x).
# O primeiro termo do gradiente, 2*erro*x tem o mesmo sinal que x. Com certeza, see
# x for positivo, peequenos aumentos na inclinação aumentarão novamente a previsão
# (e, portanto, o erro). Porém, se x for negativo, pequenos aumentos na inclinação
# diminuirão a previsão (e, portanto, o erro).

# ESSA COMPUTAÇÃO FOI APENAS PARA UM PONTO DE DADOS.

# Para o conjunto de dados como um todo, temos que calcular o 'erro quadrático médio',
# cujo gradiente é apenas a média dos gradientes individuais.

# Então faremos o seguinte:
# 1. Defina um valor aleatório para theta.
# 2. Compute a média dos gradientes.
# 3. Ajuste o theta nessa direção.
# 4. Repita o processo.

# Depois de muitas épocas (cada passagem pelo conjunto de dados), determinamos algo
# parecido com os parâmetros corretos:
from chapter4_Algebra_Linear.vetores import Vetores

def showing_gradient():
    # comece com valores aleatórios para a inclinação e o intercepto
    theta = [random.uniform(-1,1), random.uniform(-1,1)]
    learning_rate = 0.001
    for epoch in range(5000):
        # compute a média dos gradientes
        vet = Vetores()
        grad = vet.vector_mean([linear_gradient(x,y,theta) for x,y in inputs])
        # Dê um passo nessa direção
        theta = gradient_step(theta, grad, -learning_rate)
        print(f"===>\n\tEpoch:{epoch}\n\ttheta:{theta}")

    slope, intercept = theta
    assert 19.9 < slope <20.1, "slope should be about 20"
    assert 4.9 < intercept < 5.1, "Intercept should be about 5"

## Minibatch e Gradiente Descendente Estocástico
# Uma desvantagem da abordagem anteriro é a necessidade de avaliar os
# gradientes no conjunto de dados inteiro antes de dar um passo e atualizar
# os parâmetros.

# Técninca do gradiente descendente por Minibatch:
# Definimos o gradiente (e damos um passo) com base em uma amostra(minibatch)
# extraída do conjunto de dados total
from typing import TypeVar, List, Iterator
T = TypeVar('T') # isso permite a inserção de funções "genéricas"

def minibatchs(dataset: List[T],
              batch_size: int,
              shuffle: bool=True) -> Iterator[List[T]]:
    """Gera minibatches de tamanho 'batch_size' a partir do conjunto
       de dados"""
    # Inicie os índices 0, batch_size, 2*batch_size, ...
    batch_starts = [start for start in range(0,len(dataset), batch_size)]
    if shuffle: random.shuffle(batch_starts) # classifique os batches aleatóriamente
    for start in batch_starts:
        end = start+batch_size
        yield dataset[start:end]

    # Como o TypeVar(T), criamos uma função `genérica`. Ele indica que o
    # conjunto de dados pode ser uma lista de qualquer tipo. Mas, em todos
    # os casos, as saídas serão batches.

# Agora resolvemos o mesmo problema só que usando minibatchs
def showing_gradient_minibatch():
    learning_rate = 0.001
        print(f"===>\n\tEpoch:{epoch}\n\ttheta:{theta}")
    theta = [random.uniform(-1,1), random.uniform(-1,1)]
    for epoch in range(1000):
        for batch in minibatchs(inputs, batch_size=20):
            vet = Vetores()
            grad = vet.vector_mean([linear_gradient(x,y,theta) for x,y in batch])
            theta = gradient_step(theta, grad, -learning_rate)
        print(f"===>\n\tEpoch:{epoch}\n\ttheta:{theta}")

    slope, intercept = theta
    assert 19.9<slope<20.1, "slope shoud be about 20"
    assert 4.9<intercept<5.1, "intercept should be about 5"

# Outra variação é o gradiente descendente estocástico, na qual damos
# passos de gradiente com base em um exemplo de treinamento de cada vez:
def showing_stocastic_gradient():
    learning_rate = 0.001
    theta = [random.uniform(-1,1), random.uniform(-1,1)]
    for epoch in range(100):
        for x,y  in inputs:
            grad = linear_gradient(x,y,theta)
            theta = gradient_step(theta, grad, -learning_rate)
        print(f"===>\n\tEpoch:{epoch}\n\ttheta:{theta}")

    slope, intercept = theta
    assert 19.9 < slope < 20.1, "slope should be about 20"
    assert 4.9<intercept<5.1, "intercept should be about 5"

# Nesse problema, o gradiente descendente estocástico encontra os parâmetros
# indeais em um número muito menor de épocas, mas não é tão simples. Quando
# damos passos de gradiente com base em minibatchs pequenos(ou em pontos de dados
# únicos), obtemos mais informações, embora o gradiente de um ponto às vezes esteja
# em uma direção muito diferente do gradiente do conjunto de dados total.

# Além disso, quando não calculamos tudo do zero com a álgebra linear, obtemos
# ganhos de desempenho com a "vetorização" das computações de batches, pois não
# precisamos computar cada ponto de gradiente.
    

        
if __name__=="__main__":
    #estimar_derivadas()
    #using_gradient()
    #showing_gradient()
    showing_gradient_minibatch()














