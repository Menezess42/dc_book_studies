# Para extrair dados do HTML, usaremos a biblioteca Beautiful Soup.
# Beautiful Soup constrói uma árvore com os vários elementos da página
# da web e fornece uma interface simples de acesso a eles.
# Também usaremos a lib Request, uma maneira mais simpática de fazer solicitações
# ao HTTP do que os recursos do python.

# Para usar o beautful soup, passamos uma string com HTML para a funão beautfulSoup.
# Nos exemplos, este será o resultado de uma chamada para requests.get:
from bs4 import BeautifulSoup
import requests


## Introduction to web scraping
def some_web_scrap_exemples():
    # O arquvio HTML está no GitHub do Escritor
    url = "https://raw.githubusercontent.com/joelgrus/data/master/getting-data.html"
    html = requests.get(url).text
    print(f"html request: {html}\n---------\n")
    soup = BeautifulSoup(html, "html5lib")
    print(f"soup: {soup}\n---------\n")
    # Depois disso podemos ir bem longe usando alguns métodos simples

    # Geralmente, trabalharemos com objetos Tag, que correspondem às marcações (tags) da estrutura
    # da página HTML.

    # Por exemplo, para encontrar a primeira tag <p> (e seu contéudo), faça isto:
    first_paragraph = soup.find("p")  # ou apenas soup.p
    print(f"first_paragraph: {first_paragraph}\n---------\n")
    # Para obter o conteúdo de texto de uma tag, use a propriedade text:
    first_paragraph_text = soup.p.text
    print(f"first_paragraph_text: {first_paragraph_text}\n---------\n")
    first_paragraph_words = soup.p.text.split()
    print(f"first_paragraph_words: {first_paragraph_words}\n---------\n")

    # E para extrair os atritbutos de uma tag. trate-a como um dict:
    first_paragraph_id = soup.p["id"]  # gera keyerror se não houver 'id'
    print(f"first_paragraph_id: {first_paragraph_id}\n---------\n")
    first_paragraph_id2 = soup.p.get("id")  # retorna none se não houver 'id'
    print(f"first_paragraph_id2: {first_paragraph_id2}\n---------\n")

    # Para obter múltiplas tags ao mesmo tempo:
    all_paragraph = soup.find_all("p")  # ou apenas soup('p')
    print(f"all_paragraph: {all_paragraph}\n---------\n")
    paragraphs_with_ids = [p for p in soup("p") if p.get("id")]
    print(f"paragraphs_with_ids: {paragraphs_with_ids}\n---------\n")

    # Muitas vezes, você terá que encontrar tags com uma class específica:
    important_paragraphs = soup("p", {"class": "important"})
    print(f"important_paragraphs: {important_paragraphs}\n---------\n")
    important_paragraphs2 = soup("p", "important")
    print(f"important_paragraphs2: {important_paragraphs2}\n---------\n")
    important_paragraphs3 = [p for p in soup("p") if "important" in p.get("class", [])]
    print(f"important_paragraphs3: {important_paragraphs3}\n---------\n")
    # É possível combinar esses métodos para implementar uma lógica mais elaborada.
    # Por exemplo, para encontrar todos os elementos <span> contidos em um elemento <div>,
    # faça isto:
    # Aviso: retornará o mesmo <span> várias vezes
    # se ele estiver em vários <div>
    # fique atento a esse caso.
    span_inside_divs = [
        span for div in soup("div") for span in div("span")  # para cada <div> na página
    ]  # encontre cada <span> dentro dele
    print(f"span_inside_divs: {span_inside_divs}\n---------\n")
    #


# Claro que em geral, os dados importantes não são rotulados como class='important'. É preciso
# analisar atentamente o HTML de origem, a lógica de seleção e os casos extremos para confirmar
# se os dados estão corretos. vamos a um exemplo.


def paragraph_mentions(text: str, keyword: str) -> bool:
    """
    Returns True if a <p> inside the text mentions {keyword}
    """
    soup = BeautifulSoup(text, "html5lib")
    paragraphs = [p.get_text() for p in soup("p")]

    return any(keyword.lower() in paragraph.lower() for paragraph in paragraphs)


### Exemplo: Monitorando o congresso
def exemple_monitoring_the_congress():
    # Neste momento, há uma página com links para todos os sites dos parlamentares em
    # house.gov/representatives
    # quando clicamos em "Exibir código-fonte da pagina", esses links aparecem da seguinte forma
    # <td>
    #    <a href="https://jaypal.house.gov"> Jayapal, Pramila</a>
    # <td>
    # Começaremos coletando todos os URLs com links na página:
    import requests
    url = "https://www.house.gov/representatives"
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html5lib")

    all_urls = [a["href"] for a in soup("a") if a.has_attr("href")]

    print(len(all_urls))  # 965 for me, way too many

    import re

    # Must start with http:// or https://
    # Must end with .house.gov or .house.gov/
    regex = r"^https?://.*\.house\.gov/?$"

    # Let's write some tests!
    assert re.match(regex, "http://joel.house.gov")
    assert re.match(regex, "https://joel.house.gov")
    assert re.match(regex, "http://joel.house.gov/")
    assert re.match(regex, "https://joel.house.gov/")
    assert not re.match(regex, "joel.house.gov")
    assert not re.match(regex, "http://joel.house.com")
    assert not re.match(regex, "https://joel.house.gov/biography")

    # And now apply
    good_urls = [url for url in all_urls if re.match(regex, url)]

    print(len(good_urls))  # still 862 for me

    num_original_good_urls = len(good_urls)

    good_urls = list(set(good_urls))

    print(len(good_urls))  # only 431 for me

    assert len(good_urls) < num_original_good_urls

    html = requests.get("https://jayapal.house.gov").text
    soup = BeautifulSoup(html, "html5lib")

    # Use a set because the links might appear multiple times.
    links = {a["href"] for a in soup("a") if "press releases" in a.text.lower()}

    print(links)  # {'/media/press-releases'}

    # I don't want this file to scrape all 400+ websites every time it runs.
    # So I'm going to randomly throw out most of the urls.
    # The code in the book doesn't do this.
    import random

    good_urls = random.sample(good_urls, 5)
    print(f"after sampling, left with {good_urls}")

    from typing import Dict, Set

    press_releases: Dict[str, Set[str]] = {}

    for house_url in good_urls:
        html = requests.get(house_url).text
        soup = BeautifulSoup(html, "html5lib")
        pr_links = {a["href"] for a in soup("a") if "press releases" in a.text.lower()}
        print(f"{house_url}: {pr_links}")
        press_releases[house_url] = pr_links

    for house_url, pr_links in press_releases.items():
        for pr_link in pr_links:
            url = f"{house_url}/{pr_link}"
            text = requests.get(url).text

            if paragraph_mentions(text, "data"):
                print(f"{house_url}")
                break  # done with this house_url

    import requests, json

    # url = "https://www.house.gov/representatives"
    # text = requests.get(url).text
    # soup = BeautifulSoup(text, "html5lib")

    # all_urls = [a["href"] for a in soup("a") if a.has_attr("href")]

    # # print(len(all_urls))  # 965 for me, way too many

    # import re

    # # Must start with http:// or https://
    # # Must end with .house.gov or .house.gov/
    # regex = r"^https?://.*\.house\.gov/?$"

    # # Let's write some tests!
    # assert re.match(regex, "http://joel.house.gov")
    # assert re.match(regex, "https://joel.house.gov")
    # assert re.match(regex, "http://joel.house.gov/")
    # assert re.match(regex, "https://joel.house.gov/")
    # assert not re.match(regex, "joel.house.gov")
    # assert not re.match(regex, "http://joel.house.com")
    # assert not re.match(regex, "https://joel.house.gov/biography")

    # # And now apply
    # good_urls = [url for url in all_urls if re.match(regex, url)]

    # # print(len(good_urls))  # still 862 for me

    # # Os resultados aainda ultrapassam os 435 parlamentares, pos a lista contém muitas
    # # duplicatas. Usaremos o set para eliminá-las:
    # good_urls = list(set(good_urls))
    # # print(len(good_urls)) # O congresso sempre tem uns cargos vagos ou parlamentares sem sites
    # # então 431 é um bom resultado

    # # A maioria dos sites contém um link para os comunicados da imprensa (press release)
    # # Por exemplo:
    # html = requests.get("https://jayapal.house.gov").text
    # soup = BeautifulSoup(html, "html5lib")

    # # Use um conjunto porque os links talvez surjam várias vezes
    # # Use a set because the links might appear multiple times.
    # links = {a["href"] for a in soup("a") if "press releases" in a.text.lower()}

    # # print(links) # {'/media/press-releases'}

    # # Esse é um link relativo, logo, temos que lembrar do site original. Vamos extrair mais informações
    # from typing import Dict, Set

    # press_releases: Dict[str, Set[str]] = {}
    # j = 0
    # for house_url in good_urls:
    #     # print("inside this for geting the data")
    #     html = requests.get(house_url).text
    #     soup = BeautifulSoup(html, "html5lib")
    #     pr_links = {a["href"] for a in soup("a") if "press releases" in a.text.lower()}
    #     # print(f"{house_url}: {pr_links}")
    #     press_releases[house_url] = pr_links
    #     # print(f"\tCollected {j}thº data\n")
    #     if j == 100:
    #         break
    #     j += 1

    # # Agora, estamos prontos para encontrar os parlamentares certos e informar seus
    # # nomes ao vice-presidente
    # j = 0
    # for house_url, pr_links in press_releases.items():
    #     print(f"{j}ºth entrou for")
    #     for pr_link in pr_links:
    #         print("entrou segundo for")
    #         url = f"{house_url}/{pr_link}"
    #         text = requests.get(url).text

    #         if paragraph_mentions(text, "data"):
    #             print(f"{house_url}")
    #             break  # done with this house_url
    #     print(f"{j}ºth saiu segundo for")
    #     j += 1

    # # Quando analisamos várias páginas de comunicados de imprensa,
    # # observamos que a maioria contém apenas 5 ou 10 comunicados por
    # # página. isso indica que só recuperamos os mais recentes de cada
    # # congressista. uma solução mais completa é iterar as páginas e
    # # recuperar o texto completo de cada comunicado de imprensa.


# Observe que há muitos termos como /media/press-releases e media-center/press-releases
# bem como outros endereços.

# O objetivo é identificar os congressistas cujos comunicados de imprensa citam a
# palavra "data"(dados). então, escrevemos uma função um pouco mais geral para verificar
# se a página de comunicados da imprensa contém um termo específico.

# No código-fonte do site, vemos que há um trecho de cada comunicado em uma tag <p>; então,
# usaremos isso na primeira tentativa


def test_paragraph_mention():
    text = """<body><h1>Facebook</h1><p>Twitter</p>"""
    assert paragraph_mentions(text, "twitter")  # está em um <p>
    assert not paragraph_mentions(text, "facebook")  # não está em um <p>


if __name__ == "__main__":
    exemple_monitoring_the_congress()
    # test_paragraph_mention()
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
#
#
#
