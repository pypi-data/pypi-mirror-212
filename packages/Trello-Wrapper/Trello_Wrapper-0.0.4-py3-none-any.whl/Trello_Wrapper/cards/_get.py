import abc
import requests
import json


class Get:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def get_card(self, card_id, fields="all", actions=False, attachments=False, attachment_fields="all", members=False,
                 member_fields="all", members_voted=False, member_voted_fields="all", check_item_states=False,
                 checklists="none", checklist_fields="all", board=False,
                 board_fields="name,desc,descData,closed,idOrganization,pinned,url,prefs", card_list=False,
                 plugin_data=False, stickers=False, sticker_fields="all", custom_field_items=False):
        """
        Get a card by its ID.

        Args:
            card_id (str): The ID of the card.
            fields (str, optional): Specifies the fields to include in the card object.
                                    Valid values: "all", "badges", "checkItemStates", "closed", "dateLastActivity",
                                                  "desc", "descData", "due", "start", "email", "idBoard", "idChecklists",
                                                  "idLabels", "idList", "idMembers", "idShort", "idAttachmentCover",
                                                  "manualCoverAttachment", "labels", "name", "pos", "shortUrl", "url".
                                    Default: "all".
            actions (bool, optional): Whether to return the actions nested resource. Default: False.
            attachments (bool or str, optional): Whether to return attachments. Valid values: True, False, "cover".
                                                 Default: False.
            attachment_fields (str, optional): Specifies the attachment fields to include in the response.
                                               Valid values: "all", "id", "bytes", "date", "edgeColor", "idMember",
                                                             "isUpload", "mimeType", "name", "pos", "previews", "url".
                                               Default: "all".
            members (bool, optional): Whether to return member objects for members on the card. Default: False.
            member_fields (str, optional): Specifies the member fields to include in the response.
                                           Valid values: "all", "avatarHash", "fullName", "initials", "username".
                                           Default: "all".
            members_voted (bool, optional): Whether to return member objects for members who voted on the card. Default: False.
            member_voted_fields (str, optional): Specifies the member fields to include in the response for members who voted.
                                                 Valid values: "all", "avatarHash", "fullName", "initials", "username".
                                                 Default: "all".
            check_item_states (bool, optional): Whether to return checkItemStates. Default: False.
            checklists (str, optional): Whether to return the checklists on the card. Valid values: "all", "none". Default: "none".
            checklist_fields (str, optional): Specifies the checklist fields to include in the response.
                                              Valid values: "all", "idBoard", "idCard", "name", "pos".
                                              Default: "all".
            board (bool, optional): Whether to return the board object the card is on. Default: False.
            board_fields (str, optional): Specifies the board fields to include in the response.
                                          Valid values: "all", "name", "desc", "descData", "closed", "idOrganization",
                                                        "pinned", "url", "prefs".
                                          Default: "name,desc,descData,closed,idOrganization,pinned,url,prefs".
            card_list (bool, optional): Whether to return the list object the card is in. Default: False.
            plugin_data (bool, optional): Whether to include pluginData on the card with the response. Default: False.
            stickers (bool, optional): Whether to include sticker models with the response. Default: False.
            sticker_fields (str, optional): Specifies the sticker fields to include in the response.
                                            Valid values: "all", "id", "idAttachment", "image", "left", "rotate", "top", "zIndex".
                                            Default: "all".
            custom_field_items (bool, optional): Whether to include the customFieldItems. Default: False.

        Returns:
            dict: The card object.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}"

        query = {
            'key': self.api_key,
            'token': self.token,
            'fields': fields,
            'actions': actions,
            'attachments': attachments,
            'attachment_fields': attachment_fields,
            'members': members,
            'member_fields': member_fields,
            'membersVoted': members_voted,
            'memberVoted_fields': member_voted_fields,
            'checkItemStates': check_item_states,
            'checklists': checklists,
            'checklist_fields': checklist_fields,
            'board': board,
            'board_fields': board_fields,
            'list': card_list,
            'pluginData': plugin_data,
            'stickers': stickers,
            'sticker_fields': sticker_fields,
            'customFieldItems': custom_field_items
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_field(self, card_id, field):
        """
        Get a specific property of a card.

        Args:
            card_id (str): The ID of the card.
            field (str): The desired field to retrieve.

        Returns:
            dict: The value of the specified field.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/{field}"

        query = {
            'key': self.api_key,
            'token': self.token,
        }

        response = requests.get(url, params=query)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.content)


    def get_actions(self, card_id, filter_types=None, page=0):
        """
        Get the actions associated with a card by its ID.

        Args:
            card_id (str): The ID of the card.
            filter_types (str, optional): A comma-separated list of action types to filter.
                                          Default: None.
            page (int, optional): The page number of results. Each page has 50 actions.
                                  Default: 0.

        Returns:
            dict: The actions associated with the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/actions"

        query = {
            'filter': filter_types,
            'page': page,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_attachments(self, card_id, fields="all", filter_cover=False):
        """
        Get the attachments associated with a card by its ID.

        Args:
            card_id (str): The ID of the card.
            fields (str, optional): Specifies the fields to include in the attachment object.
                                    Valid values: "all" or a comma-separated list of attachment fields.
                                    Default: "all".
            filter_cover (bool, optional): Use True to restrict the results to just the cover attachment.
                                           Default: False.

        Returns:
            dict: The attachments associated with the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/attachments"

        query = {
            'fields': fields,
            'filter': 'cover' if filter_cover else 'false',
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_card_attachment(self, card_id, attachment_id, fields=None):
        """
        Get a specific attachment on a card.

        Args:
            card_id (str): The ID of the card.
            attachment_id (str): The ID of the attachment.
            fields (list of str, optional): The attachment fields to be included in the response.
                                            Default: None.

        Returns:
            dict: The specific attachment on the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/attachments/{attachment_id}"

        query = {
            'fields': ','.join(fields) if fields else None,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_card_board(self, card_id, fields="all"):
        """
        Get the board a card is on.

        Args:
            card_id (str): The ID of the card.
            fields (str, optional): Specifies the fields to include in the board object.
                                    Valid values: "all" or a comma-separated list of board fields.
                                    Default: "all".

        Returns:
            dict: The board the card is on.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/board"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_completed_checklist_items(self, card_id, fields="all"):
        """
        Get the completed checklist items on a card.

        Args:
            card_id (str): The ID of the card.
            fields (str, optional): Specifies the fields to include in the checkItemStates object.
                                    Valid values: "all" or a comma-separated list of: idCheckItem, state.
                                    Default: "all".

        Returns:
            dict: The completed checklist items on the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/checkItemStates"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_checklists(self, card_id, checkItems="all",
                            checkItem_fields="name,nameData,pos,state,due,dueReminder,idMember",
                            filter="all", fields="all"):
        """
        Get the checklists on a card.

        Args:
            card_id (str): The ID of the card.
            checkItems (str, optional): Specifies whether to include check items or not.
                                        Valid values: "all", "none".
                                        Default: "all".
            checkItem_fields (str, optional): Specifies the check item fields to include in the response.
                                              Valid values: "name", "nameData", "pos", "state", "type", "due",
                                                            "dueReminder", "idMember".
                                              Default: "name,nameData,pos,state,due,dueReminder,idMember".
            filter (str, optional): Specifies whether to include archived checklists or not.
                                    Valid values: "all", "none".
                                    Default: "all".
            fields (str, optional): Specifies the fields to include in the checklist object.
                                    Valid values: "all", "name", "nameData", "pos".
                                    Default: "all".

        Returns:
            list: The checklists on the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/checklists"

        query = {
            'checkItems': checkItems,
            'checkItem_fields': checkItem_fields,
            'filter': filter,
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_card_check_item(self, card_id, check_item_id,
                            fields="name,nameData,pos,state,type,due,dueReminder,idMember"):
        """
        Get a specific checkItem on a card.

        Args:
            card_id (str): The ID of the card.
            check_item_id (str): The ID of the checkItem.
            fields (str, optional): Specifies the checkItem fields to include in the response.
                                    Valid values: "all" or a comma-separated list of: name, nameData, pos,
                                    state, type, due, dueReminder, idMember.
                                    Default: "name,nameData,pos,state,due,dueReminder,idMember".

        Returns:
            dict: The specific checkItem on the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/checkItem/{check_item_id}"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_card_list(self, card_id, fields="all"):
        """
        Get the list a card is in.

        Args:
            card_id (str): The ID of the card.
            fields (str, optional): Specifies the fields to include in the list object.
                                    Valid values: "all", "id", "name", "closed", "pos", "subscribed".
                                    Default: "all".

        Returns:
            dict: The list the card is in.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/list"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_card_members(self, card_id, fields="avatarHash,fullName,initials,username"):
        """
        Get the members on a card.

        Args:
            card_id (str): The ID of the card.
            fields (str, optional): Specifies the fields to include in the member object.
                                    Valid values: "all", "avatarHash", "fullName", "initials", "username".
                                    Default: "avatarHash,fullName,initials,username".

        Returns:
            dict: The members on the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/members"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_card_members_voted(self, card_id, fields="avatarHash,fullName,initials,username"):
        """
        Get the members who have voted on a card.

        Args:
            card_id (str): The ID of the card.
            fields (str, optional): Specifies the fields to include in the member object.
                                    Valid values: "all", "avatarHash", "fullName", "initials", "username".
                                    Default: "avatarHash,fullName,initials,username".

        Returns:
            dict: The members who have voted on the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/membersVoted"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_card_plugin_data(self, card_id):
        """
        Get any shared pluginData on a card.

        Args:
            card_id (str): The ID of the card.

        Returns:
            dict: The pluginData associated with the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/pluginData"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

