from django.db import transaction
from drf_spectacular.utils import extend_schema
from hometask.models import Hometask, HometaskFile, HometaskImage
from hometask.serializers import HometaskCreateSerializer, HometaskListSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


@extend_schema(tags=["Домашнее задание"])
class HometaskViewSet(ModelViewSet):
    """
    Домашние задания
    """

    def get_serializer_class(self):
        serializer_class = HometaskListSerializer
        if self.action == self.create.__name__:
            serializer_class = HometaskCreateSerializer
        return serializer_class

    def get_queryset(self):
        queryset = (
            Hometask.objects.prefetch_related("images").prefetch_related("files").all()
        )
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hometask_data = serializer.validated_data
        images_data = None
        files_data = None
        images_retrieved = None
        files_retrieved = None

        if "images" in hometask_data.keys():
            images_data = hometask_data.pop("images")
            images_retrieved = request.FILES.getlist("images")

        if "files" in hometask_data.keys():
            files_data = hometask_data.pop("files")
            files_retrieved = request.FILES.getlist("files")

        hometask = Hometask.objects.create(**hometask_data)

        if images_data:
            self.create_images(hometask, images_retrieved)

        if files_data:
            self.create_files(hometask, files_retrieved)

        return Response(hometask_data, status=status.HTTP_201_CREATED)

    @staticmethod
    def create_images(hometask, images_retrieved):
        images = []
        for image in images_retrieved:
            images.append(HometaskImage(hometask=hometask, image=image))
        return HometaskImage.objects.bulk_create(images)

    @staticmethod
    def create_files(hometask, files_retrieved):
        files = []
        for file in files_retrieved:
            files.append(HometaskFile(hometask=hometask, file=file))
        return HometaskFile.objects.bulk_create(files)
