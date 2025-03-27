from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from task_manager.models import Project


# custom serializers
class ProjectSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    updated_at = serializers.DateTimeField(read_only=True)

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
        return self.instance


class ProjectModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["updated_at"]
        extra_kwargs = {
            "name": {"validators": []},
            "description": {"validators": []},
        }

    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError("uchta harfdan katta")
        return value
