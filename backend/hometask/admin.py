from django.contrib import admin
from hometask.models import Hometask, HometaskFile, HometaskImage


# Register your models here.
@admin.register(Hometask)
class PostImage(admin.ModelAdmin):
    pass


@admin.register(HometaskImage)
class PostImage(admin.ModelAdmin):
    pass


@admin.register(HometaskFile)
class PostImage(admin.ModelAdmin):
    pass
