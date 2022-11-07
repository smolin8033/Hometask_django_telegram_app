from django.db import transaction
from django.db.models import Model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from hometask.models import Hometask, HometaskFile, HometaskImage
from hometask.serializers import (
    HometaskCreateSerializer,
    HometaskFileSerializer,
    HometaskImageSerializer,
    HometaskListSerializer,
)


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
        queryset = Hometask.objects.prefetch_related("images").prefetch_related("files").all()
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hometask_data = serializer.validated_data

        hometask = Hometask.objects.create(**hometask_data)

        self.build_nested_objects(request, hometask.id, images=HometaskImage, files=HometaskFile)

        return Response(hometask_data, status=status.HTTP_201_CREATED)

    def build_nested_objects(self, request, hometask_id, **nested_objects):
        for field_name, model in nested_objects.items():
            field_objects = request.FILES.getlist(field_name)
            if field_objects is None:
                continue

            self.create_objects(hometask_id, model, field_objects)

    @staticmethod
    def create_objects(hometask_id, model: Model, objects) -> list[Model]:
        created_objects = [model(hometask_id=hometask_id, file=obj) for obj in objects]
        model.objects.bulk_create(created_objects)


@extend_schema(tags=["Изображения к домашнему заданию"])
class HometaskImageViewSet(ModelViewSet):
    queryset = HometaskImage.objects.all()
    serializer_class = HometaskImageSerializer
    http_method_names = ["get", "put"]


@extend_schema(tags=["Файлы к домашнему заданию"])
class HometaskFileViewSet(ModelViewSet):
    queryset = HometaskFile.objects.all()
    serializer_class = HometaskFileSerializer
    http_method_names = ["get", "put"]
