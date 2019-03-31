"""
Code from https://websockets.readthedocs.io/en/stable/intro.html#synchronization-example
Stress test the websocket connection : 1000 msg / s roughtly
"""
import asyncio
import websockets
from utils import STATE, USERS, notify_state, handle_new_connection


async def update_state():
    while True:
        await asyncio.sleep(0.001)
        STATE["value"] += 1
        print(STATE)
        print(USERS)
        await notify_state()


# async def update_state():
#     global OLD_STATE
#     print("update state init")
#     while True:
#         if OLD_STATE != STATE:
#             print("    notified state")
#             OLD_STATE = copy.copy(STATE)
#             await notify_state()
#         await asyncio.sleep(0.01)


# def update_state_not_async(stdscr):
#     while True:
#         key = stdscr.getch()
#         print(key)
#         STATE["value"] += key
#         time.sleep(0.01)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(handle_new_connection, "localhost", 6789)
)
asyncio.ensure_future(update_state())
# future1 = asyncio.get_event_loop().run_in_executor(
#     None, lambda: wrapper(update_state_not_async)
# )
# print("4")
asyncio.get_event_loop().run_forever()
