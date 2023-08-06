# usage
    class UserPhotoSerializer(FlexFieldsModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)

    photo = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = UserPhoto
        fields = ('id', 'url', 'user', 'photo', 'thumbnail')

