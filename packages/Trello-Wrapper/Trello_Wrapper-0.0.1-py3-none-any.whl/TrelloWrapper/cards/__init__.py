import requests

from ._get import Get
from ._post import Post
from ._put import Put
from ._delete import Delete


class Cards(Get, Post, Put, Delete):
    def __init__(self, api_key, token):
        self.api_key = api_key
        self.token = token

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
