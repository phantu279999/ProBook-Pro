from rest_framework import serializers

from news.models import News, Category, CategoryNews


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNews
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'title',
            'sapo',
            'url',
            'avatar',
            'date_create',
            'lastmodifield_date',
            'status',
            'is_home',
            'is_focus',
            'created_by',
            'edited_by',
            'category',
        ]

    def get_category(self, obj):
        categories = CategoryNews.objects.select_related('categoryid').filter(newsid=obj)
        return CategoryNewsSerializer(categories, many=True).data
