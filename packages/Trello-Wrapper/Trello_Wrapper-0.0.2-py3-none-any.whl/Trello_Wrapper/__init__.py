import os
from Trello_Wrapper.boards import Boards
from Trello_Wrapper.actions import Actions
from Trello_Wrapper.cards import Cards


class Trello():
    def __init__(self, token=None, api_key=None):
        if token is None:
            token = os.getenv('TRELLO_TOKEN')
        if api_key is None:
            api_key = os.getenv('TRELLO_API_KEY')

        if token is None or api_key is None:
            raise ValueError("Missing base token or API key")

        self.token = token
        self.api_key = api_key

    # Rest of the class methods...
    def Boards(self):
        return Boards(self.api_key, self.token)

    def Actions(self):
        return Actions(self.api_key, self.token)

    def Cards(self):
        return Cards(self.api_key, self.token)