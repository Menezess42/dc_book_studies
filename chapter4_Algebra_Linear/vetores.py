from typing import List
import math


class Vetores:
    """Para nós, vetores são pontos em uma espaço
    de dimensão finita. Embora você não pense nos
    dados como vetores essa é uma ótima maneira
    de representar dados numéricos

    """

    Vector = List[int]

    def __init__(self):
        self.height_weight_age = [70, 170, 40]
        self.grades = [95, 80, 75, 62]

    def get_height_weight_age(self):
        return self.height_weight_age

    def set_height_weight_age(self, height_weight_age):
        self.height_weight_age = height_weight_age

    # Também faremso calculos com os vetores.
    # como as listas do Python não são vetores(o que não facilita)
    # temos que criar essas ferramentas aritiméticas.

    # Soma de vetores soma seus elementos, exemplo V + w  = v[0]+w[0]
    # v[n]+w[n]. NÃO SE PODE SOMAR VETORES DE TAMANHOS DIFERENTES

    def add(self, v: Vector, w: Vector) -> Vector:
        """Soma os elementos correspondentes.
        NÃO SE PODE SOMAR VETORES DE TAMANHOS DIFERENTES"""
        assert len(v) == len(w), "vectors must be the same size"
        return [v_i + w_i for v_i, w_i in zip(v, w)]

    # da mesma forma para subtrair vetores, basta subtrair os elementos
    # correspondentes

    def subtract(self, v: Vector, w: Vector) -> Vector:
        """subtrai os elementos correspondentes
        NÃO SE PODE SUBTRAIR VETORES DE TAMANHOS DIFERENTES"""
        assert len(v) == len(w), "vectors must be the same size"
        return [v_i - w_i for v_i, w_i in zip(v, w)]

    def vector_sum(self, vectors: List[Vector]) -> Vector:
        """Às vezes, é preciso somar uma lista de vetores por componente.
        Para isso, crie um vetor cujo primeiro elemento seja a soma de todos os
        primeiros elementos, cujo o segundo elemento seja a soma de todos os
        segundo elemtnos e assim por diante."""
        # Verifica se os vetores não estão vazios
        assert vectors, "No vectors provided!"

        # Verifique se os vetores são do mesmo tamanho
        num_elements = len(vectors[0])
        assert all(len(v) == num_elements for v in vectors), "Different sizes"

        # O elemento de n⁰ i do resultado é a soma de todo vector[i]
        return [sum(vector[i] for vector in vectors) for i in range(num_elements)]

    def scalar_multply(self, c: float, v: Vector) -> Vector:
        """Também multiplicamos um vetor por um escalar: pra isso, basta
        multiplicar cada elemnto do vetor pelo número em questão"""
        return [c * v_i for v_i in v]

    # Dessa forma podemos computar a média dos componentes de uma lsita de
    # vetores (do mesmo tamanho).
    def vector_mean(self, vectors: List[Vector]) -> Vector:
        """computa a média dos elementos"""
        n = len(vectors)
        return self.scalar_multply(1 / n, self.vector_sum(vectors))

    def dot(self, v: Vector, w: Vector) -> float:
        """Uma ferramenta menos conhecida é o produto escalar
        (ou dot product). O produto escalar de dois vetores é a soma
        dos produtos por componente
        """
        assert len(v) == len(w), "vectors must be same length"

        return sum(v_i * w_i for v_i, w_i in zip(v, w))

    # Quando w tem magnitude 1, o produto escalar mede a extensão do vetor
    # v na direção w. Por exemplo, se w = [1, 0]. Então dot(v,w) é apenas
    # o primerio componente de v. Em outras palavras, esse é o comprimento
    # do vetor quando você projeta v em w.
    def sum_of_squares(self, v: Vector) -> float:
        """Dessa forma, é fácil computar a soma dos quadrados de um vetor.
        returna v_1*v_1+...+v_n*v_n
        """
        return self.dot(v, v)

    def magnitude(self, v: Vector) -> float:
        """Podemos usar esse valor para computar a magnitude(ou comprimento)
        do vetor.
        Retorna a magnitude de v
        """
        return math.sqrt(self.sum_of_squares(v))

    # Agora temos tudo que precisamos para computar a distância entre dois
    # vetores, definida da seguinte forma:
    # raiz((v1-w1)² + ... + (vn - wn)²)

    def squared_distance(self, v: Vector, w: Vector) -> float:
        """Computa (v_1 - w_1)² + .... + (vn - wn)²"""
        return self.sum_of_squares(self.subtract(v, w))

    def distance(self, v: Vector, w: Vector) -> float:
        """Computa a distância entre v e w"""
        return math.sqrt(self.squared_distance(v, w))

    def distance_(self, v: Vector, w: Vector) -> float:
        """(outra forma de) computar a distância entre v e w"""
        return self.magnitude(self.subtract(v, w))

    # isso é tudo que precisamos para começar.
    # Usar lista cmoo vetores é bom como apresentação, mas terrível
    # para o desempenho.
    # No código de produção, use a biblioteca NumPy, que contém uma
    # classe array de alto desempenho com diversas operações aritméticas


if __name__ == "__main__":
    vetor = Vetores()
    adding = vetor.add([1, 2, 3], [4, 5, 6])
    assert adding == [5, 7, 9]
    subtract = vetor.subtract([5, 7, 9], [4, 5, 6])
    assert subtract == [1, 2, 3]
    vector_sum = vetor.vector_sum([[1, 2], [3, 4], [5, 6], [7, 8]])
    assert vector_sum == [16, 20]
    scalar_multiply = vetor.scalar_multply(2, [1, 2, 3])
    assert scalar_multiply == [2, 4, 6]
    vector_mean = vetor.vector_mean([[1, 2], [3, 4], [5, 6]])
    assert vector_mean == [3, 4]
    dot_product = vetor.dot([1, 2, 3], [4, 5, 6])
    assert dot_product == 32  # 1*4+2*5+3*6
    sum_of_sqrs = vetor.sum_of_squares([1, 2, 3])
    assert sum_of_sqrs == 14  # 1*1 + 2*2 + 3*3
    magnitude = vetor.magnitude([3, 4])
    assert magnitude == 5
