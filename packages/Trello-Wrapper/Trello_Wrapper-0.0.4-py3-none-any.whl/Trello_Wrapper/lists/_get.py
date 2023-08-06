import abc
import requests
import json


class Get:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def get_list(self, list_id, fields="name,closed,idBoard,pos"):
        """
        Get information about a single List.

        Args:
            list_id (str): The ID of the List.
            fields (str, optional): Specifies the fields to include in the list object.
                                    Valid values: "all" or a comma-separated list of fields.
                                    Default: "name,closed,idBoard,pos".

        Returns:
            dict: The list information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_list_actions(self, list_id, filter=None):
        """
        Get the Actions on a List.

        Args:
            list_id (str): The ID of the list.
            filter (str, optional): A comma-separated list of action types. Default is None.

        Returns:
            list: The list of actions on the list.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}/actions"

        query = {
            'filter': filter,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_list_board(self, list_id, fields="all"):
        """
        Get the board a list is on.

        Args:
            list_id (str): The ID of the list.
            fields (str, optional): Specifies the board fields to include in the response.
                                    Valid values: "all" or a comma-separated list of fields.
                                    Default: "all".

        Returns:
            dict: The board information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}/board"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_list_cards(self, list_id):
        """
        List the cards in a list.

        Args:
            list_id (str): The ID of the list.

        Returns:
            list: The list of cards in the list.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/lists/{list_id}/cards"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()
