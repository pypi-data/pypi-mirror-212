import abc
import requests
import json
import re


class Put:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def update_action(self, action_id, new_text):
        """
        Update a specific action by its ID. Only comment actions can be updated.

        Args:
            action_id (str): The ID of the action to update.
            new_text (str): The new text for the comment.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}"

        query = {
            'text': new_text,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def update_comment(self, action_id, new_text):
        """
        Update a comment action by its ID.

        Args:
            action_id (str): The ID of the action to update.
            new_text (str): The new text for the comment.

        Returns:
            dict: The updated comment action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/text"

        query = {
            'value': new_text,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def list_reactions(self, action_id, load_member=True, load_emoji=True):
        """
        List reactions for an action by its ID.

        Args:
            action_id (str): The ID of the action.
            load_member (bool, optional): Specifies whether to load the member as a nested resource.
                                          Default: True.
            load_emoji (bool, optional): Specifies whether to load the emoji as a nested resource.
                                         Default: True.

        Returns:
            dict: The reactions for the action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/reactions"

        query = {
            'member': str(load_member).lower(),
            'emoji': str(load_emoji).lower(),
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()


    def get_reaction(self, action_id, reaction_id, load_member=True, load_emoji=True):
        """
        Get information for a reaction.

        Args:
            action_id (str): The ID of the action.
            reaction_id (str): The ID of the reaction.
            load_member (bool, optional): Whether to load the member as a nested resource.
                                          Default: True.
            load_emoji (bool, optional): Whether to load the emoji as a nested resource.
                                         Default: True.

        Returns:
            dict: The reaction information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/reactions/{reaction_id}"

        query = {
            'member': str(load_member).lower(),
            'emoji': str(load_emoji).lower(),
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

