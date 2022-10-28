from django.db import transaction
from drf_spectacular.utils import extend_schema
from hometask.models import Hometask, HometaskImage
from hometask.serializers import HometaskCreateSerializer, HometaskSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


@extend_schema(tags=["Домашнее задание"])
class HometaskViewSet(ModelViewSet):

    queryset = Hometask.objects.all()
    serializer_class = HometaskSerializer

    def get_serializer_class(self):
        serializer_class = HometaskSerializer
        if self.action == self.create.__name__:
            serializer_class = HometaskCreateSerializer
        return serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hometask_data = serializer.validated_data
        images_data = None
        files_data = None

        if "images" in hometask_data.keys():
            images_data = hometask_data.pop("images")

        if "files" in hometask_data.keys():
            files_data = hometask_data.pop("files")

        hometask = Hometask.objects.create(**hometask_data)

        if images_data:
            self.create_images(hometask, images_data)

        if files_data:
            self.create_files(hometask, files_data)

        return Response(hometask_data, status=status.HTTP_201_CREATED)

    @staticmethod
    def create_images(hometask, images_data):
        print(images_data)
        print("\n\n\n\n")
        print(i for i in images_data)
        print("\n\n\n\n")
        images = []
        for image in images_data:
            images.append(HometaskImage(hometask=hometask, image=image))
        return HometaskImage.objects.bulk_create(images)

    def create_files(self, hometask, files_data):
        pass
