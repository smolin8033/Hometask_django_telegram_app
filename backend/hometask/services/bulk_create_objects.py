from typing import Type

from hometask.models import HometaskFile, HometaskImage


def bulk_create_nested_objects(
    hometask_id: int, model: Type[HometaskImage] | Type[HometaskFile], objects: list
) -> list:
    created_objects: list[HometaskImage | HometaskFile] = [model(hometask_id=hometask_id, file=obj) for obj in objects]
    return model.objects.bulk_create(created_objects)
