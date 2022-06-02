from django.db import models

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Note(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_notes_by_user(self):
        return self.user.note_set.all()


class Tag(models.Model):
    title = models.CharField(max_length=100)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

