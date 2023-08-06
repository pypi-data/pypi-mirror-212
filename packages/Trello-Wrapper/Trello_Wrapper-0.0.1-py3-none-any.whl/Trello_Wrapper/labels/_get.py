import abc
import requests
import json


class Get:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def get_label(self, label_id, fields="all"):
        """
        Get information about a single Label.

        Args:
            label_id (str): The ID of the Label.
            fields (str, optional): Specifies the fields to include in the label object.
                                    Valid values: "all" or a comma-separated list of fields.
                                    Default: "all".

        Returns:
            dict: The label information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/labels/{label_id}"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()
