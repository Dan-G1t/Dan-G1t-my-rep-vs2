from rest_framework import serializers
from .models import Pass, CustomUser, Coordinates, Level, Image


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'fam', 'name', 'otc', 'phone']


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title']


class PassSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    coords = CoordinatesSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pass
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'level', 'images']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        user, created = CustomUser.objects.get_or_create(email=user_data['email'], defaults=user_data)

        coords = Coordinates.objects.create(**coords_data)
        level = Level.objects.create(**level_data)

        pass_instance = Pass.objects.create(user=user, coords=coords, level=level, **validated_data)

        for img_data in images_data:
            Image.objects.create(pass_reference=pass_instance, **img_data)

        return pass_instance