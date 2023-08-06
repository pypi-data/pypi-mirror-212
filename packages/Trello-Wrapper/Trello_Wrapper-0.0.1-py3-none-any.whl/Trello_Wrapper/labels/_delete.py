import abc
import requests
import json


class Delete:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def delete_label(self, label_id):
        """
        Delete a label by ID.

        Args:
            label_id (str): The ID of the Label.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/labels/{label_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)
