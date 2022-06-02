from django.contrib.auth.models import User
from rest_framework import serializers
from Notes.models import Note, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        user = User.objects.create(
            username=validate_data['username'],
        )
        user.set_password(validate_data['password'])
        user.save()
        return user


class NoteSerializer(serializers.ModelSerializer):
    #tag = serializers.CharField(max_length=500, write_only=True)

    class Meta:
        model = Note
        read_only_fields = ('id',)
        fields = ['id', 'title', 'content', 'tag_string']

    def create(self, validated_data):
        user = self.context['request'].user.userprofile
        note = Note.objects.create(title=validated_data['title'],
                                   content=validated_data['content'],
                                   user=user,
                                   tag_string=validated_data['tag_string'],
                                   )
        tags = list(self.validated_data['tag_string'].split(','))
        for tag in tags:
            Tag.objects.create(title=tag, note=note)
        return note

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.tag_string = validated_data.get('tag_string', instance.tag_string)
        instance.tag_set.all().delete()
        tags = list(self.validated_data['tag_string'].split(','))
        for tag in tags:
            Tag.objects.create(title=tag, note=instance)
        instance.save()
        return instance

