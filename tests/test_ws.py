import asyncio
import json
import websockets

async def test_ws():
    uri = "ws://127.0.0.1:8000/ws/ide"
    async with websockets.connect(uri) as ws:
        # Wait for handshake
        greeting = await ws.recv()
        data = json.loads(greeting)
        print("WS GREETING:", data)
        assert data.get("type") == "HANDSHAKE_ACK"

        # Send ping
        await ws.send(json.dumps({"type": "PING"}))
        pong = await ws.recv()
        pong_data = json.loads(pong)
        print("WS PONG:", pong_data)
        assert pong_data.get("type") == "PONG"

        print("WebSocket Bridge test PASSED!")

if __name__ == "__main__":
    asyncio.run(test_ws())
