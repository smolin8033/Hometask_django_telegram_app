from django.contrib import admin

from hometask.models import Hometask, HometaskFile, HometaskImage


# Register your models here.
@admin.register(Hometask)
class Hometask(admin.ModelAdmin):
    pass


@admin.register(HometaskImage)
class HometaskImage(admin.ModelAdmin):
    pass


@admin.register(HometaskFile)
class HometaskFile(admin.ModelAdmin):
    pass
