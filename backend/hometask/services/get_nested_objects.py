from typing import Type

from rest_framework.request import Request

from hometask.models import HometaskFile, HometaskImage
from hometask.services.bulk_create_objects import bulk_create_nested_objects


def get_nested_objects(
    request: Request, hometask_id: int, **nested_objects: Type[HometaskImage] | Type[HometaskFile]
) -> None:
    for field_name, model in nested_objects.items():
        field_objects = request.FILES.getlist(field_name)
        if field_objects is None:
            continue

        bulk_create_nested_objects(hometask_id, model, field_objects)
