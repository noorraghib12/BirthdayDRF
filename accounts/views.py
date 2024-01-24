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
        registration_serialized=RegisterSerializer(data=data)
        if registration_serialized.is_valid():
            registration_serialized.save()
            #send_otp_via_email(email=registration_serialized.data['email'])
            return Response({
                'status': 200,
                'message': "Registration Complete!",
                'data' : {}
            })
    
        return Response({
            'status': 400,
            'message': "Something went wrong.",
            'data' : registration_serialized.errors
        })




class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status':400,
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

        return Response(response,status=200)


# class ProfileWriteview(APIView):
#     """ CRUD OPERATIONS FOR USER PROFILE"""


#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]        
#     def post(self,request):
#         try:
#             data=request.data.copy()
#             data['user'] = request.user.id
#             serializer=ProfileSerializer(data=data)
#             if not serializer.is_valid():
#                 serializer.save() 
#                 return Response({
#                     'status':400,
#                     'message':"Ooops, something went wrong!",
#                     'data': serializer.errors
#                 })
#             else:
#                 return Response({
#                     'status':200,
#                     'message':"Profile data created!",
#                     'data': serializer.data
#                 })
#         except Exception as e:
#             print(e)
#             return Response({
#                 'status': 400,
#                 'message': "Ooops something went wrong",
#                 'data':{'error':e}
#             })

#     def patch(self,request):
#         data=request.data.copy()
#         data['user']=request.user.id
#         serializer=ProfileSerializer(data=data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "status":201,
#                 "message":"Profile information has been updated!", 
#                 "data":serializer.data
#             })
#         else:
#             return Response({
#                 "status":400,
#                 'message':"Sorry, there were some issues fetching the data!",
#                 'data':serializer.data
#             })



