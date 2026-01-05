from mojang import API, TooManyRequests, NotFound
import random
import string
import time
import itertools

# all allowed characters in Minecraft username
CHARACTER_POOL = string.ascii_lowercase + string.digits + '_'
COMBO_LEN = 4

GLOBAL_DELAY = 1.0
MAX_DELAY = 60.0

api = API()

def get_uuid_safe(name):
    global GLOBAL_DELAY

    while True:
        try:
            uuid = api.get_uuid(name)
            time.sleep(GLOBAL_DELAY)
            return uuid
        except NotFound:
            time.sleep(GLOBAL_DELAY)
            return None
        except TooManyRequests:
            print(f'Rate Limitied. Sleeping {GLOBAL_DELAY:.2f}s')
            time.sleep(GLOBAL_DELAY)
            GLOBAL_DELAY = min(GLOBAL_DELAY * 2, MAX_DELAY)

def all_usernames():
    for combo in itertools.product(CHARACTER_POOL, repeat=COMBO_LEN):
        yield ''.join(combo)

def create_all_usernames():
    for name in all_usernames():
        uuid = get_uuid_safe(name)
        if uuid:
            print(f'Found Taken Name: {name}')
            continue
        print(f'Found Not Taken Name: {name}')
        with open('not-taken-names.txt', 'a') as file:
            file.write(name + '\n')

def create_random_username(length):
    return ''.join(random.choices(CHARACTER_POOL, k=length))

create_all_usernames()
