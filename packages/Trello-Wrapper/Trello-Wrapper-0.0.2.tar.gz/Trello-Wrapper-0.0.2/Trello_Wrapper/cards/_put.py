import abc
import requests
import json
import re


class Put:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def update_card(self, card_id, name=None, desc=None, closed=None, idMembers=None, idAttachmentCover=None,
                    idList=None,
                    idLabels=None, idBoard=None, pos=None, due=None, start=None, dueComplete=None, subscribed=None,
                    address=None, locationName=None, coordinates=None, cover=None):
        """
        Update a card by its ID.

        Args:
            card_id (str): The ID of the card.
            name (str, optional): The new name for the card.
            desc (str, optional): The new description for the card.
            closed (bool, optional): Whether the card should be archived (closed: True).
            idMembers (str, optional): Comma-separated list of member IDs.
            idAttachmentCover (str, optional): The ID of the image attachment the card should use as its cover,
                                               or None for none.
            idList (str, optional): The ID of the list the card should be in.
            idLabels (str, optional): Comma-separated list of label IDs.
            idBoard (str, optional): The ID of the board the card should be on.
            pos (str or float, optional): The position of the card in its list. Valid values: "top", "bottom",
                                          or a positive float.
            due (str, optional): When the card is due, or None.
            start (str, optional): The start date of the card, or None.
            dueComplete (bool, optional): Whether the due date should be marked complete.
            subscribed (bool, optional): Whether the member should be subscribed to the card.
            address (str, optional): For use with/by the Map View.
            locationName (str, optional): For use with/by the Map View.
            coordinates (str, optional): For use with/by the Map View. Should be in the format "latitude,longitude".
            cover (dict, optional): Updates the card's cover. Valid parameters: "color", "brightness", "url",
                                    "idAttachment", "size".

        Returns:
            dict: The updated card object.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}"

        query = {
            'key': self.api_key,
            'token': self.token,
        }

        data = {
            'name': name,
            'desc': desc,
            'closed': closed,
            'idMembers': idMembers,
            'idAttachmentCover': idAttachmentCover,
            'idList': idList,
            'idLabels': idLabels,
            'idBoard': idBoard,
            'pos': pos,
            'due': due,
            'start': start,
            'dueComplete': dueComplete,
            'subscribed': subscribed,
            'address': address,
            'locationName': locationName,
            'coordinates': coordinates,
            'cover': cover
        }

        response = requests.put(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def update_card_check_item(self, card_id, check_item_id, name=None, state=None, idChecklist=None, pos=None,
                               due=None, dueReminder=None, idMember=None):
        """
        Update an item in a checklist on a card.

        Args:
            card_id (str): The ID of the card.
            check_item_id (str): The ID of the checkItem.
            name (str, optional): The new name for the checklist item.
            state (str, optional): The state of the checklist item. Valid values: "complete", "incomplete".
            idChecklist (str, optional): The ID of the checklist this item is in.
            pos (str or number, optional): The position of the checklist item on the card. Valid values: "top", "bottom", or a positive float.
            due (str, optional): A due date for the checkitem. Format: "YYYY-MM-DD".
            dueReminder (number, optional): A due reminder for the due date on the checkitem.
            idMember (str, optional): The ID of the member to remove from the card.

        Returns:
            dict: The updated checkItem.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/checkItem/{check_item_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        data = {
            'name': name,
            'state': state,
            'idChecklist': idChecklist,
            'pos': pos,
            'due': due,
            'dueReminder': dueReminder,
            'idMember': idMember
        }

        response = requests.put(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def update_checklist_item(self, card_id, checklist_id, checkitem_id, pos=None):
        """
        Update an item in a checklist on a card.

        Args:
            card_id (str): The ID of the card.
            checklist_id (str): The ID of the checklist containing the item.
            checkitem_id (str): The ID of the checklist item to update.
            pos (str or number, optional): The position of the checklist item.
                                           Valid values: "top", "bottom", or a positive float.
                                           Default: None.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/checklist/{checklist_id}/checkItem/{checkitem_id}"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        if pos is not None:
            query['pos'] = pos

        response = requests.put(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)
