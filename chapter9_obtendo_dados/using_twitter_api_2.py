from twython import TwythonStreamer

# # Acrescentar dados a uma variável global é um péssimo metodo
# # mas simplifica o exemplo
# tweets = []


# class MyStreamer(TwythonStreamer):
#     def on_success(self, data):
#         """O que fazer quando o twitter einvar os dados ?
#         Aqui, os dados serão um dict do python representando um tweet"""
#         # só queremos coletar tweet em inglês
#         if data.get("lang") == "en":
#             tweets.append(data)
#             print(f"recived tweet #{len(tweets)}")

#         # para quando o volume suficiente for coletado
#         if len(tweets) >= 100:
#             self.disconnect()

#     def on_error(self, status_code, data):
#         print(status_code, data)
#         self.disconnect()


# # o myStreamer se conecta ao stream do Twitter e aguarda os dados. Sempre que recebe um volumen
# # ele o insere no método on_success, que o acrescenta à lsita de tweets, quando ele está em inglês
# # e desconecta o streamer após a coleta de mil tweets.
# def starting():
#     from collections import Counter
#     import json
#     with open("credentials.json", "r") as file:
#         data = json.load(file)

#     stream = MyStreamer(data["api_key"],data['api_key_secret'],data['ACCESS_TOKEN'],data['ACCESS_TOKEN_SECRET'])
#     # para começar a consumir uma amostra de todos os status publicos
#     # stream.statuses.sample()
#     # A execução continuaŕa ae a coleta de cem tweets(ou até que surja um erro). Ao final
#     # comece a analisar os tweets. Por exemplo, para encontrar as hashtags mais comuns, faça isso
#     top_hashtags = Counter(hashtag['text'].lower()
#                            for tweet in tweets
#                            for hashtag in tweet["entitles"]["hashtags"])

#     print(top_hashtags.most_common(5))

# if __name__=="__main__":
#     starting()
def start():
    tweets = []
    import json
    with open("credentials.json", "r") as file:
        data = json.load(file)
    class MyStreamer(TwythonStreamer):
        def on_success(self, data):
            """
            What do we do when twitter sends us data?
            Here data will be a Python dict representing a tweet
            """
            # We only want to collect English-language tweets
            if data.get('lang') == 'en':
                tweets.append(data)
                print(f"received tweet #{len(tweets)}")

            # Stop when we've collected enough
            if len(tweets) >= 100:
                self.disconnect()

        def on_error(self, status_code, data):
            print(status_code, data)
            self.disconnect()

    stream = MyStreamer(data['api_key'],data['api_key_secret'],data['ACCESS_TOKEN'],data['ACCESS_TOKEN_SECRET'])

    # starts consuming public statuses that contain the keyword 'data'
    a = stream.statuses.filter(track='data')
    print(a)


if __name__=="__main__":
    start()



