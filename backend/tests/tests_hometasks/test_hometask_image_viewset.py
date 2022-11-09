import pytest
from django.urls import reverse
from rest_framework import status

from hometask.models import HometaskImage
from tests.tests_hometasks.faked_data.factories import HometaskFactory
from tests.tests_hometasks.faked_data.fake_files import generate_temp_image


class TestHometaskImageViewSet:
    @pytest.mark.django_db
    def test_action_update(self, api_client):
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
        json_response = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert json_response["hometask"] != hometask.id
        assert json_response["hometask"] == second_hometask.id
        assert json_response["file"] != image.file
