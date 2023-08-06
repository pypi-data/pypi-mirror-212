import abc
import requests
import json


class Post:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def create_list(self, name, idBoard, idListSource=None, pos=None):
        """
        Create a new List on a Board.

        Args:
            name (str): Name for the list.
            idBoard (str): The long ID of the board the list should be created on.
            idListSource (str, optional): ID of the List to copy into the new List.
            pos (str or float, optional): Position of the list: top, bottom, or a positive floating point number.

        Returns:
            dict: The created list information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = "https://api.trello.com/1/lists"

        query = {
            'name': name,
            'idBoard': idBoard,
            'key': self.api_key,
            'token': self.token
        }

        if idListSource is not None:
            query['idListSource'] = idListSource
        if pos is not None:
            query['pos'] = pos

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def archive_all_cards(self, list_id):
        """
        Archive all cards in a list.

        Args:
            list_id (str): The ID of the list.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}/archiveAllCards"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def move_all_cards(self, list_id, idBoard, idList):
        """
        Move all Cards in a List.

        Args:
            list_id (str): The ID of the list.
            idBoard (str): The ID of the board the cards should be moved to.
            idList (str): The ID of the list that the cards should be moved to.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}/moveAllCards"

        query = {
            'idBoard': idBoard,
            'idList': idList,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)
