# Asyncio websockets in python

Some codes to test the websockets.

* `utils.py` : core code with all the websocket management logic
* `stress_test.py` : code to send 1000 messages / seconds to all the connected clients. Used to test the performances of the network
* `stream_messages.py` : show how to stream messages updated from sync or async code (the state is updated 100 times per second and each time a key is pressed). This example uses curse so it should perturb the display and only work on linux / unix.

## Installation

Only use `python >= 3.6`
`pip install -r requirements.txt`

## Use

### Stress test

`python -m http.serve 9898` (to serve the static files)
`python stress_test.py` and connect your browser to `http://localhost:9898/`


### Stream messages

`python -m http.serve 9898`
`python stream_messages.py` and connect your browser to `http://localhost:9898/`
Press your keyboard to send new messages