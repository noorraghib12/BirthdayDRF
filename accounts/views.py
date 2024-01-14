from rest_framework.views import APIView
from rest_framework.response import Response
from .emails import *
from .serializer import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterAPI(APIView):
    """
    REGISTRATION API
    """

    def post(self,request):
        data=request.data
        verification_serialized=RegisterSerializer(data=data)
        if verification_serialized.is_valid():
            verification_serialized.save()
            return Response({
                'status': 200,
                'message': "Registration Complete!",
                'data' : {}
            })
    
        return Response({
            'message': "Something went wrong.",
            'data' : verification_serialized.errors
        },status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'data':serializer.errors,
                'message':"Something went wrong!"
            })
        # if not User.object.get(data['username']).is_verified:
        #     return Response({
        #         'status':400,
        #         'data':serializer.errors,
        #         'message':"Sorry, user not verified!"
        #     })

        response=serializer.get_jwt_token(data=request.data)

        return Response(response,status=status.HTTP_202_ACCEPTED)