from rest_framework import serializers
from core.models import User
from rest_framework.serializers import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_ambassador']
        extra_kwargs = {
            'password': {'write_only': True} # create password but not show in get
        }



    def create(self, validated_data):
        #For Hash Password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance 

    # def validate_first_name(self, first_name):
    #     if first_name is None:
    #         raise serializers.ValidationError({'msg' : 'first_name is invalid'})    
         
