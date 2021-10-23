import websocket
import json
import threading
import time
import asyncio
import os

class DiscordWebSocket:
    def __init__(self, token: str):
        self.token: str = token.strip()
        self.url: str = "wss://gateway.discord.gg/?v9&encoding=json"
        self.ws = websocket.WebSocket()

    def send_json_request(self, ws, request):
        ws.send(json.dumps(request))

    def recieve_json_response(self, ws):
        response = ws.recv()
        if response:
            return json.loads(response)

    def heartbeat(self, interval, ws):
        while True:
            asyncio.run(asyncio.sleep(interval))
            heartbeatJSON = {
                "op": 1,
                "d": "null"
            }
            self.send_json_request(ws, heartbeatJSON)

    async def connect(self):
        self.ws.connect(self.url)
        event = self.recieve_json_response(self.ws)
        heartbeat_interval = event['d']['heartbeat_interval'] / 1000
        threading._start_new_thread(self.heartbeat, (heartbeat_interval, self.ws))
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {}
            }
        }
        self.send_json_request(self.ws, payload)

    def event(self):
        while True:
            event = self.recieve_json_response(self.ws)

            if event['t'] != None:

                try:
                    print(f'{event}')

                except:
                    pass