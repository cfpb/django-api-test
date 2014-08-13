from django.http import HttpResponse as Response
from django.contrib.auth.models import User
import json

def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        return Response(json.dumps([{'username': user.username} for user in users]))

    elif request.method == 'POST':
        user = User.objects.create(username='user1')
        return Response(json.dumps({'username': user.username}))