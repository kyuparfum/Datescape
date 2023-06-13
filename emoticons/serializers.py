from rest_framework import serializers
from emoticons.models import Emoticon, EmoticonImage, UserEmoticonList


class EmoticonImageSerializer(serializers.ModelSerializer):
    """이모티콘 이미지"""

    class Meta:
        model = EmoticonImage
        fields = (
            "id",
            "image",
            "db_status",
        )


class EmoticonSerializer(serializers.ModelSerializer):
    """이모티콘 조회 / 수정 / 삭제"""

    images = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    buy = serializers.SerializerMethodField()
    req_username = serializers.SerializerMethodField()
    req_user_email = serializers.SerializerMethodField()
    sold_count = serializers.SerializerMethodField()

    def get_images(self, emoticon):
        qs = EmoticonImage.objects.filter(db_status=1, emoticon=emoticon)
        serializer = EmoticonImageSerializer(instance=qs, many=True)
        return serializer.data

    def get_creator_name(self, emoticon):
        if emoticon.creator:
            creator = emoticon.creator.username
        else:
            creator = "서버 또는 삭제된 사용자"
        return creator

    def get_buy(self, emoticon):
        request_user = self.context.get("user")
        qs = UserEmoticonList.objects.filter(
            sold_emoticon=emoticon, db_status=1, buyer=request_user
        )
        return bool(qs)

    def get_req_username(self, emoticon):
        if self.context.get("user"):
            request_user = self.context.get("user")
            return request_user.username
        else:
            return None

    def get_req_user_email(self, emoticon):
        if self.context.get("user"):
            request_user = self.context.get("user")
            return request_user.email
        else:
            return None

    def get_sold_count(self, emoticon):
        if self.context.get("sold_count"):
            sold_count = self.context.get("sold_count")
            return sold_count
        else:
            return None

    class Meta:
        model = Emoticon
        fields = "__all__"


class EmoticonCreateSerializer(serializers.ModelSerializer):
    """이모티콘 생성"""

    images = EmoticonImageSerializer(many=True, required=False)

    class Meta:
        model = Emoticon
        fields = "__all__"

    def create(self, validated_data):
        images_data = self.context.get("images", None)
        emoticon = super().create(validated_data)
        if images_data:
            for image_data in images_data:
                EmoticonImage.objects.create(emoticon=emoticon, image=image_data)
        return emoticon


class UserEmoticonListSerializer(serializers.ModelSerializer):
    """유저가 구매한 이모티콘"""

    class Meta:
        model = UserEmoticonList
        fields = "__all__"


class EmoticonImageSerializer(serializers.ModelSerializer):
    """이모티콘 이미지"""

    class Meta:
        model = EmoticonImage
        fields = "__all__"
