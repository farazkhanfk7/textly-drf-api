from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import permission_classes # Djnago permission won't work with APIView
from .serializers import UserSerializer,TextSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helpers import check_grammer,check_sentiment,get_textgen,get_correct_sentence,get_grammer_gif,get_sentiment_gif

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]


@permission_classes((permissions.AllowAny,)) # This decorator to be used with APIView
class TestAPI(APIView):
    def get(self, request):     
        return Response("Please send text through POST")

    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            response = dict()
            try:
                sentence = get_correct_sentence(data)
                grammer_result = check_grammer(sentence)
                sentiment = check_sentiment(sentence)
                generated_text = get_textgen(sentence)
                response["grammer"] = grammer_result
                response["grammer_gif"] = get_grammer_gif(grammer_result)
                response["sentiment"] = sentiment
                response["sentiment_gif"] = get_sentiment_gif(sentiment)
                response["generated_text"] = generated_text
            except KeyError:
                response["Oops"] = "Please enter a sentence in POST request"
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,)) # This decorator to be used with APIView
class CheckAPI(APIView):
    def get(self, request):     
        return Response("Please send text through POST")

    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            response = dict()
            try:
                sentence = get_correct_sentence(data)
                grammer_result = check_grammer(sentence)
                sentiment = check_sentiment(sentence)
                response["grammer"] = grammer_result
                response["grammer_gif"] = get_grammer_gif(grammer_result)
                response["sentiment"] = sentiment
                response["sentiment_gif"] = get_sentiment_gif(sentiment)
            except KeyError:
                response["Oops"] = "Please enter a sentence in POST request"
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,)) # This decorator to be used with APIView
class GenAPI(APIView):
    def get(self, request):     
        return Response("Please send text through POST")

    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            response = dict()
            try:
                sentence = get_correct_sentence(data)
                generated_text = get_textgen(sentence)
                response["generated_text"] = generated_text
            except KeyError:
                response["Oops"] = "Please enter a sentence in POST request"
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,)) # This decorator to be used with APIView
class SpellAPI(APIView):
    def get(self, request):     
        return Response("Please send text through POST")

    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            response = dict()
            try:
                correct_text = get_correct_sentence(data)
                response["correct_text"] = correct_text
            except KeyError:
                response["Oops"] = "Please enter a sentence in POST request"
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)