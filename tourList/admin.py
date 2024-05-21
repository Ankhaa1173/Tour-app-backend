from django.contrib import admin
from tourList.models import Review, TourItem, TourList
# Register your models here.
admin.site.register(TourList)
admin.site.register(TourItem)
admin.site.register(Review)