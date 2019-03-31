"""
Code from https://websockets.readthedocs.io/en/stable/intro.html#synchronization-example

Illustrate different ways to update a shared state from
    async (update_state_async) or
    sync (update_state_not_async, run in an executor)
functions
"""
import asyncio
import copy
import time

import websockets
from utils import STATE, USERS, notify_state, handle_new_connection
from curses import wrapper  # ncurse configuration stuff

OLD_STATE = copy.deepcopy(STATE)


async def send_state_if_updated():
    global OLD_STATE
    print("update state init")
    while True:
        if OLD_STATE != STATE:
            print("    notified state")
            OLD_STATE = copy.deepcopy(STATE)
            await notify_state()
        await asyncio.sleep(0.01)


def update_state_not_async(stdscr):
    while True:
        key = stdscr.getch()
        print(key)
        STATE["value"] += key
        time.sleep(0.01)


async def update_state_async():
    while True:
        await asyncio.sleep(0.1)
        STATE["value"] += 1
        print(STATE)
        print(USERS)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(handle_new_connection, "localhost", 6789)
)
asyncio.ensure_future(update_state_async())
asyncio.ensure_future(send_state_if_updated())
asyncio.get_event_loop().run_in_executor(None, lambda: wrapper(update_state_not_async))
asyncio.get_event_loop().run_forever()
