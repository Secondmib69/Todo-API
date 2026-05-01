from rest_framework import serializers
from todo.models import Todo
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
User = get_user_model()



class TodoSerializer(serializers.ModelSerializer):


    def user_nested(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            }
        
    user = serializers.SerializerMethodField('user_nested')
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['user'] = request.user
    #     return super().create(validated_data)

    def validate_priority(self, value):
        if value > 20:
            raise serializers.ValidationError('Maximum priority is 20')
        return value

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):

    def user_todos_count(self, obj):
        return obj.todos.count()

    password = serializers.CharField(validators=[validate_password], write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm password')
    todos_count = serializers.SerializerMethodField('user_todos_count')

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'first_name', 'last_name', 'email', 'todos_count', 'is_staff', 'is_active',]


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('passwords dont match')
        return attrs

    # def create(self, validated_data):
    #     validated_data.pop('password2')
    #     password = validated_data.pop('password')
    #     user = User(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user

