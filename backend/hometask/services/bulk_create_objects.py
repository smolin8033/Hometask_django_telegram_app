from django.db.models import Model


def bulk_create_nested_objects(hometask_id, model: Model, objects) -> list[Model]:
    created_objects = [model(hometask_id=hometask_id, file=obj) for obj in objects]
    return model.objects.bulk_create(created_objects)
