from typing import Type

from django.db import transaction
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from hometask.models import Hometask, HometaskFile, HometaskImage
from hometask.serializers import (
    HometaskCreateSerializer,
    HometaskFileSerializer,
    HometaskImageSerializer,
    HometaskListSerializer,
)
from hometask.services.get_nested_objects import get_nested_objects


@extend_schema(tags=["Домашнее задание"])
class HometaskViewSet(ModelViewSet):
    """
    Домашние задания
    """

    def get_serializer_class(self) -> Type[HometaskCreateSerializer | HometaskListSerializer]:
        serializer_class = HometaskListSerializer
        if self.action == self.create.__name__:
            serializer_class = HometaskCreateSerializer
        return serializer_class

    def get_queryset(self) -> QuerySet:
        queryset = Hometask.objects.prefetch_related("images").prefetch_related("files").all()
        return queryset

    @transaction.atomic
    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hometask_data = serializer.validated_data

        hometask = Hometask.objects.create(**hometask_data)

        get_nested_objects(request, hometask.id, images=HometaskImage, files=HometaskFile)

        return Response(hometask_data, status=status.HTTP_201_CREATED)


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
