from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = '__all__'


class RegistrationSerializer(UserSerializer):
    username = serializers.CharField(required=True)
    mobile_number = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={"input_type": "password"}, required=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    def validate(self, validated_data):
        user = User.objects.filter(Q(username=validated_data['username']) |
                                   Q(mobile_number=validated_data['mobile_number'])|
                                   Q(email=validated_data['email']))
        if user.exists():
            raise serializers.ValidationError({'detail': 'User already exists.'})
        return validated_data

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'detail': 'Passwords must match.'})

        user.set_password(password)
        user.date_of_birth = validated_data['date_of_birth']
        user.mobile_number = validated_data['mobile_number']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'mobile_number', 'email', 'first_name', 'last_name', 'date_of_birth',
                  'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value
