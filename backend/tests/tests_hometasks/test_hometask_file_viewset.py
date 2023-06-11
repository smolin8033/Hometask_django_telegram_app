import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from hometask.models import HometaskFile
from tests.tests_hometasks.faked_data.factories import HometaskFactory
from tests.tests_hometasks.faked_data.fake_files import generate_temp_file

pytestmark = pytest.mark.django_db


class TestHometaskFileViewSet:
    def test_action_update(self, api_client: APIClient) -> None:
        hometask = HometaskFactory()
        file = hometask.files.first()
        temp_file = generate_temp_file()

        assert HometaskFile.objects.count() == 1

        second_hometask = HometaskFactory()

        data = {
            "hometask": second_hometask.pk,
            "file": temp_file,
        }

        url = reverse("files-detail", kwargs={"pk": file.pk})

        response = api_client.put(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        file = HometaskFile.objects.get(id=file.pk)

        assert file.hometask_id == second_hometask.id
        assert file.file == temp_file
