import abc
import requests
import json


class Delete:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def delete_checklist(self, checklist_id):
        """
        Delete a checklist.

        Args:
            checklist_id (str): The ID of the checklist to delete.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def remove_checklist_checkItem(self, checklist_id, checkItem_id):
        """
        Remove an item from a checklist.

        Args:
            checklist_id (str): The ID of the checklist.
            checkItem_id (str): The ID of the check item to remove.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems/{checkItem_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)
