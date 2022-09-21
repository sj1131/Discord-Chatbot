from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer as Trainer

class DiscordBot(ChatBot):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.name = name

    def train(self, data='chatterbot.corpus.korean'):
        trainer = Trainer(self)
        trainer.train(
            data
        )
    
    def chat(self, query):
        # return str(self.get_response(query.strip()))
        return str(self.get_response(query.strip()))


if __name__ == '__main__':
    bot = DiscordBot('TestBot')
    while True:
        # Get user input and print response
        req = input('User: ')
        if req == '':
            exit()
        else:
            res = bot.chat(req)
            print(bot.name + ': ' + res)
