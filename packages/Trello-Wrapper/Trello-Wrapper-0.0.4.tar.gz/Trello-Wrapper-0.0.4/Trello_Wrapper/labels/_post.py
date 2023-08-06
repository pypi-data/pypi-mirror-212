import abc
import requests
import json


class Post:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def create_label(self, name, color, board_id):
        """
        Create a new Label on a Board.

        Args:
            name (str): Name for the label.
            color (str): The color for the label.
            board_id (str): The ID of the Board to create the Label on.

        Returns:
            dict: The created label information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = "https://api.trello.com/1/labels"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        data = {
            'name': name,
            'color': color,
            'idBoard': board_id
        }

        response = requests.post(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()
