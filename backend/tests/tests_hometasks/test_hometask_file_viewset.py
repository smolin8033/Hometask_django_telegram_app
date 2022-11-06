import pytest
from django.urls import reverse
from rest_framework import status
from tests.tests_hometasks.faked_data.factories import HometaskFactory
from tests.tests_hometasks.faked_data.fake_files import generate_temp_file

from hometask.models import HometaskFile


class TestHometaskFileViewSet:
    @pytest.mark.django_db
    def test_action_update(self, api_client):
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
        json_response = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert json_response["hometask"] != hometask.id
        assert json_response["hometask"] == second_hometask.id
        assert json_response["file"] != file.file
