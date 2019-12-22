from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response



from Wall.models import Wall
from .serializers import WallSerializer ,UserSerializer


class WallViewSet(viewsets.ModelViewSet):
    queryset = Wall.objects.all()
    serializer_class = WallSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
