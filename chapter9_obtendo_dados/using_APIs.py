# You can read json files like they are python dict
# {
#     "title": "Data Science Book",
#     "author": "Joel Grus",
#     "publicationYear": 2019,
#     "topics": ["data", "science", "data sciencec"]
# }
def showing_usage_of_json():
    import json
    serialized = """
    {
        "title": "Data Science Book",
        "author": "Joel Grus",
        "publicationYear": 2019,
        "topics": ["data", "science", "data science"]
    }"""

    # Analise o JSON para criar um dict do Python
    deserialized = json.loads(serialized)
    assert deserialized['publicationYear'] == 2019
    assert "data science" in deserialized['topics']

### Usando uma API não autenticada
def using_api_not_autenticated():
    import requests, json
    github_user = "Menezess42"
    endpoint = f"https://api.github.com/user/{github_user}/repos"
    repos = json.loads(requests.get(endpoint).text)
    # repos é uma lsit de dicts do python. Cada dict é um public repository do meu github.

    # Assim, é possível definir os meses e dias da semana com mais probabilidade de eu criar
    # um repositório, mas a data vem como string, e o python não sabe tratar muito bem datas,
    # por isso vamos usar a lib python-dateutil
    from collections import Counter
    from dateutil.parser import parse

    dates = [parse(repo["created_at"]) for repo in repos]
    month_counts = Counter(date.mont for date in dates)
    weekday_counts = Counter(date.weekday() for date in dates)

    # Da mesma forma é possível obter as linguagens dos meus últimos 5 repositories
    last_5_repositories = sorted(repos,
                                 key=lambda r: r["pushed_at"],
                                 reverse=True)[:5]
    last_5_repositories = [repo["language"]
                           for repo in last_5_repositories]
# Como talvez seja necessário instalar uma biblioteca de acesso à API (ou mais provável, resolver uma falha em outra biblioteca), é bom aprender alguma coisa.
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

