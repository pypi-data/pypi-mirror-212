test_data = [{"id": "64787fb7e7d51043aea35ce3",
        "nodeId": "ari:cloud:trello::board/workspace/64787faddd0cabbb20be7eab/64787fb7e7d51043aea35ce3",
        "name": "test",}, {"id": "64787fb7e7d51043aea35ce3",
        "nodeId": "ari:cloud:trello::board/workspace/64787faddd0cabbb20be7eab/64787fb7e7d51043aea35ce3",
        "name": "test2",}, {"id": "64787fb7e7d51043aea35ce3",
        "nodeId": "ari:cloud:trello::board/workspace/64787faddd0cabbb20be7eab/64787fb7e7d51043aea35ce3",
        "name": "test3",}]

print({board["name"]: board["id"] for board in test_data})