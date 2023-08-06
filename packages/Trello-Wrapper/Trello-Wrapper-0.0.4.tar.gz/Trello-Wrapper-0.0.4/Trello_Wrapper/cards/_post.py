import abc
import requests
import json


class Post:

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    def create_card(self, name, desc, pos, due, idList, idMembers=None, idLabels=None, urlSource=None, fileSource=None,
                    mimeType=None, idCardSource=None, keepFromSource=None, address=None, locationName=None,
                    coordinates=None):
        """
        Create a new card.

        Args:
            name (str): The name for the card.
            desc (str): The description for the card.
            pos (str or float): The position of the new card. Valid values: "top", "bottom", or a positive float.
            due (str): A due date for the card. Format: date.
            idList (str): The ID of the list the card should be created in.
            idMembers (list of str, optional): Comma-separated list of member IDs to add to the card. Default: None.
            idLabels (list of str, optional): Comma-separated list of label IDs to add to the card. Default: None.
            urlSource (str, optional): A URL starting with http:// or https://. Format: url. Default: None.
            fileSource (str, optional): The file attachment source. Format: binary. Default: None.
            mimeType (str, optional): The mimeType of the attachment. Max length 256. Default: None.
            idCardSource (str, optional): The ID of a card to copy into the new card. Pattern: ^[0-9a-fA-F]{24}$. Default: None.
            keepFromSource (str, optional): If using idCardSource, specify which properties to copy over. Valid values: "all" or comma-separated list of properties. Default: None.
            address (str, optional): For use with/by the Map View. Default: None.
            locationName (str, optional): For use with/by the Map View. Default: None.
            coordinates (str, optional): For use with/by the Map View. Should take the form latitude,longitude. Default: None.

        Returns:
            dict: The newly created card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = "https://api.trello.com/1/cards"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        data = {
            'name': name,
            'desc': desc,
            'pos': pos,
            'due': due,
            'idList': idList,
            'idMembers': idMembers,
            'idLabels': idLabels,
            'urlSource': urlSource,
            'fileSource': fileSource,
            'mimeType': mimeType,
            'idCardSource': idCardSource,
            'keepFromSource': keepFromSource,
            'address': address,
            'locationName': locationName,
            'coordinates': coordinates
        }

        response = requests.post(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def create_card_attachment(self, card_id, name, file=None, mime_type=None, url=None, set_cover=False):
        """
        Create an attachment to a card.

        Args:
            card_id (str): The ID of the card.
            name (str): The name of the attachment. Max length 256.
            file (str, optional): The file to attach, as multipart/form-data.
                                  Format: binary.
                                  Default: None.
            mime_type (str, optional): The mimeType of the attachment. Max length 256.
                                       Default: None.
            url (str, optional): A URL to attach. Must start with http:// or https://.
                                 Default: None.
            set_cover (bool, optional): Determines whether to use the new attachment as a cover for the card.
                                        Default: False.

        Returns:
            dict: The created attachment object.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/attachments"

        query = {
            'name': name,
            'file': file,
            'mimeType': mime_type,
            'url': url,
            'setCover': set_cover,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def create_card_checklist(self, card_id, name, idChecklistSource=None, pos='bottom'):
        """
        Create a new checklist on a card.

        Args:
            card_id (str): The ID of the card.
            name (str): The name of the checklist.
            idChecklistSource (str, optional): The ID of a source checklist to copy into the new one.
                                               Default: None.
            pos (str, optional): The position of the checklist on the card.
                                 Valid values: "top", "bottom", or a positive number.
                                 Default: "bottom".

        Returns:
            dict: The created checklist.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/checklists"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        data = {
            'name': name,
            'idChecklistSource': idChecklistSource,
            'pos': pos
        }

        response = requests.post(url, params=query, json=data)

        if response.status_code != 200:
            raise Exception(response.content)

        return response.json()

    def vote_on_card(self, card_id, member_id):
        """
        Vote on the card for a given member.

        Args:
            card_id (str): The ID of the card.
            member_id (str): The ID of the member to vote 'yes' on the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/membersVoted"

        query = {
            'value': member_id,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def add_comment(self, card_id, comment):
        """
        Add a new comment to a card.

        Args:
            card_id (str): The ID of the card.
            comment (str): The comment text.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"

        query = {
            'text': comment,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def add_label_to_card(self, card_id, label_id):
        """
        Add a label to a card.

        Args:
            card_id (str): The ID of the card.
            label_id (str): The ID of the label to add.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/idLabels"

        query = {
            'value': label_id,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def add_member_to_card(self, card_id, member_id):
        """
        Add a member to a card.

        Args:
            card_id (str): The ID of the card.
            member_id (str): The ID of the member to add.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/idMembers"

        query = {
            'value': member_id,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def create_label_and_add_to_card(self, card_id, color, name=None):
        """
        Create a new label for the board and add it to the given card.

        Args:
            card_id (str): The ID of the card.
            color (str): A valid label color or null.
            name (str, optional): A name for the label.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/labels"

        query = {
            'color': color,
            'name': name,
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)

    def mark_associated_notifications_read(self, card_id):
        """
        Mark notifications about this card as read.

        Args:
            card_id (str): The ID of the card.

        Raises:
            Exception: If the response status code is not 200.
        """

        url = f"https://api.trello.com/1/cards/{card_id}/markAssociatedNotificationsRead"

        query = {
            'key': self.api_key,
            'token': self.token
        }

        response = requests.post(url, params=query)

        if response.status_code != 200:
            raise Exception(response.content)
