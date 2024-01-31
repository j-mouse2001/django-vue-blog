from user_info.serializers import UserDescSerializer
from rest_framework import serializers
from .models import Article, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    # view_name 参数是路由名，你必须显示指定。 category-detail 是自动注册路由时，Router 默认帮你设置的详情页面的名称，
    # 类似的还有 category-list 等
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )

    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError("Category with id {} not exists.".format(value))
        return value

    # to_internal_value() 方法原本作用是将请求中的原始 Json 数据转化为 Python 表示形式（
    # 期间还会对字段有效性做初步检查）。它的执行时间比默认验证器的字段检查更早，因此有机会在此方法中将需要的数据创建好，
    # 然后等待检查的降临。isinstance() 确定标签数据是列表，才会循环并创建新数据
    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)

        return super().to_internal_value(data)

    # 这里需要写上article的原因是我们在article这个app里的urls中写了一个变量
    # app_name = 'article'
    url = serializers.HyperlinkedIdentityField(view_name="article:detail")


class ArticleListSerializers(ArticleBaseSerializer):

    class Meta:
        model = Article

        # 把author序列化嵌套进去并且设置成只读
        fields = '__all__'


class ArticleDetailSerializers(ArticleBaseSerializer):
    body_html = serializers.SerializerMethodField()
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article:detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """标签序列化器"""
    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'


