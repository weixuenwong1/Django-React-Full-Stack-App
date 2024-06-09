from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()  # list of all of the different objects when creating a new user to make sure we don't create a user that already exists
    serializer_class = UserSerializer  # tells the view what kind of data that we accept to make a new user
    permission_classes = [AllowAny]  # who can actually call this


class NoteListCreate(generics.ListCreateAPIView):
    """
    List all of the notes that the user has created or it will create a new note
    """
    serializer_class = NoteSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # get the user that is authenticated
        return Note.objects.filter(author=user)  # or Note.objects.all() to display all notes
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user 
        return Note.objects.filter(author=user)