from .models import Post, Comment
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def post_list(request):
	if request.method == 'GET':
		posts = Post.objects.all()
		serializer = PostserializerWithoutTime(posts, many = True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	elif request.method == 'POST':
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
	return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = PostDetailSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def create_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    serializer = CommentRequestSerializer(data=request.data) # 들어오는 데이터를 시리얼라이저로 보냄
    if serializer.is_valid():
        new_comment = serializer.save(post=post)
        response = CommentResponseSerializer(new_comment) # 응답용 시리얼라이저에 데이터 보냄
        return Response(response.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_comments(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)
    # filter 함수 : 조건에 맞는 객체를 필터링해서 가져옴.
    # 1개의 데이터만 가져올 수 있고, 2개 이상이나 0개의 데이터가 탐색되면 에러를 발생시키는 get과 다르게
    # 0개나 여러개의 데이터가 가져와져도 에러 발생시키지 않음
    serializer = CommentResponseSerializer(comments, many=True) # 응답용 시리얼라이저에 데이터 보냄
    return Response(serializer.data, status=status.HTTP_200_OK)