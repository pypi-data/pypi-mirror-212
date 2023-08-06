import abc
import requests
import json


class Get:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def get_all_boards(self):
        """
        Get all boards related to the user
        Returns:
            Json containing all the boards data
        """
        url = f"https://api.trello.com/1/members/me/boards"
        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )
        if response.status_code != 200:
            raise Exception(response.content)
        return response.json()

    def get_boards_ids(self):
        """
        Get Boards Ids
        Returns:

        """
        url = f"https://api.trello.com/1/members/me/boards"
        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )
        if response.status_code != 200:
            raise Exception(response.content)
        return {board["name"]: board["id"] for board in response.json()}

    def get_memberships_of_board(self, id: str):
        """
        Get information about the memberships users have to the board.
        Args:
            id: (string) The ID of the board => Pattern: ^[0-9a-fA-F]{24}$

        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}/memberships"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return json.loads(response.text)

    def get_board(self, board_id, actions="all", board_stars="none", cards="none", card_plugin_data=False,
                  checklists="none", custom_fields=False,
                  fields="name,desc,descData,closed,idOrganization,pinned,url,shortUrl,prefs,labelNames",
                  labels=False, lists="open", members="none", memberships="none", plugin_data=False,
                  organization=False, organization_plugin_data=False, my_prefs=False, tags=False):
        """
        Get a single board by its ID.

        Args:
            board_id (str): The ID of the board.
            actions (str, optional): Specifies whether to include actions as a nested resource.
                                     Valid values: "all", "none".
                                     Default: "all".
            board_stars (str, optional): Specifies whether to include board stars.
                                         Valid values: "mine", "none".
                                         Default: "none".
            cards (str, optional): Specifies whether to include cards as a nested resource.
                                   Valid values: "all", "none".
                                   Default: "none".
            card_plugin_data (bool, optional): Specifies whether to include card pluginData with the response.
                                               Default: False.
            checklists (str, optional): Specifies whether to include checklists as a nested resource.
                                        Valid values: "all", "none".
                                        Default: "none".
            custom_fields (bool, optional): Specifies whether to include custom fields as a nested resource.
                                            Default: False.
            fields (str, optional): Specifies the fields of the board to be included in the response.
                                    Valid values: "all" or a comma-separated list of: closed, dateLastActivity,
                                                  dateLastView, desc, descData, idMemberCreator, idOrganization,
                                                  invitations, invited, labelNames, memberships, name, pinned,
                                                  powerUps, prefs, shortLink, shortUrl, starred, subscribed, url.
                                    Default: "name,desc,descData,closed,idOrganization,pinned,url,shortUrl,prefs,labelNames".
            labels (bool, optional): Specifies whether to include labels as a nested resource.
                                     Default: False.
            lists (str, optional): Specifies whether to include lists as a nested resource.
                                   Valid values: "all", "none", "open".
                                   Default: "open".
            members (str, optional): Specifies whether to include members as a nested resource.
                                     Valid values: "all", "none".
                                     Default: "none".
            memberships (str, optional): Specifies whether to include memberships as a nested resource.
                                         Valid values: "all", "none".
                                         Default: "none".
            plugin_data (bool, optional): Specifies whether to include the pluginData for this board.
                                          Default: False.
            organization (bool, optional): Specifies whether to include the organization as a nested resource.
                                           Default: False.
            organization_plugin_data (bool, optional): Specifies whether to include organization pluginData with the response.
                                                       Default: False.
            my_prefs (bool, optional): Specifies whether to include the preferences for the current user.
                                       Default: False.
            tags (bool, optional): Specifies whether to include tags (collections) that the board belongs to.
                                   Default: False.

        Returns:
            dict: The board information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}"

        query = {
            'actions': actions,
            'boardStars': board_stars,
            'cards': cards,
            'card_pluginData': card_plugin_data,
            'checklists': checklists,
            'customFields': custom_fields,
            'fields': fields,
            'labels': labels,
            'lists': lists,
            'members': members,
            'memberships': memberships,
            'pluginData': plugin_data,
            'organization': organization,
            'organization_pluginData': organization_plugin_data,
            'myPrefs': my_prefs,
            'tags': tags,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_board_field(self, board_id, field):
        """
        Get a specific field on a board.

        Args:
            board_id (str): The ID of the board.
            field (str): The field you'd like to receive.
                          Valid values: "closed", "dateLastActivity", "dateLastView", "desc", "descData",
                                        "idMemberCreator", "idOrganization", "invitations", "invited", "labelNames",
                                        "memberships", "name", "pinned", "powerUps", "prefs", "shortLink",
                                        "shortUrl", "starred", "subscribed", "url".

        Returns:
            Any: The value of the specified field on the board.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/{field}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_actions(self, board_id, fields=None, action_types=None, format='list', id_models=None,
                          limit=50, include_member=True, member_fields=None, include_member_creator=True,
                          member_creator_fields=None, page=0, include_reactions=False, before=None, since=None):
        """
        Get the actions for a board.

        Args:
            board_id (str): The ID of the board.
            fields (str): The fields to be returned for the actions.
                          See available fields here: https://developers.trello.com/reference#action-fields
            action_types (str): A comma-separated list of action types.
            format (str): The format of the returned actions. Either "list" or "count".
            id_models (str): A comma-separated list of model IDs. Only actions related to these models will be returned.
            limit (int): The limit of the number of responses, between 0 and 1000.
            include_member (bool): Whether to return the member object for each action.
            member_fields (str): The fields of the member to return.
            include_member_creator (bool): Whether to return the memberCreator object for each action.
            member_creator_fields (str): The fields of the member creator to return.
            page (int): The page of results for actions.
            include_reactions (bool): Whether to show reactions on comments or not.
            before (str): An Action ID. Only actions that occurred before this action will be returned.
            since (str): An Action ID. Only actions that occurred after this action will be returned.

        Returns:
            dict: The actions for the specified board.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/actions"

        query = {
            'key': self.api_key,
            'token': self.token,
            'fields': fields,
            'filter': action_types,
            'format': format,
            'idModels': id_models,
            'limit': limit,
            'member': include_member,
            'member_fields': member_fields,
            'memberCreator': include_member_creator,
            'memberCreator_fields': member_creator_fields,
            'page': page,
            'reactions': include_reactions,
            'before': before,
            'since': since
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_cards(self, id: str):
        """
        Get cards on a board
        Args:
            id: (string) The ID of the board => Pattern: ^[0-9a-fA-F]{24}$

        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}/cards"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response.json()

    def get_card(self, board_id, card_id, fields=None, action_types=None, format='list', id_models=None,
                       limit=50, include_member=True, member_fields=None, include_member_creator=True,
                       member_creator_fields=None, page=0, include_reactions=False, before=None, since=None):
        """
        Get a single card on a board.

        Args:
            board_id (str): The ID of the board.
            card_id (str): The ID of the card to retrieve.
            fields (str): The fields to be returned for the actions.
                          See available fields here: https://developers.trello.com/reference#action-fields
            action_types (str): A comma-separated list of action types.
            format (str): The format of the returned actions. Either "list" or "count".
            id_models (str): A comma-separated list of model IDs. Only actions related to these models will be returned.
            limit (int): The limit of the number of responses, between 0 and 1000.
            include_member (bool): Whether to return the member object for each action.
            member_fields (str): The fields of the member to return.
            include_member_creator (bool): Whether to return the memberCreator object for each action.
            member_creator_fields (str): The fields of the member creator to return.
            page (int): The page of results for actions.
            include_reactions (bool): Whether to show reactions on comments or not.
            before (str): An Action ID. Only actions that occurred before this action will be returned.
            since (str): An Action ID. Only actions that occurred after this action will be returned.

        Returns:
            dict: The specified card on the board.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/cards/{card_id}"

        query = {
            'key': self.api_key,
            'token': self.token,
            'fields': fields,
            'filter': action_types,
            'format': format,
            'idModels': id_models,
            'limit': limit,
            'member': include_member,
            'member_fields': member_fields,
            'memberCreator': include_member_creator,
            'memberCreator_fields': member_creator_fields,
            'page': page,
            'reactions': include_reactions,
            'before': before,
            'since': since
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_checklist(self, id: str):
        url = f"https://api.trello.com/1/boards/{id}/checklists"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response.json()

    def get_filtered_cards(self, id, filter):
        """
        get filtered cards on a board
        Args:
            id: Boards Id
            filter: (string) Valid Values: all, closed, none, open, visible.

        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}/cards/{filter}"

        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response.json()

    def get_customFields(self, id):
        """
        Get custom Fields from a board
        Args:
            id: id of the board

        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}/customFields"

        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response.json()

    def get_labels(self, id):
        """
        Get labels on board
        Args:
            id: id of board

        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}/labels"


        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response.json()

    def get_lists(self, board_id, filter="all", fields="all", card_filter="all", card_fields="all"):
        """
        Get the lists on a board by its ID.

        Args:
            board_id (str): The ID of the board.
            filter (str, optional): Filter to apply to lists.
                                    Valid values: "all", "closed", "none", "open".
                                    Default: "all".
            fields (str, optional): Specifies the fields to include in the list objects.
                                    Valid values: "all" or a comma-separated list of list fields.
                                    Default: "all".
            card_filter (str, optional): Filter to apply to cards within the lists.
                                         Valid values: "all", "closed", "none", "open".
                                         Default: "all".
            card_fields (str, optional): Specifies the fields to include in the card objects.
                                         Valid values: "all" or a comma-separated list of card fields.
                                         Default: "all".

        Returns:
            dict: The lists on the board.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/boards/{board_id}/lists"

        query = {
            'cards': card_filter,
            'card_fields': card_fields,
            'filter': filter,
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_filtered_lists(self, id, filter):
        """
        Args:
            id: Boards Id
            filter: (string) Valid Values: all, closed, none, open, visible.

        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}/lists/{filter}"

        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response.json()

    def get_members(self, id):
        """
        Get members of a board
        Args:
            id: board_id
        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}/members"


        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response.json()

    def get_enabled_powerUps(self, id):
        """
        Get the enabled Power-Ups on a board
        Args:
            id: id of the board

        Returns:

        """
        url = f"https://api.trello.com/1/boards/{id}/boardPlugins"
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        return response.json()