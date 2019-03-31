#!/usr/bin/env python

# WS server example that synchronizes state across clients
from utils import

STATE = {"value": 0}
USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


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


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    print("toto")
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)


print("1")
asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, "localhost", 6789)
)
print("2")
asyncio.ensure_future(update_state())
print("3")
# future1 = asyncio.get_event_loop().run_in_executor(
#     None, lambda: wrapper(update_state_not_async)
# )
# print("4")
asyncio.get_event_loop().run_forever()
print("5")
