from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class EchoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()     # accept connection
        
    async def disconnect(self, close_code):
        pass # handle disconnection
    
    async def receive(self, text_data):
        # when a message is received, send back an ehco
        await self.send(text_data=f"You said: {text_data}")