import json
import os

FILE_NAME = "../data/health_data.json"


def save_health_data(data):

    existing_data = []

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r") as file:

            try:
                existing_data = json.load(file)

            except json.JSONDecodeError:
                existing_data = []

    existing_data.append(data)

    with open(FILE_NAME, "w") as file:
        json.dump(existing_data, file, indent=4)


def load_health_data():

    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as file:

        try:
            return json.load(file)

        except json.JSONDecodeError:
            return []

