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

    def delete_card_check_item(self, card_id, check_item_id):
        """
        Delete a checklist item on a card.

        Args:
            card_id (str): The ID of the card.
            check_item_id (str): The ID of the checkItem.
        Return:
            200 if deleted successfully
        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/checkItem/{check_item_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)


    def remove_label_from_card(self, card_id, label_id):
        """
        Remove a label from a card.

        Args:
            card_id (str): The ID of the card.
            label_id (str): The ID of the label to remove.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/idLabels/{label_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def remove_member_from_card(self, card_id, member_id):
        """
        Remove a member from a card.

        Args:
            card_id (str): The ID of the card.
            member_id (str): The ID of the member to remove.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/idMembers/{member_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def remove_member_vote_from_card(self, card_id, member_id):
        """
        Remove a member's vote from a card.

        Args:
            card_id (str): The ID of the card.
            member_id (str): The ID of the member whose vote to remove.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/membersVoted/{member_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def delete_checklist(self, card_id, checklist_id):
        """
        Delete a checklist from a card.

        Args:
            card_id (str): The ID of the card.
            checklist_id (str): The ID of the checklist to delete.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/checklists/{checklist_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.delete(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)
