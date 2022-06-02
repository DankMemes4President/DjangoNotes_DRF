from django.contrib import admin
from Notes.models import UserProfile, Note, Tag

admin.site.register(UserProfile)
admin.site.register(Note)
admin.site.register(Tag)
