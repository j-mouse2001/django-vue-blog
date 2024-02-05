from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown


# Create your models here.
class Category(models.Model):
    """文章分类"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Tag(models.Model):
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text


class Avatar(models.Model):
    content = models.ImageField(upload_to="avatar/%Y%m%d")


# 创建一个博客文章的类
class Article(models.Model):

    # 由admin做的作者
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles'
    )

    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    # 标题
    title = models.CharField(max_length=100)

    # 正文
    body = models.TextField()

    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc 是渲染后的目录
        return md_body, md.toc

    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    # 更新时间
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


