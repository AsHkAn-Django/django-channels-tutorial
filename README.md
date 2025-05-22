# DJango CHannels Tutorial

Just a quick little project I made while practicing Django and backend development.  
This is part of my journey as I learn and improve my skills.

## About the Project

myproject/
├── chat/
│   ├── templates/
│   │   └── chat/echo.html
│   ├── consumers.py
│   ├── routing.py
│   ├── views.py
│   └── urls.py
├── myproject/
│   ├── asgi.py
│   ├── settings.py
│   └── urls.py
└── manage.py

This project is built using Django and includes basic frontend styling with HTML, CSS, Bootstrap, and some JavaScript.  
I usually focus on the backend side of things and try to keep things simple and clean.  
Each project I make is a way for me to learn something new or reinforce what I already know.


## Technologies Used

- Python
- Django
- HTML
- CSS
- Bootstrap
- JavaScript

## About Me

Hi, I'm Ashkan — a junior Django developer who recently transitioned from teaching English as a second language to learning backend development.  
I’m currently focused on improving my skills, building projects, and looking for opportunities to work as a backend developer.  
You can find more of my work here: [My GitHub](https://github.com/AsHkAn-Django)

## How to Use

1. Clone the repository  
   `git clone https://github.com/AsHkAn-Django/django-channels-tutorial.git`
2. Navigate into the folder  
   `cd django-channels-tutorial`
3. Create a virtual environment and activate it
4. Install the dependencies  
   `pip install -r requirements.txt`
5. Run the server  
   `python manage.py runserver`

## Tutorial 

1. create django project and app
```bash
pip install django
django-admin startproject myproject
cd myproject
python manage.py startapp chat
```

2. install django channels
```bash
pip install channels
```

3. Update settings.py
```python
INSTALLED_APPS = [
    ...
    "channels",
    "chat",  # your app
]

ASGI_APPLICATION = "myproject.asgi.application"
```

4. Update asgi.py
```python
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
```

5. Create WebSocket Routing
```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/echo/$", consumers.EchoConsumer.as_asgi()),
]
```

6. Create the WebSocket Consumer
```python
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=f"You said: {text_data}")
```

7. Create a Frontend Template
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Echo</title>
</head>
<body>
    <h1>Echo Test</h1>
    <input id="messageInput" type="text" placeholder="Type something..." />
    <button onclick="sendMessage()">Send</button>
    <ul id="messages"></ul>

    <script>
        const socket = new WebSocket("ws://localhost:8000/ws/echo/");

        socket.onmessage = function(event) {
            const li = document.createElement("li");
            li.textContent = event.data;
            document.getElementById("messages").appendChild(li);
        };

        function sendMessage() {
            const input = document.getElementById("messageInput");
            socket.send(input.value);
            input.value = "";
        }
    </script>
</body>
</html>
```

8. Add django view
```python
from django.shortcuts import render

def echo_view(request):
    return render(request, "chat/echo.html")
```

9. Add url
```python
from django.urls import path
from .views import echo_view

urlpatterns = [
    path("echo/", echo_view),
]
```
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("chat.urls")),
    path("admin/", admin.site.urls),
]
```

10. install and run Daphne (ASGI server)
```bash
pip install daphne
```
```bash
daphne myproject.asgi:application
```

### If you want to add the model to store Messages
1. Create the Model
```python
from django.db import models

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
```

2. Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Update Your Consumer to Save and Load Messages
```python
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from asgiref.sync import sync_to_async
import json

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Load last 10 messages from DB
        messages = await sync_to_async(list)(Message.objects.order_by("-timestamp")[:10])
        for message in reversed(messages):
            await self.send(text_data=message.content)

    async def receive(self, text_data):
        # Save new message
        await sync_to_async(Message.objects.create)(content=text_data)

        # Echo the message back
        await self.send(text_data=f"You said: {text_data}")
```

