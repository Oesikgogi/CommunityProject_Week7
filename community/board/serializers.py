from rest_framework import serializers
from .models import Post, Comment
from django.utils import timezone

class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'created_at']

    def get_created_at(self,obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

class PostserializerWithoutTime(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


        
# 댓글 작성 시 request 객체로써 사용 : comment 필드만 받아옴
class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

# 댓글 목록 조회 시 response 객체로써 사용 : Comment 모델의 모든 필드 return하면 됨
class CommentResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

class PostDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    comments = CommentResponseSerializer(many=True, read_only=True)
    # 역참조하려면 아까 정의했던 related_name을 가지는 변수에, 원하는 return값 필드들을 가지는 시리얼라이저를 넣으면 됨
    # 여러 댓글을 시리얼라이저에 넣을 것이기 때문에 many=True
    # 단순히 댓글들을 조회해서 뱉는 역할만 하면 되므로 read_only=True

    class Meta:
        model = Post
        exclude = ['user']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

