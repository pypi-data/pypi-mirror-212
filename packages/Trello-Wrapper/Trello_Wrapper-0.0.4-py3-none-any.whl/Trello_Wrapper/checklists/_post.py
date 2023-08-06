import abc
import requests
import json


class Post:
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def create_checklist(self, id_card, name, pos=None, id_checklist_source=None):
        """
        Create a checklist and add it to a card.

        Args:
            id_card (str): The ID of the card to which the checklist should be added.
            name (str): The name of the checklist.
            pos (str or int, optional): The position of the checklist on the card.
                                        Valid values: "top", "bottom", or a positive number.
            id_checklist_source (str, optional): The ID of a checklist to copy into the new checklist.

        Returns:
            dict: The created checklist.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = "https://api.trello.com/1/checklists"

        query = {
            'idCard': id_card,
            'name': name,
            'pos': pos,
            'idChecklistSource': id_checklist_source,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def create_checklist_checkItem(self, checklist_id, name, pos=None, checked=False, due=None, dueReminder=None,
                                   idMember=None):
        """
        Create a new check item in a checklist.

        Args:
            checklist_id (str): The ID of the checklist.
            name (str): The name of the new check item on the checklist.
                         Should be a string of length 1 to 16384.
            pos (str or int, optional): The position of the check item in the checklist.
                                        One of: "top", "bottom", or a positive number.
            checked (bool, optional): Determines whether the check item is already checked when created.
                                      Default: False.
            due (str, optional): A due date for the check item.
                                 Format: date.
            dueReminder (int, optional): A due reminder for the due date on the check item.
            idMember (str, optional): An ID of a member resource.

        Returns:
            dict: The created check item.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        data = {
            'name': name,
            'pos': pos,
            'checked': checked,
            'due': due,
            'dueReminder': dueReminder,
            'idMember': idMember
        }

        response = requests.post(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()
