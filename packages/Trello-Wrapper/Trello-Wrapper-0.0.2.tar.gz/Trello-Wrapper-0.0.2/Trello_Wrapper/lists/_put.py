import abc
import requests
import json


class Put:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def update_list(self, list_id, name=None, closed=None, idBoard=None, pos=None, subscribed=None):
        """
        Update the properties of a List.

        Args:
            list_id (str): The ID of the List.
            name (str, optional): New name for the list.
            closed (bool, optional): Whether the list should be closed (archived).
            idBoard (str, optional): ID of a board the list should be moved to.
            pos (str or float, optional): New position for the list: top, bottom, or a positive floating point number.
            subscribed (bool, optional): Whether the active member is subscribed to this list.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        if name is not None:
            query['name'] = name
        if closed is not None:
            query['closed'] = closed
        if idBoard is not None:
            query['idBoard'] = idBoard
        if pos is not None:
            query['pos'] = pos
        if subscribed is not None:
            query['subscribed'] = subscribed

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def close_list(self, list_id, value=True):
        """
        Archive or unarchive a list.

        Args:
            list_id (str): The ID of the list.
            value (bool, optional): Set to True to close (archive) the list. Default is True.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}/closed"

        query = {
            'value': str(value).lower(),
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def move_list_to_board(self, list_id, board_id):
        """
        Move a List to a different Board.

        Args:
            list_id (str): The ID of the list.
            board_id (str): The ID of the board to move the list to.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}/idBoard"

        query = {
            'value': board_id,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def rename_list(self, list_id, new_name):
        """
        Rename a list.

        Args:
            list_id (str): The ID of the list.
            new_name (str): The new name for the list.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}/name"

        query = {
            'value': new_name,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

