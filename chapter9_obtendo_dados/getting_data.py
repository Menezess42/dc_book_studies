## Stdin and Stdout
# Ao executar os scripts do Python na linha de comando(terminal),
# você pode canalizar(pipe) os dados por meio deles usando sys.stdin e
# sys.stdout. Por exemplo, este é um script que lê linhas de texto e devolve as que correspondem a uma expressão regular:

# egrep.py
# line_count.py
# Você pode usá-lo para contar as linhas de um arquivo que contêm números.

# No windows faça isso:
# type SomeFile.txt | python egrep.py "[0-9]"|python line_count.py

# Já no sistema Unix, faça isso:
# cat SomeFile.txt | python egrep.py "[0-9]"|python line_count.py

# O | é o caractere de pipe e significa "use a saída do comando à esquerda
# como a entrada do comando à direita. Como isso, você pode construir
# pipelines de processamento de dados bastante sofisticados

# Da mesma forma, este script conta as palavras na entrada e grava as mais comuns:
# most_common_words.py

## Lendo arquivos
# file_reading.py
