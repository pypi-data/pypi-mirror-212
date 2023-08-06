import abc
import requests
import json
import re


class Put:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def update_board(self, id, name=None, desc=None, closed=None, subscribed=None, idOrganization=None,
                     permissionLevel=None, selfJoin=None, cardCovers=None, hideVotes=None, invitations=None,
                     voting=None, comments=None, background=None, cardAging=None, calendarFeedEnabled=None,
                     labelNames=None):
        """
        Update an existing board by id.

        Args:
            id (str): The id of the board to be updated.

            name (str, optional): The new name for the board. 1 to 16384 characters long.

            desc (str, optional): A new description for the board, 0 to 16384 characters long.

            closed (bool, optional): Whether the board is closed.

            subscribed (str, optional): Whether the acting user is subscribed to the board.

            idOrganization (str, optional): The id of the Workspace the board should be moved to.

            permissionLevel (str, optional): One of: org, private, public.

            selfJoin (bool, optional): Whether Workspace members can join the board themselves.

            cardCovers (bool, optional): Whether card covers should be displayed on this board.

            hideVotes (bool, optional): Determines whether the Voting Power-Up should hide who voted on cards or not.

            invitations (str, optional): Who can invite people to this board. One of: admins, members.

            voting (str, optional): Who can vote on this board. One of disabled, members, observers, org, public.

            comments (str, optional): Who can comment on cards on this board. One of: disabled, members, observers, org, public.

            background (str, optional): The id of a custom background or one of: blue, orange, green, red, purple, pink, lime, sky, grey.

            cardAging (str, optional): One of: pirate, regular.

            calendarFeedEnabled (bool, optional): Determines whether the calendar feed is enabled or not.

            labelNames (dict, optional): Dictionary containing label names for different colors.
                The keys should be: green, yellow, orange, red, purple, blue.

        Returns:
            bool: True if the board update was successful, False otherwise.
        """

        url = f"https://api.trello.com/1/boards/{id}"

        query_params = {
            'key': self.api_key,
            'token': self.token,
            "name": name,
            "desc": desc,
            "closed": closed,
            "subscribed": subscribed,
            "idOrganization": idOrganization,
            "prefs/permissionLevel": permissionLevel,
            "prefs/selfJoin": selfJoin,
            "prefs/cardCovers": cardCovers,
            "prefs/hideVotes": hideVotes,
            "prefs/invitations": invitations,
            "prefs/voting": voting,
            "prefs/comments": comments,
            "prefs/background": background,
            "prefs/cardAging": cardAging,
            "prefs/calendarFeedEnabled": calendarFeedEnabled,
            "labelNames/green": labelNames.get('green') if labelNames else None,
            "labelNames/yellow": labelNames.get('yellow') if labelNames else None,
            "labelNames/orange": labelNames.get('orange') if labelNames else None,
            "labelNames/red": labelNames.get('red') if labelNames else None,
            "labelNames/purple": labelNames.get('purple') if labelNames else None,
            "labelNames/blue": labelNames.get('blue') if labelNames else None
        }

        response = requests.put(url, params=query_params)
        if response.status_code != 200:
            raise Exception(response.content)
        return 200

    def invite_member(self, id, email, member_type="normal", full_name=None):
        """
        Invite a member to a board via their email address.

        Args:
            id (str): The ID of the board to invite the member to.
            email (str): The email address of the user to add as a member of the board.
            member_type (str, optional): Determines what type of member the user being added should be of the board.
                                         Valid values: "admin", "normal", "observer". Default: "normal".
            full_name (str, optional): The full name of the user to add as a member of the board.
                                       Must have a length of at least 1 and cannot begin nor end with a space.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            ValueError: If the `email` parameter is None or an empty string.
            Exception: If the response status code is not 200.
        """
        if not email:
            raise ValueError("Email parameter must be provided.")

        url = f"https://api.trello.com/1/boards/{id}/members"

        query = {
            'email': email,
            'type': member_type,
            'fullName': full_name,
            'key': self.api_key,
            'token': self.token
        }
        response = requests.put(url, params=query)
        if response.status_code != 200:
            raise Exception(response.content)
        return 200

    def add_member(self, id, member_id, member_type, allow_billable_guest=False):
        """
        Add a member to a board.

        Args:
            id (str): The ID of the board to update.
            member_id (str): The ID of the member to add to the board.
            member_type (str): Determines the type of member this user will be on the board.
                               Valid values: "admin", "normal", "observer".
            allow_billable_guest (bool, optional): Optional parameter that allows organization admins
                                                    to add multi-board guests onto a board. Default: False.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            ValueError: If the `member_type` parameter is not one of the valid values.
            Exception: If the response status code is not 200.
        """

        valid_member_types = ["admin", "normal", "observer"]

        if member_type not in valid_member_types:
            raise ValueError(f"Invalid member_type. Valid values are: {', '.join(valid_member_types)}")

        url = f"https://api.trello.com/1/boards/{id}/members/{member_id}"

        query = {
            'type': member_type,
            'allowBillableGuest': allow_billable_guest,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def update_membership(self, id, membership_id, member_type, member_fields="fullName, username"):
        """
        Update an existing board's membership by ID.

        Args:
            id (str): The ID of the board to update.
            membership_id (str): The ID of the membership to be added to the board.
            member_type (str): Determines the type of member that this membership will be to this board.
                               Valid values: "admin", "normal", "observer".
            member_fields (str, optional): Specifies the fields to include in the member object.
                                           Valid values: "all", "avatarHash", "bio", "bioData", "confirmed",
                                                         "fullName", "idPremOrgsAdmin", "initials", "memberType",
                                                         "products", "status", "url", "username".
                                           Default: "fullName, username".

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            ValueError: If the `member_type` parameter is not one of the valid values.
            Exception: If the response status code is not 200.
        """

        valid_member_types = ["admin", "normal", "observer"]
        if member_type not in valid_member_types:
            raise ValueError(f"Invalid member_type. Valid values are: {', '.join(valid_member_types)}")

        url = f"https://api.trello.com/1/boards/{id}/memberships/{membership_id}"

        query = {
            'type': member_type,
            'member_fields': member_fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def update_email_position(self, id, value="top"):
        """
        Update the emailPosition preference on a board.

        Args:
            id (str): The ID of the board to update.
            value (str): Determines the position of the email address.
                         Valid values: "bottom", "top".

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            ValueError: If the `value` parameter is not one of the valid values.
            Exception: If the response status code is not 200.
        """

        valid_values = ["bottom", "top"]
        if value not in valid_values:
            raise ValueError(f"Invalid value. Valid values are: {', '.join(valid_values)}")

        url = f"https://api.trello.com/1/boards/{id}/myPrefs/emailPosition"

        query = {
            'value': value,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def update_id_email_list(self, board_id, value):
        """
        Update the idEmailList preference on a board.

        Args:
            board_id (str): The ID of the board to update.
            value (str): The ID of an email list.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            ValueError: If the `value` parameter does not match the expected pattern.
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/myPrefs/idEmailList"

        pattern = "^[0-9a-fA-F]{24}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid value. The value must match the pattern: ^[0-9a-fA-F]{24}$")

        query = {
            'value': value,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def show_list_guide(self, board_id, value):
        """
        Update the showListGuide preference on a board.

        Args:
            board_id (str): The ID of the board to update.
            value (bool): Determines whether to show the list guide.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/myPrefs/showListGuide"

        query = {
            'value': str(value).lower(),
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def show_sidebar(self, board_id, value):
        """
        Update the showSidebar preference on a board.

        Args:
            board_id (str): The ID of the board to update.
            value (bool): Determines whether to show the sidebar.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/myPrefs/showSidebar"

        query = {
            'value': str(value).lower(),
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def show_sidebar_activity(self, board_id, value):
        """
        Update the showSidebarActivity preference on a board.

        Args:
            board_id (str): The ID of the board to update.
            value (bool): Determines whether to show sidebar activity.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/myPrefs/showSidebarActivity"

        query = {
            'value': str(value).lower(),
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def show_sidebar_board_actions(self, board_id, value):
        """
        Update the showSidebarBoardActions preference on a board.

        Args:
            board_id (str): The ID of the board to update.
            value (bool): Determines whether to show the sidebar board actions.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/myPrefs/showSidebarBoardActions"

        query = {
            'value': str(value).lower(),
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code

    def update_show_sidebar_members(self, board_id, value):
        """
        Update the showSidebarMembers preference on a board.

        Args:
            board_id (str): The ID of the board to update.
            value (bool): Determines whether to show members of the board in the sidebar.

        Returns:
            int: The HTTP status code of the response. Returns 200 if successful.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/myPrefs/showSidebarMembers"

        query = {
            'value': str(value).lower(),
            'key': self.api_key,
            'token': self.token
        }

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.status_code


