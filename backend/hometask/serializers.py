from hometask.models import Hometask, HometaskFile, HometaskImage
from rest_framework.serializers import FileField, ImageField, ModelSerializer


class HometaskImageSerializer(ModelSerializer):
    """
    Сериализатор изображений к домашнему заданию
    """

    class Meta:
        model = HometaskImage
        fields = ("hometask", "image")


class HometaskFileSerializer(ModelSerializer):
    """
    Сериализатор файлов к домашнему заданию
    """

    class Meta:
        model = HometaskFile
        fields = ("hometask", "file")


class HometaskListSerializer(ModelSerializer):
    """
    Сериализатор списка домашних заданий
    """

    images = HometaskImageSerializer(read_only=True, many=True)
    files = HometaskFileSerializer(read_only=True, many=True)

    class Meta:
        model = Hometask
        fields = (
            "id",
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


class HometaskCreateSerializer(ModelSerializer):
    """
    Сериализатор создания домашнего задания
    """

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
