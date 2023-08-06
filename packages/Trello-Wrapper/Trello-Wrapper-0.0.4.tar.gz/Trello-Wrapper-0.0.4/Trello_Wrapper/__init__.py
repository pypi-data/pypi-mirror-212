import os
from Trello_Wrapper.boards import Boards
from Trello_Wrapper.actions import Actions
from Trello_Wrapper.cards import Cards
from Trello_Wrapper.labels import Labels
from Trello_Wrapper.checklists import Checklists
from Trello_Wrapper.lists import Lists



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

    def Boards(self):
        return Boards(self.api_key, self.token)

    def Actions(self):
        return Actions(self.api_key, self.token)

    def Cards(self):
        return Cards(self.api_key, self.token)
    
    def Labels(self):
        return Labels(self.api_key, self.token)
    
    def Lists(self):
        return Lists(self.api_key, self.token)
    
    def Checklists(self):
        return Checklists(self.api_key, self.token)