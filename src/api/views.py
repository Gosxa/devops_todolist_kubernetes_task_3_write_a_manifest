from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from api.serializers import TodoListSerializer, TodoSerializer, UserSerializer
from lists.models import Todo, TodoList


from flask import Flask, Response, send_file
from django.http import HttpResponse
from django.utils import timezone
import time

app = Flask(__name__)

start_time = time.time()
# Define the startup period (in seconds)
startup_period = 10

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `creator` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # If the object doesn't have a creator (i.e. anon) allow all methods.
        if not obj.creator:
            return True

        # Instance must have an attribute named `creator`.
        return obj.creator == request.user


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class TodoListViewSet(viewsets.ModelViewSet):

    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)

class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)

@app.route('/health')
def health_check():
   return Response("Healthy", status=200)

@app.route('/ready')
def readiness_check():
   # You can add logic here to determine if the app is ready. For simplicity, we'll just return 200.
   if time.time() < start_time + startup_period:
       # Application is not ready, return a non-200 status code
       return Response("Not Ready", status=503)
   else:
       # Application is ready, return 200
       return Response("Ready", status=200)