import abc
import requests
import json


class Get:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def get_action(self, action_id, display=True, entities=False, fields='all', member=True,
                   member_fields='avatarHash,fullName,initials,username', member_creator=True,
                   member_creator_fields='avatarHash,fullName,initials,username'):
        """
        Get an action by its ID.

        Args:
            action_id (str): The ID of the action to retrieve.
            display (bool, optional): Determines whether to include display information. Default is True.
            entities (bool, optional): Determines whether to include entity information. Default is False.
            fields (str, optional): Specifies the action fields to include. Default is 'all'.
            member (bool, optional): Determines whether to include the member information. Default is True.
            member_fields (str, optional): Specifies the member fields to include. Default is
                                           'avatarHash,fullName,initials,username'.
            member_creator (bool, optional): Determines whether to include the member creator information.
                                             Default is True.
            member_creator_fields (str, optional): Specifies the member creator fields to include. Default is
                                                   'avatarHash,fullName,initials,username'.

        Returns:
            dict: The action object.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}"

        query = {
            'display': display,
            'entities': entities,
            'fields': fields,
            'member': member,
            'member_fields': member_fields,
            'memberCreator': member_creator,
            'memberCreator_fields': member_creator_fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_property(self, action_id, field):
        """
        Get a specific property of an action by its ID.

        Args:
            action_id (str): The ID of the action.
            field (str): The specific action field to retrieve.

        Returns:
            any: The value of the requested action field.

        Raises:
            ValueError: If the field parameter is not one of the valid values.
            Exception: If the response status code is not 200.
        """

        valid_fields = ["id", "idMemberCreator", "data", "type", "date", "limits", "display", "memberCreator"]
        if field not in valid_fields:
            raise ValueError(f"Invalid field. Valid values are: {', '.join(valid_fields)}")

        url = f"https://api.trello.com/1/actions/{action_id}/{field}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_board(self, action_id, fields="all"):
        """
        Get the board associated with an action by its ID.

        Args:
            action_id (str): The ID of the action.
            fields (str, optional): Specifies the fields to include in the board object.
                                    Valid values: "all", "id", "name", "desc", "descData", "closed", "idMemberCreator",
                                                  "idOrganization", "pinned", "url", "shortUrl", "prefs", "labelNames",
                                                  "starred", "limits", "memberships", "enterpriseOwned".
                                    Default: "all".

        Returns:
            dict: The board associated with the action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/board"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_card(self, action_id, fields="all"):
        """
        Get the card associated with an action by its ID.

        Args:
            action_id (str): The ID of the action.
            fields (str, optional): Specifies the fields to include in the card object.
                                    Valid values: "all", "id", "address", "badges", "checkItemStates", "closed",
                                                  "coordinates", "creationMethod", "dueComplete", "dateLastActivity",
                                                  "desc", "descData", "due", "dueReminder", "email", "idBoard",
                                                  "idChecklists", "idLabels", "idList", "idMembers", "idMembersVoted",
                                                  "idShort", "idAttachmentCover", "labels", "limits", "locationName",
                                                  "manualCoverAttachment", "name", "pos", "shortLink", "shortUrl",
                                                  "subscribed", "url", "cover", "isTemplate".
                                    Default: "all".

        Returns:
            dict: The card associated with the action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/card"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_list(self, action_id, fields="id"):
        """
        Get the list associated with an action by its ID.

        Args:
            action_id (str): The ID of the action.
            fields (str, optional): Specifies the fields to include in the list object.
                                    Valid values: "id".
                                    Default: "id".

        Returns:
            dict: The list associated with the action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/list"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_member(self, action_id, fields="all"):
        """
        Get the member associated with an action by its ID.

        Args:
            action_id (str): The ID of the action.
            fields (str, optional): Specifies the fields to include in the member object.
                                    Valid values: "all" or a comma-separated list of member fields.
                                    Default: "all".

        Returns:
            dict: The member associated with the action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/member"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_member_creator(self, action_id, fields="all"):
        """
        Get the member who created the action by its ID.

        Args:
            action_id (str): The ID of the action.
            fields (str, optional): Specifies the fields to include in the member object.
                                    Valid values: "all" or a comma-separated list of member fields.
                                    Default: "all".

        Returns:
            dict: The member who created the action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/memberCreator"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_organization(self, action_id, fields="all"):
        """
        Get the organization of the action by its ID.

        Args:
            action_id (str): The ID of the action.
            fields (str, optional): Specifies the fields to include in the organization object.
                                    Valid values: "all" or a comma-separated list of organization fields.
                                    Default: "all".

        Returns:
            dict: The organization of the action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/organization"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_reactions_summary(self, action_id):
        """
        Get a summary of all reactions for an action.

        Args:
            action_id (str): The ID of the action.

        Returns:
            dict: The summary of reactions for the action.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/actions/{action_id}/reactionsSummary"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()



