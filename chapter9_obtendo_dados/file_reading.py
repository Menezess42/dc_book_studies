# Working with text files
def workingWithTextFiles():
    # 'r' significa somente leitura, é o padrão se não for definido
    file_for_reading = open("reading_file.txt", "r")
    file_for_reading2 = open("reading_file.txt")

    # 'w' é gravar -- destrói tudo o que está no arquivo
    file_for_wrting = open("writing_file.txt", "w")

    # 'a' é acrescentar -- adiciona algo ao final do arquivo
    file_for_appending = open("appending_file.txt", "a")

    # não podemos esquecer de fechar o arquivo
    file_for_wrting.close()

    # Como é fácil esquecer de fechar os arquivos, sempre os utilize
    # em um bloco with, pois eles serão fechados automaticamente no final:
    with open(filename) as f:
        data = function_that_gets_data_from(f)

    # neste ponto, f já foi fechado, então não tente usá-lo
    process(data)

    # Para ler um arquivo de texto inteiro, basta iterar nas linhas do arquivo usando for
    starts_with_hash = 0
    with open("input.txt") as f:
        for line in f:  # analise cada linha do arquivo
            if re.match("^#", line):  # use um regex para determinar se começa com '#'
                starts_with_hash += 1  # se sim, adicione 1 à contagem


# Extracting emails from a file
def get_domain(email_adress: str) -> str:
    """Divida em '@' e retorne o último trecho"""
    return email_adress.lower().split("@")[-1]


def testing_get_domain():
    # dois testes
    assert get_domain("ariel@gmail.com") == "gmail.com"
    assert get_domain("ariel@datasciencester.com") == "datasciencester.com"


def count_domains():
    from collections import Counter

    with open("email_adress.txt", "r") as f:
        domain_count = Counter(get_domain(line.strip()) for line in f if "@" in line)
        return domain_count


def testing_count_domains():
    count = count_domains()
    print(count)


## Arquivos delimitadores
# básicamente arquivos csv, que uma linha tem vários campos e estes são
# separados por ; ou | ou : ou tabulaçẽos ou qualquer caracter assim.
# NUNCA ANALISE UM ARQUIVO SEPARADO POR VÍRGULAS POR CONTA PRÓPRIA. VOCÊ ESTRAGARÁ OS CASOS EXTERNOS!
# Se o arquivo não tiver cabeçalho (indicando que cada linha deve ser uma lista e que você precisa
# saber o conteúdo de cada coluna), use o csv.reader para iterar nas linhas de modo que cada uma delas gere uma lista separada de formaadequada.
# Por exemplo, imagine que temos um arquivo delimitado por tabulaçẽos com preços de ações:
# 6/20/2014 AAPL 90,91
# 6/20/2014 MSFT 41,68
# 6/20/2014 FB 90,91
# 6/19/2014 AAPL 91,86
# 6/19/2014 FB 64.34


def process(*args):
    date, symbol, closing_price = args
    print(f"date=>{date} symbol=>{symbol} closing_price=>{closing_price}")


import csv


# Podemos processá-los da seguinte forma:
def reading_tab_delimited_file():

    with open("tab_delimited_stock_prices.txt") as f:
        tab_reader = csv.reader(f, delimiter="\t")
        for row in tab_reader:
            date = row[0]
            symbol = row[1]
            closing_price = float(row[2])
            process(date, symbol, closing_price)


# Se o arquivo tiver cabeçalho:
# data:symbol:colosing_pricce
# é possíivel ignorar a linha de cabeçalho com uma chamada inicial para
# reder.next ou receber cada linha como um dict (usando os cabeçalhos como chaves)
# com o csv.DictReader:
def reading_headed_file():
    with open("colon_delimited_stock_prcies.txt") as f:
        colon_reader = csv.DictReader(f, delimiter=":")
        print("Here is the headed file:")
        for dict_row in colon_reader:
            date = dict_row["date"]
            symbol = dict_row["symbol"]
            closing_price = dict_row["closing_price"]
            process(date, symbol, closing_price)

# Mesmo se o arquivo não tiver cabeçalhos, você pode usar o DictReader, passando
# as chaves como parâmetro fieldname.

# Da mesma forma, é possível gravar os dados delimitadores usadno o csv.writer:
def writing_delimiter_data():
    todays_prices = {'APPL':90.91, 'MSFT': 41.68, 'FB': 64.5}
    with open('comma_delimited_stock_prices.txt', 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        for stock,price in todays_prices.items():
            csv_writer.writerow([stock,  price])

# O csv.writer sempre funciona quando os campos têm vírgulas. Um editor de texto convencional
# não. Por exemplo
def exemple():
    results = [["test1", "success", "monday"],["test2", "success, kind of", "tuesday"],["test3", "failure, kind of", "wednesday"],["test4","faliure, utter", "Thursday"]]
    # não faça isso
    with open('bad_csv.txt','w') as f:
        for row in results:
            f.write(",".join(map(str,row)))# talvez tenha muitas virgulas
            f.write("\n") # a linha também pode ter muitas newlines!
    # O arquivo resultante será algo parecido com isso:
    # test1,success,Monday
    # test2,success,kind of,Tuesday
    # test3,failure, kind of,Wednesday
    # test4,failure, utter, Thursday

if __name__ == "__main__":
    testing_get_domain()
    testing_count_domains()
    reading_tab_delimited_file()
    reading_headed_file()
    writing_delimiter_data()


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
