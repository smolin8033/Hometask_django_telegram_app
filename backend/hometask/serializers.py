from hometask.models import Hometask
from rest_framework.fields import FileField, ImageField
from rest_framework.serializers import ModelSerializer


class HometaskSerializer(ModelSerializer):
    class Meta:
        model = Hometask
        fields = "__all__"


class HometaskCreateSerializer(ModelSerializer):
    image = ImageField()
    file = FileField()

    class Meta:
        model = Hometask
        fields = (
            "name",
            "start_datetime",
            "end_datetime",
            "coursebook",
            "exercises",
            "url",
            "more_info",
            "image",
            "file",
        )
