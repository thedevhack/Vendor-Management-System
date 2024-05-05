from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.serializers import UserSerializer
from django.contrib.auth.models import User


class RegisterUser(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            token_obj, _ = Token.objects.get_or_create(user=user)
            return Response({"token": str(token_obj)})
