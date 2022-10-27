from django.contrib import admin

from hometask.models import Hometask, HometaskImage, HometaskFile


@admin.register(Hometask)
class HometaskAdmin(admin.ModelAdmin):
    pass


@admin.register(HometaskImage)
class HometaskImageAdmin(admin.ModelAdmin):
    pass


@admin.register(HometaskFile)
class HometaskFileAdmin(admin.ModelAdmin):
    pass
