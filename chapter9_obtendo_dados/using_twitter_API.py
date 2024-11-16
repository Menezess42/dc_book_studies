# # Exemplo: usando as APIs do Twitter
# # A parte mais complexa de usar a API do Twitter é a autenticação,
# # na verdade essa é a maior dificuldade em muitas APIs

# # Primeiro, você precisa da cahve da API [API key] e da chave secreta da API [API secret key]
# # (também conhecidas como chave do consumidor e segredo do consumidor, respectivamente).

# # Acessando as chaves
# import json
# with open('credentials.json', 'r') as file:
#     data = json.load(file)

# # Criando uma instância de cliente
# import webbrowser
# from twython import Twython
# CONSUMER_KEY = data['api_key']
# CONSUMER_SECRET = data['api_key_secret']
# # configure um cliente temporário para recuperar uma URL de autenticação
# temp_client = Twython(CONSUMER_KEY, CONSUMER_SECRET)
# temp_creds = temp_client.get_authentication_tokens()
# url = temp_creds['auth_url']

# # Agora, acesse a URL para autorizar o aplicativo e obter um PIN
# print(f"go visit {url} and get the PIN code and paste it bellow")
# webbrowser.open(uerl)
# PIN_CODE = input('please enter the PIN code: ')

# # Agora usamos o PIN_CODE para obeter os tokens reais
# auth_client = Twython(CONSUMER_KEY,
#                       CONSUMER_SECRET,
#                       temp_creds['oauth_token'],
#                       temp_creds['oauth_token_secret'])
# final_step = auth_client.get_authorized_tokens(PIN_CODE)
# ACCESS_TOKEN = final_step['oauth_token']
# ACCESS_TOKEN_SECRET = final_step['oauth_token_secret']
# data['ACCESS_TOKEN'] = ACCESS_TOKEN
# data['ACCESS_TOKEN_SECRET'] = ACCESS_TOKEN_SECRET
# with open('credentials.json', 'w') as file:
#     json.dump(data, file, indent=4)
# # e obter uma nova instância do Twython com eles.
# twitter = Twython(CONSUMER_KEY,
#                   CONSUMER_SECRET,
#                   ACCESS_TOKEN,
#                   ACCESS_TOKEN_SECRET)
# # Com uma instância do twython autenticada, podemos começar as pesquisas:
# # Pesquise tweets que contenham a expressão 'data science'
# for status in twitter.search(q='"data science"')["status"]:
#     user = status["user"]["screen_name"]
#     text = status["text"]
#     print(f"{user}: {text}\n")
import json
import webbrowser
from twython import Twython

with open("credentials.json", "r") as file:
    data = json.load(file)

# Criando uma instância de cliente
CONSUMER_KEY = data["api_key"]
CONSUMER_SECRET = data["api_key_secret"]

# Get a temporary client to retrieve an authentication url
temp_client = Twython(CONSUMER_KEY, CONSUMER_SECRET)
temp_creds = temp_client.get_authentication_tokens()
url = temp_creds["auth_url"]

# Now visit that URL to authorize the application and get a PIN
print(f"go visit {url} and get the PIN code and paste it below")
webbrowser.open(url)
PIN_CODE = input("please enter the PIN code: ")

# Now we use that PIN_CODE to get the actual tokens
auth_client = Twython(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    temp_creds["oauth_token"],
    temp_creds["oauth_token_secret"],
)
final_step = auth_client.get_authorized_tokens(PIN_CODE)
ACCESS_TOKEN = final_step["oauth_token"]
ACCESS_TOKEN_SECRET = final_step["oauth_token_secret"]

# And get a new Twython instance using them.
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# print(twitter)
aa = twitter.cursor(twitter.search, q='"data science"')
print(aa)
# Iterate over the generator and print each tweet's information
for status in aa:
    user = status["user"]["screen_name"]
    text = status["text"]
    print(f"{user}: {text}\n")
# for status in twitter.search(q='"data science"')["status"]:
#     user = status["user"]["screen_name"]
#     text = status["text"]
#     print(f"{user}: {text}\n")
