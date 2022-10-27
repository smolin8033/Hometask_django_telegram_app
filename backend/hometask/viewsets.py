from drf_spectacular.utils import extend_schema
from hometask.models import Hometask
from hometask.serializers import HometaskCreateSerializer, HometaskSerializer
from rest_framework.viewsets import ModelViewSet


@extend_schema(tags=["Домашнее задание"])
class HometaskViewSet(ModelViewSet):

    queryset = Hometask.objects.all()
    serializer_class = HometaskSerializer

    def get_serializer_class(self):
        if self.action == "create":
            serializer_class = HometaskCreateSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        print(serializer.initial_data)
        print("\n")
        print(serializer.is_valid(raise_exception=True))
        print("\n")
        print(serializer)
        print("\n")
        print(serializer.data)
        print("\n")
