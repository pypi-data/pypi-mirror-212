import abc
import requests
import json


class Post:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def add_reaction_to_action(self, action_id, short_name=None, skin_variation=None, native=None, unified=None):
        """
        Adds a new reaction to an action.

        Args:
            action_id (str): The ID of the action.
            short_name (str, optional): The primary shortName of the emoji to add.
                                        Default: None.
            skin_variation (str, optional): The skinVariation of the emoji to add.
                                            Default: None.
            native (str, optional): The emoji to add as a native unicode emoji.
                                    Default: None.
            unified (str, optional): The unified value of the emoji to add.
                                     Default: None.

        Returns:
            dict: The added reaction details.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/reactions"

        payload = {
            'shortName': short_name,
            'skinVariation': skin_variation,
            'native': native,
            'unified': unified,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, json=payload)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()
