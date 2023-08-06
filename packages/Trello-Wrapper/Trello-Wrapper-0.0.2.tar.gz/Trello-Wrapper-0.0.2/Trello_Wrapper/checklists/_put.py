import abc
import requests
import json


class Put:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def update_checklist(self, checklist_id, name=None, pos=None):
        """
        Update an existing checklist.

        Args:
            checklist_id (str): The ID of the checklist to update.
            name (str, optional): Name of the new checklist being created.
                                  Should be a string of length 1 to 16384.
            pos (str or int, optional): Determines the position of the checklist on the card.
                                        Valid values: "top", "bottom", or a positive number.

        Returns:
            dict: The updated checklist information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        data = {}
        if name is not None:
            data['name'] = name
        if pos is not None:
            data['pos'] = pos

        response = requests.put(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def update_checklist_field(self, checklist_id, field, value):
        """
        Update a specific field of a checklist.

        Args:
            checklist_id (str): The ID of the checklist.
            field (str): Field to update. Valid values: "name", "pos".
            value (str or int): The value to change the checklist field to.
                                Should be a string of length 1 to 16384 or a valid position value.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}/{field}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        data = {
            'value': value
        }

        response = requests.put(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)
