# Uma matriz é uma coleção bidimensioanl de números
# Representaremos as matrizes como lista de listas
# as listas internas terão o mesmo tamanho e
# representarão as linhas da matriz
# Se A é uma matriz então A[i][j] é o elemnto que
# está na linha i e na coluna j.
# Por convenção matemática, usaremos letras maiúsculas
# para representar matrizes.
from typing import List, Tuple, Callable
from vetores import Vetores
import math


class Matrizes:
    Matrix = List[List[float]]

    def __init__(self):
        self.a = [[1, 2, 3], [4, 5, 6]]
        self.b = [[1, 2], [3, 4], [5, 6]]

    # Como representa uma lista de listas, a matriz A contém
    # as linhas len(A) e colunas len(a[0]) que consideramos
    # seu shape(formato)
    def shape(self, A: Matrix) -> Tuple[int, int]:
        """Retorna (n⁰ de linhas de A, n⁰ de colunas de A)"""
        num_rows = len(A)
        num_cols = len(A[0]) if A else 0  # número de elementos na primeria linha
        return num_rows, num_cols

    def get_row(self, A: Matrix, i: int) -> Vetores.Vector:
        """Retorna a linha i de A (como um Vector)"""
        return A[i]  # A[i] já está na linha i

    def get_column(self, A: Matrix, j: int) -> Vetores.Vector:
        """Retorna a coluna j de A (como um Vector)"""
        return [A_i[j] for A_i in A]  # Elemento j da linha A_i  # para cada linha A_i

    # Também criaremos matrizes, produzindo seus elementos a partir da
    # sua forma e de uma função. Para isso, usamos uma compreensão de lista
    # aninhada.

    def make_matrix(
        self, num_rows: int, num_cols: int, entry_fn: Callable[[int, int], float]
    ) -> Matrix:
        """Retorna uma matriz num_rows x num_cols
        cuja entrada (i, j) é entry_fn(i, j)"""
        return [
            [
                entry_fn(i, j) for j in range(num_cols)  # com i, crie uma lista
            ]  # [entry_fn(i,0),...]
            for i in range(num_rows)
        ]  # cire uma lista para cada i

    # Com esta função, você pode criar uma MATRIZ IDENTIDADE 5x5
    # com 1s na diagonal e 0s nos outros pontos

    def identity_matriz(self, n: int) -> Matrix:
        """Retorna a matriz de identidade nxn"""
        return self.make_matrix(n, n, lambda i, j: 1 if i == j else 0)


if __name__ == "__main__":
    matriz = Matrizes()
    shape = matriz.shape([[1, 2, 3], [4, 5, 6]])
    assert shape == (2, 3)  # 2 linhas, 3 colunas
    _5x5_identity_matriz = matriz.identity_matriz(5)
    assert _5x5_identity_matriz == [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
    ]
