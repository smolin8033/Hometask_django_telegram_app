from hometask.models import Hometask, HometaskImage
from rest_framework.serializers import FileField, ImageField, ModelSerializer


class HometaskSerializer(ModelSerializer):
    class Meta:
        model = Hometask
        fields = "__all__"


class HometaskCreateSerializer(ModelSerializer):
    # images = ImageField(required=False)
    images = ImageField(required=False)
    files = FileField(required=False)

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
            "images",
            "files",
        )
