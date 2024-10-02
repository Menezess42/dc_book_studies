from typing import List


class Vetores:
    """Para nós, vetores são ponstos em uma espaço
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


if __name__ == "__main__":
    vetor = Vetores()
    adding = vetor.add([1, 2, 3], [4, 5, 6])
    assert adding == [5, 7, 9]
    subtract = vetor.subtract([5, 7, 9], [4, 5, 6])
    assert subtract == [1, 2, 3]
