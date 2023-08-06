import abc
import requests
import json


class Delete:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def delete_card(self, card_id):
        """
        Delete a card by its ID.

        Args:
            card_id (str): The ID of the card to delete.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}"

        query = {
            'key': self.api_key,
            'token': self.token,
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def delete_card_attachment(self, card_id, attachment_id):
        """
        Delete an attachment from a card.

        Args:
            card_id (str): The ID of the card.
            attachment_id (str): The ID of the attachment.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/attachments/{attachment_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

