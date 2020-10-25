#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import pickle


async def hello(websocket, path):
    names = await websocket.recv()

    #print([name.strip(",").split("|") for name in names])
    DOMMatrix = [element.split("|") for element in "".join(names).split(",")]
    print(DOMMatrix)
    print(len(names))
    with open('DOMMatrix', 'wb') as f:
        # dump information to that file
        pickle.dump(DOMMatrix, f)

    greeting = f"{names}"

    await websocket.send(greeting)
    #print(f"> {greeting}")

start_server = websockets.serve(hello, "localhost", 9998)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
