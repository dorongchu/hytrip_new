from django.conf import settings
from django.db import models
from django.urls import reverse
from pytz import timezone

def local_time(input_time):
    fmt = '%Y-%m-%d %H:%M'
    my_zone = timezone(settings.TIME_ZONE)
    my_local_time = input_time.astimezone(my_zone)
    return my_local_time.strftime(fmt)

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 'auth.User'라고 쓰는 것보다 강추
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='게시자',
    )
    name = models.CharField('제목', max_length=20)
    desc = models.TextField('내용')
    photo = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='tags')
    post_hit = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def short_content(self):
        if self.desc:
            t = self.desc[:20] + '...'   # content 속성의 일부만 반환
        else:
            t = '(내용 없음)'
        return t
    short_content.short_description = '간략 내용'

    def tagged(self):
        ts = self.tags.all()
        return  ', '.join(map(str, ts))

    tagged.short_description = '태그 집합'

    def updated(self):
        return local_time(self.updated_at)
    updated.short_description = '수정 일시'

    def get_absolute_url(self):
        # return reverse('blog:post_detail', args=[self.pk])
        return reverse('post:post_detail', kwargs={'pk': self.pk})

    @property
    def update_counter(self):
        self.post_hit = self.post_hit + 1
        self.save()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='게시물')
    message = models.TextField('댓글')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-post__id', '-id']  # '-post__id', '-id'

    def __str__(self):
        return self.message

    def updated(self):
        return local_time(self.updated_at)
    updated.short_description = '수정 일시'

class Tag(models.Model):
    name = models.CharField('태그', max_length=100, unique=True)

    class Meta:
        ordering = ['-id']  # Tag 객체의 기본 정렬 순서 지정

    def __str__(self):
        return self.name