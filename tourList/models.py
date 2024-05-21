import django
from django.db import models
from user.models import User, Company
import datetime
# Create your models here.
def upload_path(instance, filename):
    print(instance.company)

    return '/'.join([instance.company.name  + str(instance.company.id) , str(instance.name + str( instance.id)), instance.name + '_' +filename])

def upload_path_item(instance, filename):
    # tour = TourList.objects.get(pk = instance.tour_id)
    # comp = Company.objects.get(pk = tour.company.id)
    return '/'.join([instance.tour_id.company.name  + str(instance.tour_id.company_id) , instance.tour_id.name + str(instance.tour_id.id), instance.tour_id.name + '_' + str(instance.tour_id.id) + '_' + instance.name + '_' + filename])

class TourList(models.Model):
    name = models.CharField(max_length = 50)
    duration = models.IntegerField(default =  0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.IntegerField(default = 0)
    level = models.IntegerField(default = 1)
    recommended_people_no = models.IntegerField(default=1)
    type = models.CharField(max_length=20)
    tag1 = models.CharField(max_length=30)
    tag2 = models.CharField(max_length=30)
    tag3 = models.CharField(max_length=30)
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    main_img_path = models.ImageField(blank=True, null=True, upload_to=upload_path)
    created_date = models.DateTimeField(default =  django.utils.timezone.now)
    modified_date = models.DateTimeField(default =  django.utils.timezone.now)

class TourItem(models.Model):
    name = models.CharField(max_length = 50)
    tour_id = models.ForeignKey(TourList, on_delete=models.CASCADE)
    img_path = models.ImageField(blank=True, null=True, upload_to=upload_path_item)
    duration = models.DecimalField(max_digits=3, decimal_places=2)
    price = models.IntegerField()
    level = models.IntegerField()
    description = models.CharField(max_length=2000)
    created_date = models.DateTimeField(default = django.utils.timezone.now)
    modified_date = models.DateTimeField(default =  django.utils.timezone.now)

class Review(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    tour_id = models.ForeignKey(TourList, on_delete=models.CASCADE)
    rating =  models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review = models.CharField(max_length=1000)
    review_date = models.DateTimeField(default=django.utils.timezone.now)

class SavedPlace(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    tour_id = models.ForeignKey(TourList, on_delete=models.CASCADE)


class Order(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    tour_id = models.ForeignKey(TourList, on_delete=models.CASCADE)
    tour_date =  models.DateTimeField(default=django.utils.timezone.now)
    order_date =  models.DateTimeField(default=django.utils.timezone.now)
    pay_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_confirmed = models.BooleanField()
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    bank_account_no = models.CharField(max_length=20)
    status = models.CharField(max_length=20)