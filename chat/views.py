from django.shortcuts import render

def echo_view(request):
    return render(request, "chat/echo.html")
