import abc
import requests
import json


class Delete:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def delete_board(self, id):
        """
        Delete a board
        Args:
            id: Board ID

        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "DELETE",
            url,
            headers=headers,
            params=query
        )
        if response.status_code != 200:
            raise Exception(response.content)

        return 200

    def remove_member(self, id, member_id):
        """
           Remove a member from a board.

           Args:
               id (str): The ID of the board to update.
               member_id (str): The ID of the member to remove from the board.

           Returns:
               int: The HTTP status code of the response. Returns 200 if successful.

           Raises:
               Exception: If the response status code is not 200.
           """
        url = f"https://api.trello.com/1/boards/{id}/members/{member_id}"
        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "DELETE",
            url,
            headers=headers,
            params=query
        )
        if response.status_code != 200:
            raise Exception(response.content)

        return 200