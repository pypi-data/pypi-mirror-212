import abc
import requests
import json


class Delete:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def delete_action(self, action_id):
        """
        Delete a specific action by its ID. Only comment actions can be deleted.

        Args:
            action_id (str): The ID of the action to delete.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def delete_reaction(self, action_id, reaction_id):
        """
        Delete a reaction.

        Args:
            action_id (str): The ID of the action.
            reaction_id (str): The ID of the reaction.

        Returns:
            None

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/reactions/{reaction_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return 200
