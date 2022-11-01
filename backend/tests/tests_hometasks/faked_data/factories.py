import factory
from factory import RelatedFactory
from factory.django import DjangoModelFactory
from faker import Faker
from hometask.models import Hometask, HometaskFile, HometaskImage

faker = Faker()


class HometaskImageFactory(DjangoModelFactory):
    """Фабрика для модели изображения к домашнему заданию"""

    hometask = None
    image = factory.django.ImageField(width=50, height=50)

    class Meta:
        model = HometaskImage


class HometaskFileFactory(DjangoModelFactory):
    """Фабрика для модели файла к домашнему заданию"""

    hometask = None
    file = factory.django.FileField()

    class Meta:
        model = HometaskFile


class HometaskFactory(DjangoModelFactory):
    """Фабрика для модели домашнего задания"""

    name = faker.word()
    start_datetime = faker.date_time_this_month()
    end_datetime = faker.future_datetime()
    coursebook = faker.word()
    exercises = faker.word()
    url = faker.url()
    more_info = faker.text()

    hometask = RelatedFactory(
        HometaskImageFactory,
        factory_related_name="hometask",
        image=factory.django.ImageField(width=50, height=50),
    )

    hometask_1 = RelatedFactory(
        HometaskFileFactory,
        factory_related_name="hometask",
        file=factory.django.FileField(),
    )

    class Meta:
        model = Hometask
