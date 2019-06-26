from rest_framework import serializers
from meiduoAdmin.serializers.home_serializers import UserGoodsDaySerializer
from users.models import User




#2,获取用户信息，序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoodsDaySerializer
        fields=("id","username","mobile","email")


# 3,新增用户,序列化器
class UserAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "mobile", "email", "password")

        # 1,添加额外的约束,不返回密码
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    # 1,重写create方法,加密密码
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
