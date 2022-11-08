from hometask.services.bulk_create_objects import bulk_create_objects


def build_nested_objects(request, hometask_id, **nested_objects):
    for field_name, model in nested_objects.items():
        field_objects = request.FILES.getlist(field_name)
        if field_objects is None:
            continue

        bulk_create_objects(hometask_id, model, field_objects)
