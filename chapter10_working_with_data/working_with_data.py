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

##NamedTuples
# Uma forma comum de representar os dados é com os dicts:
import datetime
# stock_price = {
# 'closing_price': 102.06,
# 'date': datetime.date(2014,8,29),
# 'symbol': 'AAPL'
#}

# No entanto há varios motivos para não fazer isso.
# Essa é uma representação ligeiramente ineficaz (um dict semrpe causa alguma sobrecarga)
# Se você tiver muitos preços de ação eles ocuparão mais memória.
# O maior problema é que acessar itens pela chave do dict tem grande propensão a erros

# Como alternativa, o python tem a classe namedtuple, parecida com uma tuple, mas com slots nomeados:
from collections import namedtuple
stockPrice = namedtuple('StockPrice', ['symbol', 'date', 'closing_price'])
price = stockPrice('MSFT', datetime.date(2018,12,14), 106.03)

assert price.symbol == 'MSFT'
assert price.closing_price == 106.03

# Como as tuples regulares, as namedtuples são imutáveis, ou seja, você não pode
# modificar seus valores depois de criá-los. Vez ou outra, isso atrapalhará, mas, no geral, é uma boa propriedade.
# Observe que ainda não resolvemos o problema da anotação de tipo. Para isso, usamos a variante tipada
# NamedTuple
from typing import NamedTuple

class StockPrice(NamedTuple):
    symbol: str
    date: datetime.date
    closing_price: float

    def is_high_tech(self) -> float:
        """Como é uma classe, também podemos adicionar métodos"""
        return self.symbol in ['MSFT', 'GOOG', 'FB', 'AMZN', 'AAPL']

price = StockPrice('MSFT', datetime.date(2018,12,14), 106.03)

assert price.symbol == 'MSFT'
assert price.closing_price == 106.03
assert price.is_high_tech()
# Nota do autor:
#> Bem pouca gente usa NamedTuple dessa forma, mas todos deveriam


## Dataclasses
# São (mais ou menos) uam versão mutável da NamedTuple. "mais ou menos" porque a NamedTuple
# representa seus dados compactamente como tuplas, mas as dataclasses são apenas classes regulares
# do python que geram alguns métodos automaticamente).
# A syntax é bem parecida com a NamedTuple. No entanto, em vez de herdar de uma classe, usamos
# um decorador
from dataclasses import dataclass

@dataclass
class StockPrice2:
    symbol: str
    date: datetime.date
    closing_price: float
    def is_high_tech(self) -> float:
        """Como é uma classe, também podemos adicionar métodos"""
        return self.symbol in ['MSFT', 'GOOG', 'FB', 'AMZN', 'AAPL']

price2 = StockPrice2('MSFT', datetime.date(2018, 12, 14), 106.03)
assert price2.symbol=='MSFT'
assert price2.closing_price==106.03
assert price2.is_high_tech()

# omo vimos antes, aqui, a grande diferença é a possibilidade de modificar os valores
# de uma instância da dataclass:
# divide as ações
price2.closing_price /=2
print(price2.closing_price)
assert price2.closing_price == 53.015

# Isso também nos deixa suscetíveis aos erros que queremos evitar quando não usamos os dicts:

# como esse é uma classe regular, adicione os novos campos da forma como quiser:
price2.closing_price = 75 # oops kkkk

#> Não usaremos dataclass, mas talvez você se depare com elas na selva do mundo real.

## Limpando e Estruturando
# Anteriormente, fiezemos isso antes de usar os dados
#closing_price = float(row[2])

# Entretanto, é possível reduzir a propensão a erros se a análise for feita em uma função
# testável
from dateutil.parser import parse

def parse_row(row: List[str]) -> StockPrice:
    symbol, date, closing_price = row
    return StockPrice(symbol=symbol,
                      date=parse(date).date(),
                      closing_price=float(closing_price))

# Agora, teste a função
stock = parse_row(['MSFT', '2018-12-14', '106.03'])

assert stock.symbol == 'MSFT'
assert stock.date == datetime.date(2018,12,14)
assert stock.closing_price == 106.03

# E se houver dados inválidos ? Um valor 'float' que não representa nenhum número?
# Vocẽ prefere receber um None a causar uma falha no programa ?

from typing import Optional
import re

def try_parse_row(row: List[str]) -> Optional[StockPrice]:
    symbol, date_, closing_price_ = row
    # Os simbolos das ações devem estar em letras maiúsculas
    if not re.match(r'^[A-Z]+$', symbol):
        return None
    try:
        date = parse(date_).date()
    except ValueError:
        return None
    try:
        closing_price = float(closing_price_)
    except ValueError:
        return None

    return StockPrice(symbol, date, closing_price)

# Dve retornar None em caso de erros
assert try_parse_row(['MSFT0','2018-12-14', '106.03']) is None
assert try_parse_row(['MSFT','2018-12--14', '106.03']) is None
assert try_parse_row(['MSFT','2018-12-14', 'x']) is None

# Mas deve retornar o mesmo que antes se os dados forem válidos
assert try_parse_row(['MSFT', '2018-12-14', '106.03']) == stock

# Por exemplo, quando temos preços de ações delimitados por vírgulas
# dados inválidos:
# AAPL,6/20/2014,90.91
# MSFT,6/20/2014,41.68
# FB,6/20/3014,64.5
# AAPL,6/19/2014,91.86
# MSFT,6/19/2014,n/a
# FB,6/19/2014,64.34

# Agora, podemos ler e retronar apenas as linhas válidas:
import csv
data: List[StockPrice] = []

with open('comma_delimited_stock_prices.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        maybe_stock = try_parse_row(row)
        if maybe_stock is None:
            print(f"skipping invalid row: {row}")
        else:
            data.append(maybe_stock)

# Dados inválidos:
# De modo geral, as três opções:
# -são eliminá-las.
# - vloltar à fonte para tentar corrigir os dados inválidos/ausentes ou
# - não fazer nada e confiar na sorte.
# Uma linha errada em meio a milhoẽos, supostamente não faz diferença, e ignora-la não faz mal.
# Mas se metade das linhas estão inválidas, você deve voltar a fonte e corrigir.

# um bom próximo passo é procurar outliers usando as técnicas indicadas na seção "explorando os dados"
# ou investigações ad hoc. Por exemplo, você observou que uma das datas no arquivo de ações trazia
# o ano 3014? Isso não gerará (necessariamente) um erro, mas está totalmente errado,
# e seus resultados serão malucos se a dta naõ for ajustada.

## Manipulando os dados
# Uma das habilidades mais importantes do cientista de dados é saber como manipular dados.
# Porém, como se trata mais de uma abordagem geral do que de uma técnica específica,
# analisaremos somenta alguns exemplos:
# Imagine um monte de dados sobre preços de ações parecidos com estes:
# data = [StockPrice(symbol='MSFT',date=datetime.data(2018,12,24), closing_price=106.03),
#         #...
#         ]

# Faremos PERGUNTAS sobre esses dados. Ao longo do caminho, tentaremos IDENTIFICAR PADRÕES
# e abstrair ferramentas para facilitar a manipulação.

# Por exemplo, imagine que queremos determinar o maior preço de fechamento da AAPL.
# Vamos FAZER isso em ETAPAS CONCRETAS:
# 1. Selecione apenas as linhas AAPL;
# 2. Selecione o closing_price de cada linha;
# 3. Calcule o max desses preços;

# Podemos executar as três etapas ao mesmo tempo usando uma compreensão:
max_aapl_price = max(stock_price.closing_price for stock_price in data if stock_price.symbol == 'AAPL')
print(max_aapl_price)

# De modo geral, queremos determinar o maior preço de fechamento de cada ação no conjunto de dados. Podemos fazer o seguinte:
# 1. crie um dcit para controlar os preços mais altos (usaremos um defaultdict que retorna menos infinito para valores ausentes, pois todos os preços serão maiores que esse valor);
# 2. Itere nos dados, fazendo sua atualização

from collections import defaultdict
max_price: Dict[str, float] = defaultdict(lambda: float('-inf'))

for sp in data:
    symbol, closing_price = sp.symbol, sp.closing_price
    if closing_price > max_price[symbol]:
        max_price[symbol] = closing_price

print(max_price)


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
