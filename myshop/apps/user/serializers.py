import re
from datetime import datetime, timedelta
from myshop.settings import REGEX_MOBILE
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册
    '''
    #验证用户名是否存在
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    # 输入密码的时候不显示明文
    password = serializers.CharField(
        style={'input_type': 'password'}, label=True, write_only=True
    )

    # 密码加密保存
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

        # 所有字段。attrs是字段验证合法之后返回的总的dict
    def validate(self, attrs):
        #前端没有传mobile值到后端，这里添加进来
        attrs["mobile"] = attrs["username"]
        #code是自己添加得，数据库中并没有这个字段，验证完就删除掉
        return attrs

    class Meta:
        model = User
        fields = ('username', 'mobile', 'password')

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email","mobile")
