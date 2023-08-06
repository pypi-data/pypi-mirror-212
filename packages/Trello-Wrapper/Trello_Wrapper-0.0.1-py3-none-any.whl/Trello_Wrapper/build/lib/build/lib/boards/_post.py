import abc
import requests
import json


class Post:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def create_board(self, name, default_labels=True, default_lists=True, desc=None, id_organization=None,
                     id_board_source=None, keep_from_source=None, power_ups=None, prefs_permission_level='private',
                     prefs_voting='disabled', prefs_comments='members', prefs_invitations='members',
                     prefs_self_join=True, prefs_card_covers=True, prefs_background='blue', prefs_card_aging='regular'):
        """
        Create a new board.

        Args:
            name (str): The new name for the board.
            default_labels (bool, optional): Determines whether to use the default set of labels. Default is True.
            default_lists (bool, optional): Determines whether to add the default set of lists to the board. Default is True.
            desc (str, optional): A new description for the board.
            id_organization (str, optional): The ID or name of the Workspace the board should belong to.
            id_board_source (str, optional): The ID of a board to copy into the new board.
            keep_from_source (str, optional): To keep cards from the original board, pass in the value "cards".
            power_ups (str, optional): The Power-Ups that should be enabled on the new board.
            prefs_permission_level (str, optional): The permissions level of the board. Default is "private".
            prefs_voting (str, optional): Who can vote on this board. Default is "disabled".
            prefs_comments (str, optional): Who can comment on cards on this board. Default is "members".
            prefs_invitations (str, optional): Determines what types of members can invite users to join. Default is "members".
            prefs_self_join (bool, optional): Determines whether users can join the boards themselves. Default is True.
            prefs_card_covers (bool, optional): Determines whether card covers are enabled. Default is True.
            prefs_background (str, optional): The id of a custom background or a predefined color. Default is "blue".
            prefs_card_aging (str, optional): Determines the type of card aging that should take place on the board.
                                              Default is "regular".

        Returns:
            dict: The JSON response containing the details of the created board.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = "https://api.trello.com/1/boards"

        query = {
            'name': name,
            'defaultLabels': str(default_labels).lower(),
            'defaultLists': str(default_lists).lower(),
            'desc': desc,
            'idOrganization': id_organization,
            'idBoardSource': id_board_source,
            'keepFromSource': keep_from_source,
            'powerUps': power_ups,
            'prefs_permissionLevel': prefs_permission_level,
            'prefs_voting': prefs_voting,
            'prefs_comments': prefs_comments,
            'prefs_invitations': prefs_invitations,
            'prefs_selfJoin': str(prefs_self_join).lower(),
            'prefs_cardCovers': str(prefs_card_covers).lower(),
            'prefs_background': prefs_background,
            'prefs_cardAging': prefs_card_aging,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def create_label(self, id, name=None, color=None):
        """
           Create a label on a board.

           Args:
               id (str): The id of the board to create the label on.
               name (str): The name of the label.
               color (str): The color of the label.

           Returns:
               int: The HTTP status code of the response. Returns 200 if successful.

           Raises:
               ValueError: If the `name` parameter is None or an empty string.
               Exception: If the response status code is not 200.
           """

        url = f"https://api.trello.com/1/boards/{id}/labels"

        if not name:
            raise ValueError("Name parameter must be provided.")

        query = {
            'name': name,
            'color': color,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.request(
            "POST",
            url,
            params=query
        )

        if response.status_code != 200:
            raise Exception(response.content)

        return 200

    def create_list(self, id, name, pos="top"):
        """
        Create a new list on a board.

        Args:
            id (str): The ID of the board to create the list on.
            name (str): The name of the list to be created. 1 to 16384 characters long.
            pos (str, optional): Determines the position of the list. Valid values: "top", "bottom", or a positive number.
                                 Default: "top"

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            ValueError: If the `name` parameter is None or an empty string.
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{id}/lists"

        if not name:
            raise ValueError("Name parameter must be provided.")

        query = {
            'name': name,
            'pos': pos,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.request(
            "POST",
            url,
            params=query
        )

        if response.status_code != 200:
            raise Exception(response.content)

        return 200

    def generate_calendar_key(self, board_id):
        """
        Generate a calendar key for a board.

        Args:
            board_id (str): The ID of the board to generate the calendar key for.

        Returns:
            dict: The JSON response containing the generated calendar key.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/calendarKey/generate"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def generate_email_key(self, board_id):
        """
        Generate an email key for a board.

        Args:
            board_id (str): The ID of the board to generate the email key for.

        Returns:
            dict: The JSON response containing the generated email key.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/emailKey/generate"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def create_board_tag(self, board_id, tag_id):
        """
        Create a tag for a board.

        Args:
            board_id (str): The ID of the board to create the tag for.
            tag_id (str): The ID of the tag to be added to the board.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/idTags"

        query = {
            'value': tag_id,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def mark_board_as_viewed(self, board_id):
        """
        Mark a board as viewed.

        Args:
            board_id (str): The ID of the board to mark as viewed.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/markedAsViewed"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

