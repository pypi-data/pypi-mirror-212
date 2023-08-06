import abc
import requests
import json


class Get:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def get_checklist(self, checklist_id, cards="none", checkItems="all", checkItem_fields="all", fields="all"):
        """
        Get a checklist by its ID.

        Args:
            checklist_id (str): The ID of the checklist.
            cards (str, optional): Valid values: "all", "closed", "none", "open", "visible".
                                   Cards is a nested resource.
                                   Default: "none".
            checkItems (str, optional): The check items on the list to return.
                                        Valid values: "all", "none".
                                        Default: "all".
            checkItem_fields (str, optional): The fields on the checkItem to return if checkItems are being returned.
                                              Valid values: "all" or a comma-separated list of: name, nameData, pos,
                                                            state, type, due, dueReminder, idMember.
                                              Default: "all".
            fields (str, optional): "all" or a comma-separated list of checklist fields.
                                    Default: "all".

        Returns:
            dict: The checklist information.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}"

        query = {
            'cards': cards,
            'checkItems': checkItems,
            'checkItem_fields': checkItem_fields,
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_checklist_field(self, checklist_id, field):
        """
        Get a specific field of a checklist.

        Args:
            checklist_id (str): The ID of the checklist.
            field (str): Field to retrieve. Valid values: "name", "pos".

        Returns:
            dict: The value of the requested field.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}/{field}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_checklist_board(self, checklist_id, fields="all"):
        """
        Get the board associated with a checklist by its ID.

        Args:
            checklist_id (str): The ID of the checklist.
            fields (str, optional): Specifies the fields to include in the board object.
                                    Valid values: "all", "name".
                                    Default: "all".

        Returns:
            dict: The board associated with the checklist.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}/board"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_checklist_cards(self, checklist_id):
        """
        Get the cards associated with a checklist by its ID.

        Args:
            checklist_id (str): The ID of the checklist.

        Returns:
            list: The cards associated with the checklist.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}/cards"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_checklist_checkItems(self, checklist_id, filter="all",
                                 fields="name,nameData,pos,state,due,dueReminder,idMember"):
        """
        Get the check items associated with a checklist by its ID.

        Args:
            checklist_id (str): The ID of the checklist.
            filter (str, optional): Specifies the filter for check items. Valid values: "all", "none".
                                    Default: "all".
            fields (str, optional): Specifies the fields to include in the check item objects.
                                    Valid values: "all", "name", "nameData", "pos", "state", "type", "due",
                                                  "dueReminder", "idMember".
                                    Default: "name,nameData,pos,state,due,dueReminder,idMember".

        Returns:
            list: The check items associated with the checklist.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"

        query = {
            'filter': filter,
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def get_checklist_checkItem(self, checklist_id, checkItem_id,
                                fields="name,nameData,pos,state,due,dueReminder,idMember"):
        """
        Retrieve a specific check item in a checklist.

        Args:
            checklist_id (str): The ID of the checklist.
            checkItem_id (str): The ID of the check item to retrieve.
            fields (str, optional): Specifies the fields to include in the check item object.
                                    Valid values: "all", "name", "nameData", "pos", "state", "type", "due", "dueReminder", "idMember".
                                    Default: "name,nameData,pos,state,due,dueReminder,idMember".

        Returns:
            dict: The retrieved check item.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems/{checkItem_id}"

        query = {
            'fields': fields,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.get(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

