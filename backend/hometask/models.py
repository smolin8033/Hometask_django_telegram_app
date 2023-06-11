from django.db import models
from django.db.models import FileField, ImageField


class Hometask(models.Model):
    """
    Домашнее задание
    """

    name = models.CharField(max_length=60, verbose_name="Название д/з")
    start_datetime = models.DateTimeField(verbose_name="Время начала выполнения д/з")
    end_datetime = models.DateTimeField(verbose_name="Время сдачи д/з")
    coursebook = models.CharField(max_length=50, verbose_name="Название учебника", blank=True)
    exercises = models.CharField(max_length=50, verbose_name="Упражнения для выполнения", blank=True)
    url = models.URLField(
        max_length=200,
        verbose_name="Ссылка для прикрепления в случае необходимости",
        blank=True,
    )
    more_info = models.TextField(verbose_name="Дополнительная информация", blank=True)

    def __str__(self) -> str:
        return self.name


class HometaskBaseFile(models.Model):
    hometask = models.ForeignKey(Hometask, on_delete=models.CASCADE)
    file = ...

    class Meta:
        abstract = True


class HometaskImage(HometaskBaseFile):
    """
    Изображение для прикрепления к домашнему заданию
    """

    hometask = models.ForeignKey(Hometask, related_name="images", on_delete=models.CASCADE)
    file: ImageField = ImageField()

    def __str__(self) -> str:
        return str(self.file)


class HometaskFile(HometaskBaseFile):
    """
    Файл для прикрепления к домашнему заданию
    """

    hometask = models.ForeignKey(Hometask, related_name="files", on_delete=models.CASCADE)
    file: FileField = FileField()

    def __str__(self) -> str:
        return str(self.file)
