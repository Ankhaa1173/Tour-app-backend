from rest_framework import serializers
from .models import Company, Operator, User, Constants

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name', 'email', 'password', 'user_level', 'created_date', 'phone_no']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        username = validated_data.pop('username',None)
        instance = self.Meta.model(**validated_data)
        if username is None:
            instance.set_username_email()
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'

class ConstantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constants
        fields = '__all__'
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'