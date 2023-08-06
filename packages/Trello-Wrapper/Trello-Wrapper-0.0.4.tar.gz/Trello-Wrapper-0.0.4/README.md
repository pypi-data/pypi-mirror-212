# TRELLO-WRAPPER


[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org/)

A Wrapper around the Trello API

## Installation
    pip install Trello-Wrapper

## Usage
1. Obtain your Trello API key and token by following the instructions on the Trello Developer site: https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/

2. Import the Trello-Wrapper class and create an instance with your API key and token:
    

    from Trello_Wrapper import Trello
    trello = Trello(api_key=YOUR_API_KEY, token=YOUR_TOKEN)


3. Use the available methods to interact with Trello resources. For example, to get all boards:
    

    boards = trello.Boards()
    print(boards.get_all_boards()) 


Refer to the documentation within the Trello_Wrapper class for more available methods and their usage.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


## Authors
Tsilavo Tahina R.

[Mail](https://github.com/Rtsil)


[Github](https://github.com/Rtsil)


