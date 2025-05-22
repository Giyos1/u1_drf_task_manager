from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.serializers import UserSerializer
from task_manager.models import Project, Task


# custom serializers
class ProjectSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    updated_at = serializers.DateTimeField(read_only=True)
    total_task = serializers.IntegerField()

    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError("uchta harfdan katta")
        return value

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        Project.objects.filter(id=instance.id).update(**validated_data)
        return instance

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        if self.instance:
            self.instance = self.update(self.instance, validated_data)
        else:
            self.instance = self.create(validated_data)
        print(self.instance)
        return self.instance


# class ProjectDetailSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=255)
#     description = serializers.CharField()
#     updated_at = serializers.DateTimeField(read_only=True)
#     owner = serializers.IntegerField()
#     members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


# model serializer

class ProjectDetailModelSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    members = UserSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectCreateAndUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class ProjectListSerializers(serializers.ModelSerializer):
    total_task = serializers.IntegerField()

    class Meta:
        model = Project
        fields = ["id", "name", 'description', 'created_at', 'owner', 'members', 'total_task']


class ProjectDetailSerializers(serializers.ModelSerializer):
    owner = UserSerializer()
    members = UserSerializer(many=True)
    total_task = serializers.IntegerField()

    class Meta:
        model = Project
        fields = ["id", "name", 'description', 'created_at', 'owner', 'members', 'total_task']


class ProjectCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'members']


class ProjectUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'members']


class ProjectAddMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['members']
