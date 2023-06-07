from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CommonModel, User
from emoticons.models import EmoticonImage

# Create your models here.
class Article(CommonModel):
    """
    게시글 모델입니다.
    아직 User모델과합치지않아서 User모델은 주석처리해뒀습니다.
    지도연동부분도 지도연동후에 주석을풀겠습니다.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256,)
    content = models.TextField()
    images = models.ImageField(null=True,blank=True)
    score = models.FloatField(null=True,blank=True,validators=[MinValueValidator(0),MaxValueValidator(10),])
    # place = models.CharField(max_length=200,null=True,blank=True) #필드를 뭐로 할지 아직 잘 모르겠습니다. 좌표는 숫자라 integer 일 거 같긴 한데 더 만들어보고 정하겠습니다.

    def __int__(self):
        return self.id

    def clean(self):
        if self.score >= 10:
            raise ValidationError("숫자는 10 이하로 입력해주세요.")

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'article'


class Tag(CommonModel):
    """
    Tag관련 모델입니다.
    tag
    """
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag


class TagList(CommonModel):
    """
    Article, Tag 모델의 중간
    """
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

    def __str__(self):
        return self.article

    def __str__(self):
        return f'작성자: {self.writer} - 내용: {self.comment}'

class Comment(CommonModel):
    """
    댓글 모델입니다.
    게시글 객체와 일대다 관계를 가집니다.
    Comment객체는 게시글 객체를 의미하는 article필드, 댓글 작성자를 의미하는 writer필드,
    댓글내용의 comment필드, 사용된 이모티콘을 의미하는 use_emoticon필드로 구성됩니다.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField("댓글 내용", blank=True)
    use_emoticon = models.ForeignKey(EmoticonImage, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'작성자: {self.writer} - 내용: {self.comment}'

class CommentLike(CommonModel):
    likers = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment