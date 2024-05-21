import datetime
from rest_framework import serializers
from tourList.models import Order, Review, SavedPlace, TourItem, TourList
from user.serializers import UserSerializer
from django.db.models import Q, Avg

class tourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourList
        fields = ('id', 'company', 'name', 'duration', 'price','level','created_date','modified_date', 'province', 'district', 'description', 'main_img_path', 'type', 'tag1', 'tag2', 'tag3', 'recommended_people_no')
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.createdDate = datetime.datetime.now(datetime.timezone.utc)
        instance.save()
        return instance
    
class TourItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourItem
        fields = ('id', 'tour_id','name', 'duration', 'price','level','description', 'created_date','modified_date', 'img_path')
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.createdDate = datetime.datetime.now(datetime.timezone.utc)
        instance.modified_date = instance.created_date
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'tour_id','user_id','user', 'review', 'review_date','rating')
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.review_date = datetime.datetime.now(datetime.timezone.utc)
        instance.save()
        return instance

class SavedPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPlace
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'bankaccountno': {'read-only': True}
        }
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.order_date = datetime.datetime.now(datetime.timezone.utc)
        instance.save()
        return instance