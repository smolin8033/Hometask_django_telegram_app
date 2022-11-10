import pytest
from django.urls import reverse
from rest_framework import status

from hometask.models import Hometask, HometaskFile, HometaskImage
from tests.tests_hometasks.faked_data.factories import HometaskFactory
from tests.tests_hometasks.faked_data.fake_files import (
    generate_temp_file,
    generate_temp_image,
)

pytestmark = pytest.mark.django_db


class TestHometaskViewSet:
    def test_action_create_no_files(self, api_client):
        data = {
            "name": "test_name",
            "start_datetime": "2022-10-30 01:55:39",
            "end_datetime": "2022-10-30 01:55:39",
            "url": "http://njnj.ru/golits/golits_tenses2.htm",
            "more_info": "Additional test info",
        }
        url = reverse("hometasks-list")

        assert Hometask.objects.count() == 0

        response = api_client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Hometask.objects.count() == 1

        hometask = Hometask.objects.first()

        hometask.start_datetime = hometask.start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        hometask.end_datetime = hometask.end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        assert data["name"] == hometask.name
        assert data["start_datetime"] == hometask.start_datetime
        assert data["end_datetime"] == hometask.end_datetime
        assert data["url"] == hometask.url
        assert data["more_info"] == hometask.more_info

    def test_action_create_one_image_one_file(self, api_client):
        images = generate_temp_image(counter=1)
        files = generate_temp_file(counter=1)

        data = {
            "name": "test_name",
            "start_datetime": "2022-10-30 01:55:39",
            "end_datetime": "2022-10-30 01:55:39",
            "url": "http://njnj.ru/golits/golits_tenses2.htm",
            "more_info": "Additional test info",
            "images": images,
            "files": files,
        }

        url = reverse("hometasks-list")

        assert Hometask.objects.count() == 0
        assert HometaskImage.objects.count() == 0
        assert HometaskFile.objects.count() == 0

        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Hometask.objects.count() == 1
        assert HometaskImage.objects.count() == 1
        assert HometaskFile.objects.count() == 1

        hometask = Hometask.objects.first()

        hometask.start_datetime = hometask.start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        hometask.end_datetime = hometask.end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        assert data["name"] == hometask.name
        assert data["start_datetime"] == hometask.start_datetime
        assert data["end_datetime"] == hometask.end_datetime
        assert data["url"] == hometask.url
        assert data["more_info"] == hometask.more_info

    def test_action_create_multiple_files(self, api_client):
        images = generate_temp_image(counter=2)
        files = generate_temp_file(counter=2)

        data = {
            "name": "test_name",
            "start_datetime": "2022-10-30 01:55:39",
            "end_datetime": "2022-10-30 01:55:39",
            "url": "http://njnj.ru/golits/golits_tenses2.htm",
            "more_info": "Additional test info",
            "images": images,
            "files": files,
        }

        url = reverse("hometasks-list")

        assert Hometask.objects.count() == 0
        assert HometaskImage.objects.count() == 0
        assert HometaskFile.objects.count() == 0

        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Hometask.objects.count() == 1
        assert HometaskImage.objects.count() == 2
        assert HometaskFile.objects.count() == 2

        hometask = Hometask.objects.first()

        hometask.start_datetime = hometask.start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        hometask.end_datetime = hometask.end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        assert data["name"] == hometask.name
        assert data["start_datetime"] == hometask.start_datetime
        assert data["end_datetime"] == hometask.end_datetime
        assert data["url"] == hometask.url
        assert data["more_info"] == hometask.more_info

    def test_action_list(self, api_client, django_assert_max_num_queries):

        hometasks_array = [HometaskFactory() for _ in range(3)]
        assert len(hometasks_array) == 3

        url = reverse("hometasks-list")

        with django_assert_max_num_queries(3):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert len(json_response) == 3
        assert len(json_response[0]["images"]) == 1
        assert len(json_response[2]["files"]) == 1

    def test_action_retrieve(self, api_client, django_assert_max_num_queries):

        hometask = HometaskFactory()

        url = reverse("hometasks-detail", kwargs={"pk": hometask.pk})

        with django_assert_max_num_queries(3):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_action_delete(self, api_client):
        hometask = HometaskFactory()

        assert Hometask.objects.count() == 1
        assert HometaskImage.objects.count() == 1
        assert HometaskFile.objects.count() == 1

        url = reverse("hometasks-detail", kwargs={"pk": hometask.pk})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Hometask.objects.count() == 0
        assert HometaskImage.objects.count() == 0
        assert HometaskFile.objects.count() == 0

    def test_action_update(self, api_client):
        hometask = HometaskFactory()

        assert Hometask.objects.count() == 1

        data = {
            "name": "Abs new name",
            "start_datetime": "2023-10-30 01:55:39",
            "end_datetime": "2023-10-30 01:55:39",
            "url": "https://heeeeeeeey.com/",
            "more_info": "New test info",
            "coursebook": "New cb",
            "exercises": "some exercises",
        }

        url = reverse("hometasks-detail", kwargs={"pk": hometask.pk})

        response = api_client.put(url, data=data)

        assert response.status_code == status.HTTP_200_OK

        assert Hometask.objects.count() == 1
        hometask = Hometask.objects.first()

        hometask.start_datetime = hometask.start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        hometask.end_datetime = hometask.end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        assert hometask.name == data["name"]
        assert hometask.start_datetime == data["start_datetime"]
        assert hometask.end_datetime == data["end_datetime"]
        assert hometask.url == data["url"]
        assert hometask.more_info == data["more_info"]
        assert hometask.coursebook == data["coursebook"]
        assert hometask.exercises == data["exercises"]
