import abc
import requests
import json


class Put:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def update_label(self, label_id, name=None, color=None):
        """
        Update a label by ID.

        Args:
            label_id (str): The ID of the Label.
            name (str, optional): The new name for the label.
            color (str, optional): The new color for the label.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/labels/{label_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        data = {}

        if name is not None:
            data['name'] = name

        if color is not None:
            data['color'] = color

        response = requests.put(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)

    def update_label_field(self, label_id, field, value):
        """
        Update a field on a label.

        Args:
            label_id (str): The ID of the Label.
            field (str): The field on the Label to update.
            value (str): The new value for the field.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/labels/{label_id}/{field}"

        query = {
            'key': self.api_key,
            'token': self.token,
            'value': value
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)
