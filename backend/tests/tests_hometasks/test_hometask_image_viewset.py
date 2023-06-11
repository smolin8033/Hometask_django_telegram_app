import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from hometask.models import HometaskImage
from tests.tests_hometasks.faked_data.factories import HometaskFactory
from tests.tests_hometasks.faked_data.fake_files import generate_temp_image

pytestmark = pytest.mark.django_db


class TestHometaskImageViewSet:
    def test_action_update(self, api_client: APIClient) -> None:
        hometask = HometaskFactory()
        image = hometask.images.first()
        temp_image = generate_temp_image()

        assert HometaskImage.objects.count() == 1

        second_hometask = HometaskFactory()

        data = {
            "hometask": second_hometask.pk,
            "file": temp_image,
        }

        url = reverse("images-detail", kwargs={"pk": image.pk})

        response = api_client.put(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        image = HometaskImage.objects.get(id=image.pk)

        assert image.hometask_id == second_hometask.id
        assert image.file == temp_image
