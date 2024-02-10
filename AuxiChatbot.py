import re
from difflib import SequenceMatcher

class Chatbot():
    def __init__(self):
        self.tokens = []
        with open('./conjunctions.txt', 'r') as f:
            self.conjunctions = [conjunction.rstrip() for conjunction in f.readlines()]
            f.close()
        with open('./messages.txt', 'r') as f:
            file = f.readlines()
            self.messages = [message.rstrip().split('|')[0].rstrip() for message in file]
            self.responses = [message.rstrip().split('|')[1].rstrip() for message in file]
            f.close()

    def process(self, existing_tokens):
        for token in existing_tokens:
            for conjunction in self.conjunctions:
                if conjunction in token:
                    self.process(token.split(conjunction))
                elif token.lstrip().rstrip() not in self.tokens and not any(x in token for x in self.conjunctions):
                    self.add_token(token.lstrip().rstrip())
        print(self.tokens)

    def refresh(self):
        with open('./conjunctions.txt', 'r') as f:
            self.conjunctions = [conjunction.rstrip() for conjunction in f.readlines()]
            f.close()
        with open('./messages.txt', 'r') as f:
            file = f.readlines()
            self.messages = [message.rstrip().split('|')[0].rstrip() for message in file]
            self.responses = [message.rstrip().split('|')[1].rstrip() for message in file]
            f.close()

    def check_similarity(self, piece, item):
        rating = SequenceMatcher(None, piece.lower(), item.lower()).ratio()
        if rating > 0.7:
            return True
        else:
            return False
    
    def reset_tokens(self):
        self.tokens = []
    
    def add_token(self, token):
        self.tokens.append(token)

    def get_response(self, message):
        response = ''
        self.reset_tokens()
        self.process(message)
        split_message = self.tokens
        for item in self.messages:
            for piece in split_message:
                if self.check_similarity(piece, item):
                    response += self.responses[self.messages.index(item)]
                else:
                    response += ""
        return response.rstrip().lstrip()
