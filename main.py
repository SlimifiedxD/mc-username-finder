import itertools
import random
import string
import time
from typing import List

import requests
from requests import RequestException

# all allowed characters in Minecraft username
CHARACTER_POOL = string.ascii_lowercase + string.digits + "_"
COMBO_LEN = 4


class MojangAPIError(Exception):
    pass


def make_api_request(initial_names: List[str]) -> List[str]:
    if len(initial_names) > 10:
        raise Exception("List is too large")
    try:
        response = requests.post(
            "https://api.mojang.com/profiles/minecraft",
            json=initial_names,
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            print(f"Error response: {response.text}")
            return []
        data = response.json()
        if isinstance(data, dict) and "error" in data:
            raise MojangAPIError(data.get("errorMessage"))
        if isinstance(data, str):
            raise MojangAPIError(f"API error returned string: {data}")
        if not isinstance(data, list):
            raise MojangAPIError(f"Unexpected response type: {type(data)}")

        initial_set = {name.lower() for name in initial_names}
        api_names = {item["name"].lower() for item in data}
        return list(initial_set - api_names)

    except MojangAPIError as e:
        print(f"Mojang rejected request: {e}")
        return []

    except RequestException as e:
        print(f"HTTP/Network Error: {e}")
        return []


def all_usernames():
    for combo in itertools.product(CHARACTER_POOL, repeat=COMBO_LEN):
        yield "".join(combo)


def create_all_usernames():
    names = list(all_usernames())
    random.shuffle(names)
    segment_lists = [names[i : i + 10] for i in range(0, len(names), 10)]
    for l in segment_lists:
        not_taken_names = make_api_request(l)
        for name in not_taken_names:
            print(f"Found Name: {name}")
            with open("names.txt", "a") as file:
                file.write(name + "\n")
        time.sleep(1)


def create_random_username(length):
    return "".join(random.choices(CHARACTER_POOL, k=length))


create_all_usernames()
